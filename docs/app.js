/*
 * Page logic for docs/index.html: builds one card per calculator from the
 * definitions below and recalculates as the reader types. The arithmetic lives
 * in calculators.js. Educational use only; not for dosing or clinical decisions.
 */
(function () {
  "use strict";

  var DDI = window.DDI;

  var GROUPS = [
    { id: "exposure", title: "Exposure and mechanisms" },
    { id: "timing", title: "Timing" },
    { id: "qt", title: "QT" },
    { id: "signal", title: "Signal detection" },
    { id: "epi", title: "Epidemiology and exposure" },
    { id: "liver", title: "Liver" },
  ];

  // u: unit shown next to the label; v: the book's worked example (blank = not given)
  var CARDS = [
    // ------------------------------------------------------------ exposure
    {
      name: "auc_ratio_inhibition",
      group: "exposure",
      title: "AUC ratio from fm and inhibition",
      purpose: "Expected rise in the object drug's exposure when one clearance pathway is inhibited, with an optional gut-wall effect.",
      inputs: [
        { k: "fm", label: "fm, fraction of clearance through the pathway", u: "0 to 1", v: 0.9 },
        { k: "fraction_inhibited", label: "Fraction of the pathway inhibited, I", u: "0 to 1; or leave blank and use [I]/Ki", v: 0.9, opt: true },
        { k: "i_over_ki", label: "[I]/Ki", u: "ratio; use instead of I", v: "", opt: true },
        { k: "fg_before", label: "Fraction escaping gut metabolism, before", u: "0 to 1, optional", v: 0.3, opt: true },
        { k: "fg_after", label: "Fraction escaping gut metabolism, with the inhibitor", u: "0 to 1, optional", v: 0.9, opt: true },
      ],
      outputs: [
        { k: "fraction_inhibited", label: "Fraction inhibited, I" },
        { k: "remaining_clearance", label: "Remaining clearance, 1 − fm × I" },
        { k: "auc_ratio_systemic", label: "AUC ratio, systemic (hepatic) part" },
        { k: "gut_factor", label: "Gut-wall factor" },
        { k: "auc_ratio", label: "AUC ratio, combined", main: true },
      ],
      formula: "AUC ratio ≈ 1 / (1 − fm × I). With [I]/Ki: AUCR = 1 / (fm / (1 + [I]/Ki) + (1 − fm)). Gut wall: multiply by (fraction escaping gut metabolism with the inhibitor) / (before).",
      book: "fm 0.9, I 0.9: 1 / 0.19 ≈ 5.3; with the gut wall (0.3 to 0.9), 3 × 5.3 ≈ 16. Calculation 5.1: fm 0.9 with [I]/Ki = 1 gives about 1.8.",
      source: "Calculation 1.1, Chapter 1; Calculation 5.1, Chapter 5",
      assumption: "Linear pharmacokinetics and one inhibited pathway; ignores transporters, metabolites, and individual variability.",
    },
    {
      name: "fm_ceiling",
      group: "exposure",
      title: "The fm ceiling",
      purpose: "The largest AUC ratio that complete inhibition of one pathway can produce.",
      inputs: [{ k: "fm", label: "fm, fraction of clearance through the pathway", u: "0 to under 1", v: 0.75 }],
      outputs: [
        { k: "remaining_clearance", label: "Remaining clearance, 1 − fm" },
        { k: "auc_ratio_max", label: "Maximum AUC ratio", main: true },
        { k: "max_increase_percent", label: "Maximum increase", unit: "%" },
      ],
      formula: "Maximum AUC ratio = 1 / (1 − fm).",
      book: "Ravolixan, fm 0.75: ceiling 4.0 (itraconazole gave 4.2). fm 0.90 → 10; 0.50 → 2.0; 0.20 → 1.25 (no more than about 25%).",
      source: "Calculation 5.1, Chapter 5; Calculation 19.1, Chapter 19; Calculation 23.1, Chapter 23",
      assumption: "Complete blockade of one pathway of systemic clearance; no gut-wall or transporter effect.",
    },
    {
      name: "inhibition_from_auc_ratio",
      group: "exposure",
      title: "Inhibition implied by an AUC ratio",
      purpose: "How much of the pathway must be inhibited to produce an observed AUC ratio (Calculation 1.1 in reverse).",
      inputs: [
        { k: "fm", label: "fm, fraction of clearance through the pathway", u: "0 to 1", v: 0.75 },
        { k: "auc_ratio", label: "Observed AUC ratio", u: "1 or more, up to 1 / (1 − fm)", v: 2.0 },
      ],
      outputs: [
        { k: "fraction_inhibited", label: "Fraction of the pathway inhibited", main: true },
        { k: "remaining_pathway_activity", label: "Remaining pathway activity" },
        { k: "auc_ratio_max", label: "Ceiling, 1 / (1 − fm)" },
      ],
      formula: "I = (1 − 1 / AUC ratio) / fm. An AUC ratio above the ceiling 1 / (1 − fm) cannot come from this pathway alone.",
      book: "Diltiazem, AUC ratio 2.0 with fm 0.75: about two-thirds inhibited, 1 / (0.75 × 0.33 + 0.25) ≈ 2.0. Try 4.2 (itraconazole) to see the ceiling.",
      source: "Calculation 23.1, Chapter 23",
      assumption: "Linear pharmacokinetics; the whole AUC change comes from the one pathway with share fm.",
    },
    {
      name: "induction_auc_ratio",
      group: "exposure",
      title: "Induction and recovered enzyme activity",
      purpose: "AUC ratio when a pathway's activity is multiplied by an inducer, or recovers when inflammation is relieved.",
      inputs: [
        { k: "fm", label: "fm, fraction of clearance through the pathway", u: "0 to 1", v: 0.7 },
        { k: "activity_multiplier", label: "Pathway activity multiplied by", u: "1 or more", v: 4 },
        { k: "bioavailability_before", label: "Bioavailability before", u: "0 to 1, optional", v: 0.5, opt: true },
        { k: "bioavailability_after", label: "Bioavailability with the inducer", u: "0 to 1, optional", v: 0.25, opt: true },
        { k: "baseline_concentration", label: "Concentration before (to scale)", u: "any unit, optional", v: "", opt: true },
      ],
      outputs: [
        { k: "relative_clearance", label: "Relative clearance" },
        { k: "auc_ratio_systemic", label: "AUC ratio, systemic part" },
        { k: "bioavailability_ratio", label: "Bioavailability factor" },
        { k: "auc_ratio", label: "AUC ratio, combined", main: true },
        { k: "percent_change", label: "Change in AUC", unit: "%" },
        { k: "concentration_after", label: "Concentration after" },
      ],
      formula: "Relative clearance = fm × multiplier + (1 − fm); AUC ratio = (1 / relative clearance) × (bioavailability after / before).",
      book: "Calculation 5.2: clearance 3.10, systemic 0.32, combined ≈ 0.16 (84% reduction). Calculation 10.1: fm 0.90, multiplier 1.8, trough 100 → clearance 1.72, about 58 ng/mL.",
      source: "Calculation 5.2, Chapter 5; Calculation 10.1, Chapter 10",
      assumption: "Linear kinetics; only the named pathway (and bioavailability, if given) changes.",
    },
    {
      name: "clearance_pathways",
      group: "exposure",
      title: "Clearance pathways and renal function",
      purpose: "Route shares, which route the precipitant affects, and what impaired renal function leaves of the rest.",
      inputs: [
        { k: "nonrenal_fraction", label: "Non-renal (e.g. hepatic) share", u: "0 to 1", v: 0.1 },
        { k: "renal_fraction", label: "Renal share not affected (e.g. filtration)", u: "0 to 1", v: 0.4 },
        { k: "secretion_fraction", label: "Tubular secretion share", u: "0 to 1", v: 0.5 },
        { k: "nonrenal_inhibition", label: "Fraction of non-renal route inhibited", u: "0 to 1", v: 0 },
        { k: "secretion_inhibition", label: "Fraction of secretion inhibited", u: "0 to 1", v: 0.6 },
        { k: "renal_function", label: "Renal function", u: "fraction of normal, 1 = normal", v: 0.4 },
      ],
      outputs: [
        { k: "baseline_clearance", label: "Clearance without the precipitant" },
        { k: "inhibited_clearance", label: "Clearance with the precipitant" },
        { k: "impairment_alone_ratio", label: "Exposure from impairment alone" },
        { k: "auc_ratio_vs_own_baseline", label: "AUC ratio vs own baseline", main: true },
        { k: "auc_ratio_vs_normal_alone", label: "AUC ratio vs healthy person alone", main: true },
      ],
      formula: "Baseline = non-renal + renal function × (renal + secretion). With the precipitant, each route loses its inhibited fraction. AUC ratio = baseline / inhibited; vs a healthy person = 1 / inhibited. The three shares must sum to 1.",
      book: "Calculation 6.2, renal function 40%: baseline 0.46 (2.2-fold already), inhibited 0.34, own ratio ≈ 1.4, vs healthy ≈ 2.9. Calculation 2.1: hepatic 0.6 inhibited 80%, renal 0.4: 1.9; with renal clearance down 75%: 3.2 and 4.5.",
      source: "Calculation 2.1, Chapter 2; Calculation 6.2, Chapter 6",
      assumption: "AUC inversely proportional to clearance; renal routes scale with renal function; shares are illustrative.",
    },
    {
      name: "protein_binding_displacement",
      group: "exposure",
      title: "Protein-binding displacement",
      purpose: "What displacement does and does not change at steady state for a low-extraction oral drug.",
      inputs: [
        { k: "dose_rate", label: "Dose rate", u: "mg/day", v: 400 },
        { k: "fu", label: "Unbound fraction, fu", u: "0 to 1", v: 0.4 },
        { k: "clu", label: "Clearance of unbound drug, CLu", u: "L/day", v: 100 },
        { k: "fu_new", label: "fu with the precipitant", u: "0 to 1, optional", v: 0.55, opt: true },
        { k: "clu_new", label: "CLu with the precipitant", u: "L/day, optional", v: "", opt: true },
      ],
      outputs: [
        { k: "total_concentration", label: "Total concentration, baseline", unit: "mg/L" },
        { k: "unbound_concentration", label: "Unbound concentration, baseline", unit: "mg/L" },
        { k: "total_concentration_new", label: "Total concentration, new", unit: "mg/L" },
        { k: "unbound_concentration_new", label: "Unbound concentration, new", unit: "mg/L", main: true },
        { k: "total_concentration_change", label: "Change in total concentration", pct: true },
        { k: "unbound_concentration_ratio", label: "Unbound concentration ratio", main: true },
      ],
      formula: "Total clearance = fu × CLu; total concentration = dose rate / total clearance; unbound concentration = fu × total.",
      book: "Baseline 10 and 4.0 mg/L. Displacement alone (fu 0.55): total 7.3 mg/L (−27%), unbound 4.0 unchanged. Add CLu 50: total 14.5, unbound 8.0 (double).",
      source: "Calculation 6.1, Chapter 6",
      assumption: "Low-extraction oral drug at steady state; average concentrations only; ignores the transient rise after displacement.",
    },
    {
      name: "dose_adjusted_exposure",
      group: "exposure",
      title: "Dose change against an AUC ratio",
      purpose: "Average exposure relative to the usual dose taken alone, after reducing the dose during coadministration.",
      inputs: [
        { k: "auc_ratio", label: "AUC ratio with the precipitant", u: "ratio", v: 4.2 },
        { k: "dose", label: "New dose", u: "mg", v: 20 },
        { k: "reference_dose", label: "Usual dose", u: "mg", v: 40 },
      ],
      outputs: [
        { k: "dose_fraction", label: "Dose fraction" },
        { k: "relative_exposure", label: "Exposure relative to usual dose alone", main: true },
      ],
      formula: "Relative exposure = (dose / usual dose) × AUC ratio.",
      book: "Ravolixan 20 mg: diltiazem 0.5 × 2.0 = 1.0; fluconazole 1.3; itraconazole 0.5 × 4.2 = 2.1; clarithromycin ≈ 2.0.",
      source: "Calculation 23.1, Chapter 23; Calculation 19.2, Chapter 19",
      assumption: "Exposure proportional to dose (linear pharmacokinetics); average exposure only; not a dose.",
    },
    {
      name: "auc_mic",
      group: "exposure",
      title: "AUC/MIC after an absorption interaction",
      purpose: "Whether a fall in absorption moves 24-hour AUC/MIC across an exposure target.",
      inputs: [
        { k: "single_dose_auc", label: "Single-dose AUC", u: "mg·h/L", v: 5.4 },
        { k: "doses_per_day", label: "Doses per day", u: "count", v: 2 },
        { k: "mic", label: "MIC of the organism", u: "mg/L", v: 0.125 },
        { k: "target", label: "Illustrative AUC/MIC target", u: "optional; the book uses 125", v: 125, opt: true },
      ],
      outputs: [
        { k: "auc_24h", label: "24-hour AUC", unit: "mg·h/L" },
        { k: "auc_mic", label: "AUC/MIC", main: true },
        { k: "target_ratio", label: "AUC/MIC as a multiple of the target" },
        { k: "meets_target", label: "At or above the target" },
      ],
      formula: "24-hour AUC ≈ doses per day × single-dose AUC; AUC/MIC = 24-hour AUC / MIC.",
      book: "Ciprofloxacin 500 mg twice daily: 29 mg·h/L alone, 10.8 with iron. MIC 0.125: 232 without iron, 86 with iron (moves below the target). Change the AUC to 14.5 to compare.",
      source: "Calculation 4.1, Chapter 4",
      assumption: "Linear pharmacokinetics, every dose affected equally, total drug; the target of 125 is illustrative, not validated.",
    },
    // -------------------------------------------------------------- timing
    {
      name: "time_to_steady_state",
      group: "timing",
      title: "Time to a new steady state",
      purpose: "New half-life, new steady state, and the time to approach it after a precipitant changes clearance.",
      inputs: [
        { k: "half_life", label: "Half-life before the change", u: "hours", v: 40 },
        { k: "n_half_lives", label: "Number of half-lives", u: "count", v: 4 },
        { k: "clearance_ratio", label: "New clearance / old clearance", u: "ratio, e.g. 0.6 for a 40% fall", v: 0.6, opt: true },
        { k: "auc_ratio", label: "Or: AUC ratio", u: "ratio; use instead of the clearance ratio", v: "", opt: true },
      ],
      outputs: [
        { k: "new_half_life", label: "New half-life", unit: "hours" },
        { k: "steady_state_ratio", label: "New steady state / old" },
        { k: "time_to_n_half_lives", label: "Time for n new half-lives", unit: "hours", main: true },
        { k: "fraction_complete", label: "Fraction of the change completed", pct: true },
      ],
      formula: "Fraction completed after n half-lives = 1 − 0.5^n. New half-life = half-life / clearance ratio; steady state changes by 1 / clearance ratio.",
      book: "Half-life 40 h, clearance down 40%: steady state 1.7-fold, new half-life ≈ 67 h, four new half-lives ≈ 267 h (about 11 days; 160 h with the old half-life).",
      source: "Section 8.2 and Calculation 8.1, Chapter 8; Calculation 21.2, Chapter 21",
      assumption: "First-order elimination, volume unchanged, precipitant effect constant from the start.",
    },
    {
      name: "exposure_rise_after_inhibition",
      group: "timing",
      title: "Exposure rise after an inhibitor starts",
      purpose: "How far exposure has risen a given time after an inhibitor's effect began.",
      inputs: [
        { k: "auc_ratio", label: "Steady-state AUC ratio", u: "ratio", v: 3.9 },
        { k: "bioavailability_before", label: "Bioavailability before", u: "0 to 1", v: 0.6 },
        { k: "bioavailability_after", label: "Bioavailability with the inhibitor", u: "0 to 1", v: 0.9 },
        { k: "half_life", label: "Half-life without the inhibitor", u: "hours", v: 14 },
        { k: "time_since_start", label: "Time since the inhibition began", u: "hours", v: 58 },
      ],
      outputs: [
        { k: "bioavailability_ratio", label: "Bioavailability factor (immediate)" },
        { k: "clearance_fold", label: "Systemic clearance fall (fold)" },
        { k: "new_half_life", label: "New half-life", unit: "hours" },
        { k: "n_new_half_lives", label: "New half-lives elapsed" },
        { k: "fraction_to_steady_state", label: "Fraction of the way to the new steady state" },
        { k: "exposure_fold_now", label: "Exposure now (fold baseline)", main: true },
        { k: "time_to_4_half_lives", label: "Four new half-lives", unit: "hours" },
        { k: "time_to_5_half_lives", label: "Five new half-lives", unit: "hours" },
      ],
      formula: "Clearance fold = AUC ratio / bioavailability factor; new half-life = half-life × clearance fold; systemic now = 1 + (1 − 0.5^(t / new half-life)) × (clearance fold − 1); exposure now = bioavailability factor × systemic now.",
      book: "Clarithromycin, Worked Case 25.1: 3.9 / 1.5 ≈ 2.6, half-life ≈ 36 h, 1.6 half-lives, 0.67 of the way, about 3.1-fold exposure at the event.",
      source: "Calculation 25.1, Chapter 25",
      assumption: "Inhibition fully established at the start time; linear kinetics; volume unchanged.",
    },
    {
      name: "residual_inhibition",
      group: "timing",
      title: "Residual inhibition after stopping",
      purpose: "Pathway activity at a given time after a reversible inhibitor with a long half-life is stopped.",
      inputs: [
        { k: "half_life", label: "Inhibitor half-life", u: "days", v: 50 },
        { k: "i_over_ki_at_stop", label: "[I]/Ki at stopping", u: "ratio", v: 4 },
        { k: "time", label: "Time since stopping", u: "days", v: 28 },
      ],
      outputs: [
        { k: "fraction_inhibitor_remaining", label: "Inhibitor remaining" },
        { k: "i_over_ki", label: "[I]/Ki now" },
        { k: "pathway_activity", label: "Pathway activity (fraction of normal)", main: true },
        { k: "pathway_activity_at_stop", label: "Activity at stopping" },
      ],
      formula: "Inhibitor remaining = 0.5^(t / half-life); activity = 1 / (1 + [I]/Ki).",
      book: "Half-life 50 days, [I]/Ki 4: activity 20% at stopping; at 28 days 0.68 remaining, [I]/Ki ≈ 2.7, activity ≈ 27%; at 100 days, 50%.",
      source: "Calculation 8.2, Chapter 8",
      assumption: "First-order elimination of a competitive, reversible inhibitor; ignores active metabolites.",
    },
    {
      name: "de_induction_remaining",
      group: "timing",
      title: "De-induction after stopping an inducer",
      purpose: "Induced enzyme excess remaining after the inducer stops, and the object drug's AUC.",
      inputs: [
        { k: "half_life", label: "Turnover (recovery) half-life", u: "days", v: 8 },
        { k: "time", label: "Time since stopping", u: "days", v: 28 },
        { k: "induced_auc_ratio", label: "AUC ratio during induction", u: "0 to 1, optional", v: 0.18, opt: true },
      ],
      outputs: [
        { k: "fraction_remaining", label: "Induced excess remaining", main: true },
        { k: "fraction_recovered", label: "Recovered" },
        { k: "clearance_multiple_at_stop", label: "Clearance at stopping (× baseline)" },
        { k: "clearance_multiple", label: "Clearance now (× baseline)" },
        { k: "auc_relative_to_uninduced", label: "AUC relative to uninduced", main: true },
      ],
      formula: "Excess remaining = 0.5^(t / half-life). Clearance at stopping = 1 / AUC ratio; clearance now = 1 + (clearance at stopping − 1) × excess remaining; AUC = 1 / clearance now.",
      book: "Rifampin (AUC 0.18), 8-day half-life, 28 days: about 9% remains, clearance ≈ 1.4, AUC ≈ 0.7 (0.9 at 42 days). Calculation 8.3: 70 h vs 8 days at 14 days gives 0.04 vs 0.30.",
      source: "Calculation 5.2, Chapter 5; Calculation 8.3, Chapter 8; Calculation 21.1, Chapter 21",
      assumption: "Inducer eliminated quickly; induced excess decays as a single exponential; turnover half-lives are uncertain, so state a range.",
    },
    {
      name: "washout",
      group: "timing",
      title: "Washout from enzyme recovery",
      purpose: "Washout length from a recovery half-life, and the effect left at a given washout.",
      inputs: [
        { k: "recovery_half_life", label: "Recovery half-life", u: "days", v: 2.3 },
        { k: "n_half_lives", label: "Number of half-lives", u: "count", v: 5 },
        { k: "elimination_lag", label: "Time for the inhibitor to be eliminated first", u: "days", v: 1.5 },
        { k: "washout_duration", label: "Washout to evaluate", u: "days, optional", v: 14, opt: true },
      ],
      outputs: [
        { k: "time_required", label: "Washout needed", unit: "days", main: true },
        { k: "fraction_remaining_after_n", label: "Effect left after n half-lives", pct: true },
        { k: "fraction_remaining_at_washout", label: "Effect left at the washout evaluated", pct: true },
      ],
      formula: "Time = n × recovery half-life + elimination lag; effect left after n half-lives = 0.5^n; at a washout D: 0.5^((D − lag) / half-life).",
      book: "Clarithromycin, recovery half-life 2.3 days: five half-lives ≈ 11.5 days leave about 3%; add 1 to 2 days: about 13 days, so the 14-day washout covers it.",
      source: "Section 21.3 and Calculation 21.1, Chapter 21",
      assumption: "Single-exponential recovery; probe-based recovery estimates assumed to apply to the object drug.",
    },
    // ------------------------------------------------------------------ qt
    {
      name: "qt_correction",
      group: "qt",
      title: "QT correction: Bazett and Fridericia",
      purpose: "How the correction formula and heart rate change the QTc from the same measured QT.",
      inputs: [
        { k: "qt", label: "Measured QT", u: "ms", v: 480 },
        { k: "heart_rate", label: "Heart rate", u: "beats per minute", v: 90 },
      ],
      outputs: [
        { k: "rr", label: "RR interval", unit: "s" },
        { k: "qtc_bazett", label: "QTc, Bazett", unit: "ms", main: true },
        { k: "qtc_fridericia", label: "QTc, Fridericia", unit: "ms", main: true },
      ],
      formula: "RR = 60 / heart rate; Bazett QTc = QT / RR^(1/2); Fridericia QTc = QT / RR^(1/3).",
      book: "QT 480 ms at 90/min: Bazett ≈ 588 ms, Fridericia ≈ 549 ms; at 60/min both give 480 ms.",
      source: "Calculation 7.1, Chapter 7",
      assumption: "Bazett overcorrects at fast heart rates; record the formula, heart rate, and measurement method.",
    },
    {
      name: "exposure_qtc_line",
      group: "qt",
      title: "Exposure–QTc line",
      purpose: "Mean ΔQTc read from a straight line through two thorough QT results.",
      inputs: [
        { k: "multiple_1", label: "Anchor 1: multiple of therapeutic exposure", u: "×", v: 1 },
        { k: "dqtc_1", label: "Anchor 1: mean ΔQTcF", u: "ms", v: 6 },
        { k: "multiple_2", label: "Anchor 2: multiple of therapeutic exposure", u: "×", v: 4 },
        { k: "dqtc_2", label: "Anchor 2: mean ΔQTcF", u: "ms", v: 18 },
        { k: "multiple", label: "Exposure to read off", u: "× therapeutic", v: 2.1 },
      ],
      outputs: [
        { k: "slope", label: "Slope", unit: "ms per multiple" },
        { k: "intercept", label: "Intercept", unit: "ms" },
        { k: "dqtc", label: "Mean ΔQTcF", unit: "ms", main: true },
        { k: "extrapolated", label: "Outside the two anchors" },
      ],
      formula: "Line through (multiple 1, ΔQTc 1) and (multiple 2, ΔQTc 2); here ΔQTcF ≈ 2 + 4 × multiple.",
      book: "2.1-fold: about 10 ms; 4.2-fold: about 19 ms; 1.3-fold (20 mg with fluconazole): about 7 ms; 3-fold (Calculation 25.1): about 14 ms.",
      source: "Calculation 19.2, Chapter 19; Calculation 25.1, Chapter 25",
      assumption: "A straight line through two means, not a fitted model; averages, not individuals.",
    },
    // -------------------------------------------------------------- signal
    {
      name: "prr_ror",
      group: "signal",
      title: "PRR and ROR",
      purpose: "Proportional reporting ratio and reporting odds ratio, with 95% confidence intervals, from a 2×2 table of reports.",
      inputs: [
        { k: "a", label: "a: drug of interest, event of interest", u: "reports", v: 47 },
        { k: "b", label: "b: drug of interest, other events", u: "reports", v: 4053 },
        { k: "c", label: "c: other drugs, event of interest", u: "reports", v: 21992 },
        { k: "d", label: "d: other drugs, other events", u: "reports", v: 9973908 },
      ],
      outputs: [
        { k: "prr", label: "PRR", main: true },
        { k: "prr_lower", label: "PRR, lower 95% limit" },
        { k: "prr_upper", label: "PRR, upper 95% limit" },
        { k: "ror", label: "ROR", main: true },
        { k: "ror_lower", label: "ROR, lower 95% limit" },
        { k: "ror_upper", label: "ROR, upper 95% limit" },
      ],
      formula: "PRR = [a / (a + b)] / [c / (c + d)]; ROR = (a × d) / (b × c); SE of ln ROR = √(1/a + 1/b + 1/c + 1/d); SE of ln PRR = √(1/a − 1/(a+b) + 1/c − 1/(c+d)); 95% CI = exp(ln ± 1.96 SE).",
      book: "Calculation 18.1: PRR 5.21 (3.92 to 6.93), ROR 5.26 (3.94 to 7.01). Calculation 18.2 (21, 399, 26, 3654): PRR 7.08 (4.02 to 12.47), ROR 7.40 (4.12 to 13.27).",
      source: "Section 18.1 and Calculations 18.1 and 18.2, Chapter 18",
      assumption: "Describes how reports are distributed, not risk; a threshold is a filter for review, not a finding.",
      fictional: true,
    },
    {
      name: "information_component",
      group: "signal",
      title: "Information component (IC)",
      purpose: "A shrunk observed-to-expected measure and its lower 95% credibility limit.",
      inputs: [
        { k: "a", label: "a: drug of interest, event of interest", u: "reports", v: 47 },
        { k: "b", label: "b: drug of interest, other events", u: "reports", v: 4053 },
        { k: "c", label: "c: other drugs, event of interest", u: "reports", v: 21992 },
        { k: "d", label: "d: other drugs, other events", u: "reports", v: 9973908 },
      ],
      outputs: [
        { k: "observed", label: "Observed, O" },
        { k: "expected", label: "Expected, E" },
        { k: "ic", label: "IC", main: true },
        { k: "ic025", label: "IC025", main: true },
      ],
      formula: "E = (a + b)(a + c) / N; IC = log2[(O + 0.5) / (E + 0.5)]; IC025 from the gamma posterior (shape O + 0.5, rate E + 0.5).",
      book: "Ravolixan × QT-related events: E = 9.04, IC = 2.32, IC025 = 1.87.",
      source: "Section 18.1 and Calculation 18.1, Chapter 18",
      assumption: "Describes reporting, not risk; the 0.5 shrinkage is a convention.",
      fictional: true,
    },
    {
      name: "four_stratum_expectations",
      group: "signal",
      title: "Four strata: additive and multiplicative",
      purpose: "Expected proportion of event reports for a combination if the drugs did not interact, under two models.",
      inputs: "STRATA",
      outputs: [
        { k: "f11", label: "Observed f11" },
        { k: "multiplicative_expected_f11", label: "Multiplicative expected f11" },
        { k: "multiplicative_expected_count", label: "Multiplicative expected count" },
        { k: "multiplicative_ratio", label: "Observed / multiplicative expected", main: true },
        { k: "additive_expected_f11", label: "Additive expected f11" },
        { k: "additive_expected_count", label: "Additive expected count" },
        { k: "additive_excess", label: "Excess proportion over additive" },
        { k: "additive_ratio", label: "Observed / additive expected", main: true },
      ],
      formula: "f = event reports / reports in each stratum. Multiplicative: expected f11 = f10 × f01 / f00. Additive: expected f11 = f10 + f01 − f00. Expected count = expected f11 × reports with both drugs.",
      book: "Ravolixan with CYP3A4 inhibitors: multiplicative 0.0247 (10.4 expected, ratio 2.0); additive 0.0121 (5.1 expected, excess 0.038, about four times).",
      source: "Section 18.2 and Calculation 18.3, Chapter 18",
      assumption: "Two models of no interaction; describes reporting, not risk, and inherits confounding and reporting bias.",
      fictional: true,
    },
    {
      name: "omega_shrinkage",
      group: "signal",
      title: "Ω shrinkage measure",
      purpose: "Observed-to-expected ratio for a combination on an additive baseline, with shrinkage, as the book defines it.",
      inputs: "STRATA",
      outputs: [
        { k: "expected_odds", label: "Expected odds" },
        { k: "expected_count", label: "Expected count, E111" },
        { k: "observed", label: "Observed, n111" },
        { k: "unshrunk_log2_ratio", label: "Unshrunk log2(n111 / E111)" },
        { k: "omega", label: "Ω", main: true },
        { k: "omega025_normal", label: "Ω025, normal approximation", main: true },
        { k: "omega025_gamma", label: "Ω025, gamma posterior", main: true },
      ],
      formula: "g = f / (1 − f); expected odds = max(g00, g10) + max(g00, g01) − g00; E111 = [odds / (1 + odds)] × reports with both; Ω = log2[(n111 + 0.5) / (E111 + 0.5)]; Ω025 ≈ Ω − 1.96 / (ln 2 × √n111), or from the gamma posterior.",
      book: "Calculation 18.3: E111 5.05, Ω 1.95, Ω025 1.34 (normal) and 1.27 (gamma). Diltiazem, Calculation 18.4 (80,000 / 200; 60 / 3): E111 0.45, Ω 1.88, Ω025 0.24 and −0.17.",
      source: "Section 18.2 and Calculations 18.3 and 18.4, Chapter 18",
      assumption: "Additive baseline on the odds scale with 0.5 shrinkage; with sparse counts report counts and interval.",
      fictional: true,
    },
    // ----------------------------------------------------------------- epi
    {
      name: "absolute_risk",
      group: "epi",
      title: "Absolute versus relative risk",
      purpose: "The same relative effect gives very different absolute harm at different baseline risks.",
      inputs: [
        { k: "baseline_risk", label: "Baseline risk", u: "proportion, 0.05 = 5%", v: 0.05 },
        { k: "relative_risk", label: "Relative risk", u: "ratio", v: 1.6 },
      ],
      outputs: [
        { k: "risk_exposed", label: "Risk with exposure", pct: true },
        { k: "excess_risk", label: "Excess risk", pct: true, main: true },
        { k: "number_needed_to_harm", label: "Number needed to harm", main: true },
      ],
      formula: "Risk with exposure = baseline × relative risk; excess = difference; number needed to harm = 1 / excess.",
      book: "NSAID, 1.6-fold: baseline 0.5% → 0.8% (1 per 333); baseline 5% → 8% (1 per 33).",
      source: "Calculation 9.1, Chapter 9",
      assumption: "Relative effect constant across baseline risk (a simplification); not causation in an individual.",
    },
    {
      name: "reporting_rate",
      group: "epi",
      title: "Reporting rate",
      purpose: "Cases per unit of exposure, from spontaneous reports.",
      inputs: [
        { k: "cases", label: "Cases", u: "count", v: 47 },
        { k: "exposure", label: "Exposure", u: "patient-years", v: 180000 },
        { k: "per", label: "Per", u: "patient-years", v: 100000 },
      ],
      outputs: [{ k: "rate", label: "Reporting rate", unit: "per denominator", main: true }],
      formula: "Rate = cases / exposure × per.",
      book: "47 / 180,000 ≈ 26.1 per 100,000 patient-years (0.26 per 1,000). Interval 24 / 61,000 = 39.3.",
      source: "Calculation 17.1, Chapter 17; Calculation 20.1, Chapter 20; Calculation 22.1, Chapter 22",
      assumption: "A reporting rate, not an incidence: it depends on under-reporting and case definition.",
      fictional: true,
    },
    {
      name: "co_exposure_sensitivity",
      group: "epi",
      title: "Co-exposure sensitivity analysis",
      purpose: "Reporting rates with and without a co-medication under an assumed share of exposure.",
      inputs: [
        { k: "cases_with", label: "Cases with the co-medication", u: "count", v: 21 },
        { k: "cases_without", label: "Cases without", u: "count", v: 26 },
        { k: "total_exposure", label: "Total exposure", u: "patient-years", v: 180000 },
        { k: "co_exposure_fraction", label: "Assumed share with the co-medication", u: "0 to 1, e.g. 0.02", v: 0.02 },
        { k: "per", label: "Per", u: "patient-years", v: 100000 },
      ],
      outputs: [
        { k: "exposure_with", label: "Exposure with", unit: "patient-years" },
        { k: "rate_with", label: "Rate with", unit: "per denominator" },
        { k: "rate_without", label: "Rate without", unit: "per denominator" },
        { k: "rate_ratio", label: "Ratio of rates", main: true },
      ],
      formula: "Exposure with = total × f; without = total × (1 − f); each rate = cases / exposure × per.",
      book: "f = 2%: 583 vs 14.7 per 100,000, ratio about 40; 5%: about 15; 10%: about 7.",
      source: "Calculation 17.1, Chapter 17; Calculation 20.1, Chapter 20; Calculation 22.1, Chapter 22",
      assumption: "The co-exposure fraction is an assumption, and reporting is assumed equally complete in both groups.",
      fictional: true,
    },
    {
      name: "proportion_ratio",
      group: "epi",
      title: "Ratio of two proportions",
      purpose: "Compare a proportion between two periods, with a 95% confidence interval and the absolute difference.",
      inputs: [
        { k: "events_1", label: "Events, group 1 (before)", u: "count", v: 198 },
        { k: "total_1", label: "Total, group 1", u: "count", v: 10400 },
        { k: "events_2", label: "Events, group 2 (after)", u: "count", v: 101 },
        { k: "total_2", label: "Total, group 2", u: "count", v: 11200 },
      ],
      outputs: [
        { k: "proportion_1", label: "Proportion 1", pct: true },
        { k: "proportion_2", label: "Proportion 2", pct: true },
        { k: "ratio", label: "Ratio, 2 / 1", main: true },
        { k: "ratio_lower", label: "Lower 95% limit" },
        { k: "ratio_upper", label: "Upper 95% limit" },
        { k: "difference_per_1000", label: "Difference per 1,000" },
      ],
      formula: "Ratio = p2 / p1; SE of ln ratio = √(1/events2 − 1/total2 + 1/events1 − 1/total1); CI = exp(ln ratio ± 1.96 SE); difference = p2 − p1.",
      book: "Strong-inhibitor co-dispensing: 1.90% → 0.90%, risk ratio 0.47 (0.37 to 0.60), about 10 fewer per 1,000.",
      source: "Calculation 24.1, Chapter 24",
      assumption: "Groups treated as independent samples; a two-period comparison cannot exclude a pre-existing trend.",
      fictional: true,
    },
    {
      name: "rule_of_three",
      group: "epi",
      title: "Rule of three",
      purpose: "Upper 95% bound for a risk when no events have been seen.",
      inputs: [{ k: "n", label: "Patients with no events", u: "count", v: 2900 }],
      outputs: [
        { k: "upper_bound", label: "Upper 95% bound", pct: true, main: true },
        { k: "one_in", label: "As 1 in", main: true },
      ],
      formula: "Upper bound ≈ 3 / n.",
      book: "No torsade de pointes in about 2,900 patients: about 3 in 2,900, roughly 1 in 1,000.",
      source: "Section 19.4, Chapter 19; Section 26.2, Chapter 26",
      assumption: "Zero events observed; the bound applies only to the conditions studied.",
    },
    // --------------------------------------------------------------- liver
    {
      name: "liver_injury_r_ratio",
      group: "liver",
      title: "R ratio for liver injury",
      purpose: "Classify the biochemical pattern of suspected drug-induced liver injury.",
      inputs: [
        { k: "alt", label: "ALT", u: "U/L", v: 1240 },
        { k: "alt_uln", label: "ALT upper limit of normal", u: "U/L", v: 40 },
        { k: "alp", label: "ALP", u: "U/L", v: 180 },
        { k: "alp_uln", label: "ALP upper limit of normal", u: "U/L", v: 130 },
        { k: "bilirubin", label: "Total bilirubin", u: "µmol/L, optional", v: 92, opt: true },
        { k: "bilirubin_uln", label: "Bilirubin upper limit of normal", u: "µmol/L, optional", v: 21, opt: true },
      ],
      outputs: [
        { k: "alt_x_uln", label: "ALT × ULN" },
        { k: "alp_x_uln", label: "ALP × ULN" },
        { k: "r_ratio", label: "R", main: true },
        { k: "pattern", label: "Pattern", main: true },
        { k: "bilirubin_x_uln", label: "Bilirubin × ULN" },
      ],
      formula: "R = (ALT / ULN) ÷ (ALP / ULN): hepatocellular if R ≥ 5, cholestatic if R ≤ 2, mixed in between.",
      book: "Worked Case 14.1: (1,240 ÷ 40) ÷ (180 ÷ 130) = 31 ÷ 1.38 ≈ 22, hepatocellular; bilirubin about 4.4 × ULN.",
      source: "Section 14.4 and Worked Case 14.1, Chapter 14",
      assumption: "Classifies the biochemical pattern only; it does not establish a cause or an interaction.",
    },
  ];

  var STRATA_INPUTS = [
    { k: "reports_00", label: "Reports, neither drug", u: "count", v: 9595900 },
    { k: "events_00", label: "Event reports, neither drug", u: "count", v: 19192 },
    { k: "reports_10", label: "Reports, drug 1 only (ravolixan)", u: "count", v: 3680 },
    { k: "events_10", label: "Event reports, drug 1 only", u: "count", v: 26 },
    { k: "reports_01", label: "Reports, drug 2 only (inhibitor)", u: "count", v: 400000 },
    { k: "events_01", label: "Event reports, drug 2 only", u: "count", v: 2800 },
    { k: "reports_11", label: "Reports, both drugs", u: "count", v: 420 },
    { k: "events_11", label: "Event reports, both drugs", u: "count", v: 21 },
  ];

  // ------------------------------------------------------------- rendering

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (key) {
        if (key === "text") node.textContent = attrs[key];
        else if (key === "className") node.className = attrs[key];
        else node.setAttribute(key, attrs[key]);
      });
    }
    (children || []).forEach(function (child) {
      if (child) node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
    });
    return node;
  }

  function sig(x, digits) {
    return Number(x.toPrecision(digits));
  }

  function formatValue(value, out) {
    if (value === null || value === undefined) return "not defined for these inputs";
    if (typeof value === "boolean") return value ? "yes" : "no";
    if (typeof value === "string") return value;
    var text;
    var unit = out.unit ? (out.unit === "%" ? "%" : " " + out.unit) : "";
    if (out.pct) {
      text = sig(value * 100, 4).toLocaleString("en-US", { maximumFractionDigits: 6 });
      unit = "%";
    } else {
      var abs = Math.abs(value);
      if (abs >= 1000) text = Math.round(value).toLocaleString("en-US");
      else if (abs === 0) text = "0";
      else text = sig(value, 4).toLocaleString("en-US", { maximumFractionDigits: 8 });
    }
    return text.replace("-", "−") + unit;
  }

  function readInputs(card, fields) {
    var values = {};
    fields.forEach(function (f) {
      var raw = f.input.value.trim();
      if (raw === "") return;
      var n = Number(raw.replace(/,/g, ""));
      values[f.k] = isNaN(n) ? raw : n;
    });
    return values;
  }

  function buildCard(card, index) {
    var fn = DDI.calculators[card.name];
    var inputs = card.inputs === "STRATA" ? STRATA_INPUTS : card.inputs;
    var id = "calc-" + card.name;

    var form = el("form", { className: "inputs", novalidate: "novalidate" });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
    });
    var fields = inputs.map(function (spec) {
      var inputId = id + "-" + spec.k;
      var input = el("input", {
        id: inputId,
        name: spec.k,
        type: "text",
        inputmode: "decimal",
        autocomplete: "off",
        spellcheck: "false",
        value: spec.v === "" ? "" : String(spec.v),
      });
      var label = el("label", { for: inputId }, [
        el("span", { className: "label-text", text: spec.label }),
        el("span", { className: "unit", text: spec.u }),
      ]);
      form.appendChild(el("div", { className: "field" + (spec.opt ? " optional" : "") }, [label, input]));
      return { k: spec.k, input: input, initial: spec.v === "" ? "" : String(spec.v) };
    });

    var results = el("div", { className: "results", "aria-live": "polite", id: id + "-results" });
    var reset = el("button", { type: "button", className: "reset", text: "Book example" });

    function update() {
      var values = readInputs(card, fields);
      results.textContent = "";
      fields.forEach(function (f) {
        f.input.removeAttribute("aria-invalid");
        f.input.removeAttribute("aria-describedby");
      });
      var result;
      try {
        result = fn(values);
      } catch (err) {
        var msgId = id + "-error";
        results.appendChild(
          el("p", { className: "error", id: msgId }, [el("strong", { text: "Check the inputs: " }), err.message])
        );
        var bad = fields.filter(function (f) {
          return new RegExp("(^|[^a-z0-9_])" + f.k + "([^a-z0-9_]|$)").test(err.message);
        });
        bad.forEach(function (f) {
          f.input.setAttribute("aria-invalid", "true");
          f.input.setAttribute("aria-describedby", msgId);
        });
        return;
      }
      var dl = el("dl");
      card.outputs.forEach(function (out) {
        if (!(out.k in result)) return;
        dl.appendChild(
          el("div", { className: "row" + (out.main ? " main" : "") }, [
            el("dt", { text: out.label }),
            el("dd", { text: formatValue(result[out.k], out) }),
          ])
        );
      });
      results.appendChild(dl);
    }

    form.addEventListener("input", update);
    reset.addEventListener("click", function () {
      fields.forEach(function (f) {
        f.input.value = f.initial;
      });
      update();
    });

    var article = el(
      "article",
      { className: "card", id: id, "data-group": card.group, "aria-labelledby": id + "-title" },
      [
        el("header", { className: "card-head" }, [
          el("h3", { id: id + "-title", text: card.title }),
          el("code", { className: "name", text: card.name }),
        ]),
        el("p", { className: "purpose", text: card.purpose }),
        card.fictional ? el("p", { className: "fictional", text: "Example uses the book's fictional ravolixan data." }) : null,
        el("div", { className: "body" }, [
          el("div", { className: "col" }, [form, reset]),
          el("div", { className: "col" }, [el("h4", { text: "Result" }), results]),
        ]),
        el("dl", { className: "meta" }, [
          el("div", {}, [el("dt", { text: "Formula" }), el("dd", { text: card.formula })]),
          el("div", {}, [el("dt", { text: "Book's worked numbers" }), el("dd", { text: card.book })]),
          el("div", { className: "assumption" }, [el("dt", { text: "Main assumption" }), el("dd", { text: card.assumption })]),
          el("div", {}, [el("dt", { text: "Source" }), el("dd", { text: card.source })]),
        ]),
      ]
    );
    update();
    return article;
  }

  function build() {
    var main = document.getElementById("calculators");
    var toc = document.getElementById("toc-list");
    GROUPS.forEach(function (group) {
      var cards = CARDS.filter(function (c) {
        return c.group === group.id;
      });
      var section = el("section", { className: "group", id: "group-" + group.id, "aria-labelledby": "h-" + group.id }, [
        el("h2", { id: "h-" + group.id, text: group.title }),
      ]);
      var sub = el("ul");
      cards.forEach(function (card, i) {
        section.appendChild(buildCard(card, i));
        sub.appendChild(el("li", { "data-calc": card.name }, [el("a", { href: "#calc-" + card.name, text: card.title })]));
      });
      main.appendChild(section);
      toc.appendChild(el("li", { "data-group": group.id }, [el("a", { href: "#group-" + group.id, text: group.title }), sub]));
    });

    var filter = document.getElementById("filter");
    var status = document.getElementById("filter-status");
    filter.addEventListener("input", function () {
      var q = filter.value.trim().toLowerCase();
      var shown = 0;
      CARDS.forEach(function (card) {
        var hay = [card.title, card.name, card.purpose, card.source, card.group].join(" ").toLowerCase();
        var match = q === "" || hay.indexOf(q) !== -1;
        document.getElementById("calc-" + card.name).hidden = !match;
        var li = toc.querySelector('[data-calc="' + card.name + '"]');
        if (li) li.hidden = !match;
        if (match) shown += 1;
      });
      GROUPS.forEach(function (group) {
        var section = document.getElementById("group-" + group.id);
        var any = section.querySelector(".card:not([hidden])");
        section.hidden = !any;
        toc.querySelector('[data-group="' + group.id + '"]').hidden = !any;
      });
      status.textContent = q === "" ? "" : shown + " of " + CARDS.length + " calculators shown";
    });
  }

  if (!DDI) {
    document.getElementById("calculators").textContent = "calculators.js did not load.";
    return;
  }
  build();
})();
