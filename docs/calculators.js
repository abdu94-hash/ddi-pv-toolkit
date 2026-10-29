/*
 * ddi-pv-toolkit calculators: JavaScript port of the Python package ddi_toolkit.
 *
 * Calculators from "Drug-Drug Interactions in Drug Safety and Pharmacovigilance"
 * (Dr. Hafez Selim). Names, inputs and outputs match spec/CALCULATORS.md and
 * spec/vectors.json exactly.
 *
 * EDUCATIONAL USE ONLY. These functions reproduce the book's worked calculations
 * with simplified static models. They teach the reasoning; they do not predict
 * what happens in an individual and must not be used for dosing or any other
 * clinical decision.
 *
 * No dependencies and no build step. Works as a classic <script> (exposes
 * window.DDI) and from Node (module.exports, or `import DDI from "./calculators.js"`).
 * Every calculator takes one object of named inputs and returns an object of
 * named outputs; invalid inputs throw a ValidationError (a RangeError subclass)
 * whose message matches the Python ValueError message.
 */
(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.DDI = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  // ---------------------------------------------------------------- validation

  function ValidationError(message) {
    var err = new RangeError(message);
    err.name = "ValidationError";
    return err;
  }

  /** Format like Python's {:g}: six significant digits, no trailing zeros. */
  function g(v) {
    if (typeof v !== "number" || !isFinite(v)) return String(v);
    if (v === 0) return "0";
    var abs = Math.abs(v);
    if (abs >= 1e-4 && abs < 1e6) return String(Number(v.toPrecision(6)));
    var s = v.toExponential(5).replace(/\.?0+e/, "e");
    return s.replace(/e([+-])(\d)$/, "e$10$2");
  }

  function given(x) {
    return x !== undefined && x !== null;
  }

  function number(name, value) {
    if (value === undefined || value === null || value === "") throw ValidationError(name + " is required");
    if (typeof value !== "number") {
      throw ValidationError(name + " must be a number, got " + JSON.stringify(value === undefined ? null : value));
    }
    if (!isFinite(value)) throw ValidationError(name + " must be a finite number, got " + value);
    return value;
  }

  function positive(name, value) {
    var v = number(name, value);
    if (v <= 0) throw ValidationError(name + " must be greater than 0, got " + g(v));
    return v;
  }

  function nonnegative(name, value) {
    var v = number(name, value);
    if (v < 0) throw ValidationError(name + " must be 0 or greater, got " + g(v));
    return v;
  }

  function fraction(name, value, opts) {
    opts = opts || {};
    var allowZero = opts.allowZero !== false;
    var allowOne = opts.allowOne !== false;
    var v = number(name, value);
    var lowOk = v > 0 || (allowZero && v === 0);
    var highOk = v < 1 || (allowOne && v === 1);
    if (!(lowOk && highOk)) {
      throw ValidationError(
        name + " must be in the range " + (allowZero ? "[0" : "(0") + ", " + (allowOne ? "1]" : "1)") + ", got " + g(v)
      );
    }
    return v;
  }

  function count(name, value, minimum) {
    minimum = minimum === undefined ? 0 : minimum;
    var v = number(name, value);
    if (v !== Math.trunc(v)) throw ValidationError(name + " must be a whole number, got " + g(v));
    if (v < minimum) throw ValidationError(name + " must be at least " + minimum + ", got " + v);
    return v;
  }

  function atLeast(name, value, minimum) {
    var v = number(name, value);
    if (v < minimum) throw ValidationError(name + " must be at least " + g(minimum) + ", got " + g(v));
    return v;
  }

  function optionalPair(nameA, a, nameB, b) {
    if (given(a) !== given(b)) throw ValidationError("give both " + nameA + " and " + nameB + ", or neither");
    return given(a);
  }

  function log2(x) {
    return Math.log(x) / Math.LN2;
  }

  // ---------------------------------------------------------- gamma quantile
  // Same method as python/src/ddi_toolkit/_gamma.py: bisection on the
  // regularized lower incomplete gamma function (series / continued fraction).

  var LANCZOS = [
    0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6,
    1.5056327351493116e-7,
  ];

  function lgamma(x) {
    if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - lgamma(1 - x);
    x -= 1;
    var a = LANCZOS[0];
    var t = x + 7.5;
    for (var i = 1; i < 9; i++) a += LANCZOS[i] / (x + i);
    return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
  }

  var EPS = 1e-15;
  var MAX_ITER = 500;

  function lowerSeries(a, x) {
    var term = 1 / a;
    var total = term;
    var n = a;
    for (var i = 0; i < MAX_ITER; i++) {
      n += 1;
      term *= x / n;
      total += term;
      if (Math.abs(term) < Math.abs(total) * EPS) break;
    }
    return total * Math.exp(-x + a * Math.log(x) - lgamma(a));
  }

  function upperContinuedFraction(a, x) {
    var tiny = 1e-300;
    var b = x + 1 - a;
    var c = 1 / tiny;
    var d = 1 / b;
    var h = d;
    for (var i = 1; i < MAX_ITER; i++) {
      var an = -i * (i - a);
      b += 2;
      d = an * d + b;
      if (Math.abs(d) < tiny) d = tiny;
      c = b + an / c;
      if (Math.abs(c) < tiny) c = tiny;
      d = 1 / d;
      var delta = d * c;
      h *= delta;
      if (Math.abs(delta - 1) < EPS) break;
    }
    return Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
  }

  function gammaCdf(x, shape) {
    if (shape <= 0) throw ValidationError("shape must be greater than 0, got " + g(shape));
    if (x <= 0) return 0;
    if (x < shape + 1) return lowerSeries(shape, x);
    return 1 - upperContinuedFraction(shape, x);
  }

  function gammaQuantile(p, shape) {
    if (!(p > 0 && p < 1)) throw ValidationError("p must be strictly between 0 and 1, got " + g(p));
    if (shape <= 0) throw ValidationError("shape must be greater than 0, got " + g(shape));
    var lo = 0;
    var hi = Math.max(1, shape);
    while (gammaCdf(hi, shape) < p) hi *= 2;
    for (var i = 0; i < 200; i++) {
      var mid = 0.5 * (lo + hi);
      if (gammaCdf(mid, shape) < p) lo = mid;
      else hi = mid;
      if (hi - lo <= 1e-14 * Math.max(1, hi)) break;
    }
    return 0.5 * (lo + hi);
  }

  // ------------------------------------------------------------------- pk

  function auc_ratio_inhibition(o) {
    o = o || {};
    var fm = fraction("fm", o.fm);
    if (given(o.fraction_inhibited) === given(o.i_over_ki)) {
      throw ValidationError("give exactly one of fraction_inhibited or i_over_ki");
    }
    var inhibited;
    if (given(o.i_over_ki)) {
      var r = nonnegative("i_over_ki", o.i_over_ki);
      inhibited = r / (1 + r);
    } else {
      inhibited = fraction("fraction_inhibited", o.fraction_inhibited);
    }
    var remaining = 1 - fm * inhibited;
    if (remaining <= 0) {
      throw ValidationError("fm = 1 with complete inhibition leaves no clearance: the AUC ratio is unbounded");
    }
    var gut = 1;
    if (optionalPair("fg_before", o.fg_before, "fg_after", o.fg_after)) {
      var before = fraction("fg_before", o.fg_before, { allowZero: false });
      var after = fraction("fg_after", o.fg_after, { allowZero: false });
      gut = after / before;
    }
    var systemic = 1 / remaining;
    return {
      fraction_inhibited: inhibited,
      remaining_clearance: remaining,
      auc_ratio_systemic: systemic,
      gut_factor: gut,
      auc_ratio: systemic * gut,
    };
  }

  function fm_ceiling(o) {
    o = o || {};
    var fm = fraction("fm", o.fm, { allowOne: false });
    var ceiling = 1 / (1 - fm);
    return {
      remaining_clearance: 1 - fm,
      auc_ratio_max: ceiling,
      max_increase_percent: (ceiling - 1) * 100,
    };
  }

  function inhibition_from_auc_ratio(o) {
    o = o || {};
    var fm = fraction("fm", o.fm, { allowZero: false });
    var r = atLeast("auc_ratio", o.auc_ratio, 1);
    var ceiling = fm === 1 ? Infinity : 1 / (1 - fm);
    if (r > ceiling) {
      throw ValidationError(
        "auc_ratio " + g(r) + " exceeds the ceiling 1 / (1 - fm) = " + Number(ceiling.toPrecision(3)) +
          " for fm = " + g(fm) + "; the excess cannot come from this pathway alone " +
          "(for example, gut-wall or transporter inhibition; Calculation 23.1)"
      );
    }
    var inhibited = (1 - 1 / r) / fm;
    return {
      fraction_inhibited: inhibited,
      remaining_pathway_activity: 1 - inhibited,
      auc_ratio_max: isFinite(ceiling) ? ceiling : null,
    };
  }

  function induction_auc_ratio(o) {
    o = o || {};
    var fm = fraction("fm", o.fm);
    var k = atLeast("activity_multiplier", o.activity_multiplier, 1);
    var fRatio = 1;
    if (optionalPair("bioavailability_before", o.bioavailability_before, "bioavailability_after", o.bioavailability_after)) {
      var before = fraction("bioavailability_before", o.bioavailability_before, { allowZero: false });
      var after = fraction("bioavailability_after", o.bioavailability_after, { allowZero: false });
      fRatio = after / before;
    }
    var rc = fm * k + (1 - fm);
    var systemic = 1 / rc;
    var auc = systemic * fRatio;
    var out = {
      relative_clearance: rc,
      auc_ratio_systemic: systemic,
      bioavailability_ratio: fRatio,
      auc_ratio: auc,
      percent_change: (auc - 1) * 100,
    };
    if (given(o.baseline_concentration)) {
      out.concentration_after = nonnegative("baseline_concentration", o.baseline_concentration) * auc;
    }
    return out;
  }

  function clearance_pathways(o) {
    o = o || {};
    var fn = fraction("nonrenal_fraction", o.nonrenal_fraction);
    var fr = fraction("renal_fraction", o.renal_fraction);
    var fs = fraction("secretion_fraction", given(o.secretion_fraction) ? o.secretion_fraction : 0);
    if (Math.abs(fn + fr + fs - 1) > 1e-6) {
      throw ValidationError(
        "nonrenal_fraction + renal_fraction + secretion_fraction must sum to 1, got " + g(fn + fr + fs)
      );
    }
    var iN = fraction("nonrenal_inhibition", given(o.nonrenal_inhibition) ? o.nonrenal_inhibition : 0);
    var iS = fraction("secretion_inhibition", given(o.secretion_inhibition) ? o.secretion_inhibition : 0);
    var rf = fraction("renal_function", given(o.renal_function) ? o.renal_function : 1, { allowZero: false });
    var baseline = fn + rf * (fr + fs);
    var inhibited = fn * (1 - iN) + rf * (fr + fs * (1 - iS));
    if (inhibited <= 0) throw ValidationError("no clearance remains with these inputs: the AUC ratio is unbounded");
    return {
      baseline_clearance: baseline,
      inhibited_clearance: inhibited,
      impairment_alone_ratio: 1 / baseline,
      auc_ratio_vs_own_baseline: baseline / inhibited,
      auc_ratio_vs_normal_alone: 1 / inhibited,
    };
  }

  function protein_binding_displacement(o) {
    o = o || {};
    var dose = positive("dose_rate", o.dose_rate);
    var fu0 = fraction("fu", o.fu, { allowZero: false });
    var clu0 = positive("clu", o.clu);
    var fu1 = given(o.fu_new) ? fraction("fu_new", o.fu_new, { allowZero: false }) : fu0;
    var clu1 = given(o.clu_new) ? positive("clu_new", o.clu_new) : clu0;
    var cl0 = fu0 * clu0;
    var cl1 = fu1 * clu1;
    var c0 = dose / cl0;
    var c1 = dose / cl1;
    var cu0 = fu0 * c0;
    var cu1 = fu1 * c1;
    return {
      total_clearance: cl0,
      total_concentration: c0,
      unbound_concentration: cu0,
      total_clearance_new: cl1,
      total_concentration_new: c1,
      unbound_concentration_new: cu1,
      total_concentration_change: c1 / c0 - 1,
      unbound_concentration_ratio: cu1 / cu0,
    };
  }

  function dose_adjusted_exposure(o) {
    o = o || {};
    var r = positive("auc_ratio", o.auc_ratio);
    var d = positive("dose", o.dose);
    var d0 = positive("reference_dose", o.reference_dose);
    return { dose_fraction: d / d0, relative_exposure: (d / d0) * r };
  }

  function auc_mic(o) {
    o = o || {};
    var auc = positive("single_dose_auc", o.single_dose_auc);
    var n = positive("doses_per_day", o.doses_per_day);
    var m = positive("mic", o.mic);
    var auc24 = n * auc;
    var out = { auc_24h: auc24, auc_mic: auc24 / m };
    if (given(o.target)) {
      var t = positive("target", o.target);
      out.target_ratio = auc24 / m / t;
      out.meets_target = auc24 / m >= t;
    }
    return out;
  }

  // --------------------------------------------------------------- timing

  function time_to_steady_state(o) {
    o = o || {};
    var tHalf = positive("half_life", o.half_life);
    var n = positive("n_half_lives", given(o.n_half_lives) ? o.n_half_lives : 4);
    if (given(o.clearance_ratio) && given(o.auc_ratio)) {
      throw ValidationError("give clearance_ratio or auc_ratio, not both");
    }
    var cl = 1;
    if (given(o.auc_ratio)) cl = 1 / positive("auc_ratio", o.auc_ratio);
    else if (given(o.clearance_ratio)) cl = positive("clearance_ratio", o.clearance_ratio);
    var newHalf = tHalf / cl;
    return {
      new_half_life: newHalf,
      steady_state_ratio: 1 / cl,
      time_to_n_half_lives: n * newHalf,
      fraction_complete: 1 - Math.pow(0.5, n),
    };
  }

  function exposure_rise_after_inhibition(o) {
    o = o || {};
    var r = positive("auc_ratio", o.auc_ratio);
    var f0 = fraction("bioavailability_before", o.bioavailability_before, { allowZero: false });
    var f1 = fraction("bioavailability_after", o.bioavailability_after, { allowZero: false });
    var tHalf = positive("half_life", o.half_life);
    var t = nonnegative("time_since_start", o.time_since_start);
    var fRatio = f1 / f0;
    var fold = r / fRatio;
    var newHalf = tHalf * fold;
    var n = t / newHalf;
    var frac = 1 - Math.pow(0.5, n);
    var systemicNow = 1 + frac * (fold - 1);
    return {
      bioavailability_ratio: fRatio,
      clearance_fold: fold,
      new_half_life: newHalf,
      n_new_half_lives: n,
      fraction_to_steady_state: frac,
      systemic_fold_now: systemicNow,
      exposure_fold_now: fRatio * systemicNow,
      time_to_4_half_lives: 4 * newHalf,
      time_to_5_half_lives: 5 * newHalf,
    };
  }

  function residual_inhibition(o) {
    o = o || {};
    var tHalf = positive("half_life", o.half_life);
    var i0 = nonnegative("i_over_ki_at_stop", o.i_over_ki_at_stop);
    var t = nonnegative("time", o.time);
    var remaining = Math.pow(0.5, t / tHalf);
    var it = i0 * remaining;
    return {
      fraction_inhibitor_remaining: remaining,
      i_over_ki: it,
      pathway_activity: 1 / (1 + it),
      pathway_activity_at_stop: 1 / (1 + i0),
    };
  }

  function de_induction_remaining(o) {
    o = o || {};
    var tHalf = positive("half_life", o.half_life);
    var t = nonnegative("time", o.time);
    var remaining = Math.pow(0.5, t / tHalf);
    var out = { fraction_remaining: remaining, fraction_recovered: 1 - remaining };
    if (given(o.induced_auc_ratio)) {
      var r = fraction("induced_auc_ratio", o.induced_auc_ratio, { allowZero: false });
      var atStop = 1 / r;
      var excess = atStop - 1;
      var now = 1 + excess * remaining;
      out.clearance_multiple_at_stop = atStop;
      out.excess_at_stop = excess;
      out.clearance_multiple = now;
      out.auc_relative_to_uninduced = 1 / now;
    }
    return out;
  }

  function washout(o) {
    o = o || {};
    var tHalf = positive("recovery_half_life", o.recovery_half_life);
    var n = positive("n_half_lives", given(o.n_half_lives) ? o.n_half_lives : 5);
    var lag = nonnegative("elimination_lag", given(o.elimination_lag) ? o.elimination_lag : 0);
    var out = { time_required: n * tHalf + lag, fraction_remaining_after_n: Math.pow(0.5, n) };
    if (given(o.washout_duration)) {
      var d = nonnegative("washout_duration", o.washout_duration);
      out.fraction_remaining_at_washout = Math.pow(0.5, Math.max(0, d - lag) / tHalf);
    }
    return out;
  }

  // ------------------------------------------------------------------- qt

  function qt_correction(o) {
    o = o || {};
    var qt = positive("qt", o.qt);
    if (qt > 1000) throw ValidationError("qt is in milliseconds and must be at most 1000, got " + g(qt));
    var hr = positive("heart_rate", o.heart_rate);
    if (hr > 300) throw ValidationError("heart_rate is in beats per minute and must be at most 300, got " + g(hr));
    var rr = 60 / hr;
    return { rr: rr, qtc_bazett: qt / Math.pow(rr, 0.5), qtc_fridericia: qt / Math.pow(rr, 1 / 3) };
  }

  function exposure_qtc_line(o) {
    o = o || {};
    var m1 = positive("multiple_1", o.multiple_1);
    var m2 = positive("multiple_2", o.multiple_2);
    var q1 = number("dqtc_1", o.dqtc_1);
    var q2 = number("dqtc_2", o.dqtc_2);
    var m = nonnegative("multiple", o.multiple);
    if (m1 === m2) throw ValidationError("multiple_1 and multiple_2 must differ to define a line");
    var slope = (q2 - q1) / (m2 - m1);
    var intercept = q1 - slope * m1;
    return {
      slope: slope,
      intercept: intercept,
      dqtc: intercept + slope * m,
      extrapolated: !(Math.min(m1, m2) <= m && m <= Math.max(m1, m2)),
    };
  }

  // ------------------------------------------------------------------ epi

  function absolute_risk(o) {
    o = o || {};
    var p0 = fraction("baseline_risk", o.baseline_risk, { allowZero: false, allowOne: false });
    var rr = positive("relative_risk", o.relative_risk);
    var p1 = p0 * rr;
    if (p1 > 1) {
      throw ValidationError(
        "baseline_risk × relative_risk = " + g(p1) + " exceeds 1; the multiplicative model cannot apply at this baseline risk"
      );
    }
    var excess = p1 - p0;
    return { risk_exposed: p1, excess_risk: excess, number_needed_to_harm: excess > 0 ? 1 / excess : null };
  }

  function reporting_rate(o) {
    o = o || {};
    var n = count("cases", o.cases);
    var e = positive("exposure", o.exposure);
    var p = positive("per", given(o.per) ? o.per : 100000);
    return { rate: (n / e) * p };
  }

  function co_exposure_sensitivity(o) {
    o = o || {};
    var n1 = count("cases_with", o.cases_with);
    var n0 = count("cases_without", o.cases_without);
    var total = positive("total_exposure", o.total_exposure);
    var f = fraction("co_exposure_fraction", o.co_exposure_fraction, { allowZero: false, allowOne: false });
    var p = positive("per", given(o.per) ? o.per : 100000);
    var e1 = total * f;
    var e0 = total * (1 - f);
    var r1 = (n1 / e1) * p;
    var r0 = (n0 / e0) * p;
    return { exposure_with: e1, exposure_without: e0, rate_with: r1, rate_without: r0, rate_ratio: r0 > 0 ? r1 / r0 : null };
  }

  function proportion_ratio(o) {
    o = o || {};
    var e1 = count("events_1", o.events_1, 1);
    var n1 = count("total_1", o.total_1, 1);
    var e2 = count("events_2", o.events_2, 1);
    var n2 = count("total_2", o.total_2, 1);
    if (e1 > n1) throw ValidationError("events_1 (" + e1 + ") cannot exceed total_1 (" + n1 + ")");
    if (e2 > n2) throw ValidationError("events_2 (" + e2 + ") cannot exceed total_2 (" + n2 + ")");
    var p1 = e1 / n1;
    var p2 = e2 / n2;
    var ratio = p2 / p1;
    var se = Math.sqrt(1 / e2 - 1 / n2 + 1 / e1 - 1 / n1);
    return {
      proportion_1: p1,
      proportion_2: p2,
      ratio: ratio,
      ratio_lower: Math.exp(Math.log(ratio) - 1.96 * se),
      ratio_upper: Math.exp(Math.log(ratio) + 1.96 * se),
      difference: p2 - p1,
      difference_per_1000: (p2 - p1) * 1000,
    };
  }

  function rule_of_three(o) {
    o = o || {};
    var n = count("n", o.n, 1);
    return { upper_bound: 3 / n, one_in: n / 3 };
  }

  // ---------------------------------------------------- disproportionality

  var Z = 1.96;

  function prr_ror(o) {
    o = o || {};
    var a = count("a", o.a, 1);
    var b = count("b", o.b, 1);
    var c = count("c", o.c, 1);
    var d = count("d", o.d, 1);
    var prr = a / (a + b) / (c / (c + d));
    var sePrr = Math.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d));
    var ror = (a * d) / (b * c);
    var seRor = Math.sqrt(1 / a + 1 / b + 1 / c + 1 / d);
    return {
      prr: prr,
      se_ln_prr: sePrr,
      prr_lower: Math.exp(Math.log(prr) - Z * sePrr),
      prr_upper: Math.exp(Math.log(prr) + Z * sePrr),
      ror: ror,
      se_ln_ror: seRor,
      ror_lower: Math.exp(Math.log(ror) - Z * seRor),
      ror_upper: Math.exp(Math.log(ror) + Z * seRor),
    };
  }

  function information_component(o) {
    o = o || {};
    var a = count("a", o.a, 0);
    var b = count("b", o.b, 1);
    var c = count("c", o.c, 1);
    var d = count("d", o.d, 1);
    var n = a + b + c + d;
    var expected = ((a + b) * (a + c)) / n;
    return {
      observed: a,
      expected: expected,
      ic: log2((a + 0.5) / (expected + 0.5)),
      ic025: log2(gammaQuantile(0.025, a + 0.5) / (expected + 0.5)),
    };
  }

  function strata(o) {
    var names = ["00", "10", "01", "11"];
    var f = {};
    var n11 = 0;
    var r11 = 0;
    for (var i = 0; i < names.length; i++) {
      var k = names[i];
      var r = count("reports_" + k, o["reports_" + k], 1);
      var e = count("events_" + k, o["events_" + k], 0);
      if (e > r) throw ValidationError("events_" + k + " (" + e + ") cannot exceed reports_" + k + " (" + r + ")");
      if (e === r) {
        throw ValidationError("events_" + k + " must be less than reports_" + k + " so that the odds are finite");
      }
      f[k] = e / r;
      if (k === "11") {
        n11 = e;
        r11 = r;
      }
    }
    return { f: f, n11: n11, r11: r11 };
  }

  function four_stratum_expectations(o) {
    o = o || {};
    var s = strata(o);
    var f = s.f;
    if (f["00"] === 0) throw ValidationError("events_00 must be at least 1 for the multiplicative model");
    var mult = (f["10"] * f["01"]) / f["00"];
    var add = f["10"] + f["01"] - f["00"];
    var multCount = mult * s.r11;
    var addCount = add * s.r11;
    return {
      f00: f["00"],
      f10: f["10"],
      f01: f["01"],
      f11: f["11"],
      multiplicative_expected_f11: mult,
      multiplicative_expected_count: multCount,
      multiplicative_ratio: multCount > 0 ? s.n11 / multCount : null,
      additive_expected_f11: add,
      additive_expected_count: addCount,
      additive_excess: f["11"] - add,
      additive_ratio: addCount > 0 ? s.n11 / addCount : null,
    };
  }

  function omega_shrinkage(o) {
    o = o || {};
    var s = strata(o);
    var gg = {};
    ["00", "10", "01", "11"].forEach(function (k) {
      gg[k] = s.f[k] / (1 - s.f[k]);
    });
    var odds = Math.max(gg["00"], gg["10"]) + Math.max(gg["00"], gg["01"]) - gg["00"];
    var proportion = odds / (1 + odds);
    var e111 = proportion * s.r11;
    var n = s.n11;
    var omega = log2((n + 0.5) / (e111 + 0.5));
    return {
      g00: gg["00"],
      g10: gg["10"],
      g01: gg["01"],
      expected_odds: odds,
      expected_proportion: proportion,
      expected_count: e111,
      observed: n,
      unshrunk_log2_ratio: n > 0 && e111 > 0 ? log2(n / e111) : null,
      omega: omega,
      omega025_normal: n > 0 ? omega - Z / (Math.LN2 * Math.sqrt(n)) : null,
      omega025_gamma: log2(gammaQuantile(0.025, n + 0.5) / (e111 + 0.5)),
    };
  }

  // ---------------------------------------------------------------- liver

  function liver_injury_r_ratio(o) {
    o = o || {};
    var altX = positive("alt", o.alt) / positive("alt_uln", o.alt_uln);
    var alpX = positive("alp", o.alp) / positive("alp_uln", o.alp_uln);
    var r = altX / alpX;
    var pattern = r >= 5 ? "hepatocellular" : r <= 2 ? "cholestatic" : "mixed";
    var out = { alt_x_uln: altX, alp_x_uln: alpX, r_ratio: r, pattern: pattern };
    if (optionalPair("bilirubin", o.bilirubin, "bilirubin_uln", o.bilirubin_uln)) {
      out.bilirubin_x_uln = nonnegative("bilirubin", o.bilirubin) / positive("bilirubin_uln", o.bilirubin_uln);
    }
    return out;
  }

  // ---------------------------------------------------------------- export

  var calculators = {
    auc_ratio_inhibition: auc_ratio_inhibition,
    fm_ceiling: fm_ceiling,
    inhibition_from_auc_ratio: inhibition_from_auc_ratio,
    induction_auc_ratio: induction_auc_ratio,
    clearance_pathways: clearance_pathways,
    protein_binding_displacement: protein_binding_displacement,
    dose_adjusted_exposure: dose_adjusted_exposure,
    auc_mic: auc_mic,
    time_to_steady_state: time_to_steady_state,
    exposure_rise_after_inhibition: exposure_rise_after_inhibition,
    residual_inhibition: residual_inhibition,
    de_induction_remaining: de_induction_remaining,
    washout: washout,
    qt_correction: qt_correction,
    exposure_qtc_line: exposure_qtc_line,
    absolute_risk: absolute_risk,
    reporting_rate: reporting_rate,
    co_exposure_sensitivity: co_exposure_sensitivity,
    proportion_ratio: proportion_ratio,
    rule_of_three: rule_of_three,
    prr_ror: prr_ror,
    information_component: information_component,
    four_stratum_expectations: four_stratum_expectations,
    omega_shrinkage: omega_shrinkage,
    liver_injury_r_ratio: liver_injury_r_ratio,
  };

  var api = { calculators: calculators, gammaQuantile: gammaQuantile, gammaCdf: gammaCdf, version: "1.0.0" };
  Object.keys(calculators).forEach(function (k) {
    api[k] = calculators[k];
  });
  api.CAVEAT =
    "Educational use only: simplified static models from the book; not for dosing or clinical decisions.";
  return api;
});
