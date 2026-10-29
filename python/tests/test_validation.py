"""Targeted tests: input validation and behavior the vectors do not cover."""

import math

import pytest

import ddi_toolkit as dt
from ddi_toolkit._gamma import gamma_cdf, gamma_quantile
from ddi_toolkit.registry import CALCULATORS


@pytest.mark.parametrize(
    "func, kwargs, message",
    [
        (dt.auc_ratio_inhibition, {"fm": 1.2, "fraction_inhibited": 0.5}, "fm"),
        (dt.auc_ratio_inhibition, {"fm": 0.5}, "exactly one"),
        (dt.auc_ratio_inhibition, {"fm": 0.5, "fraction_inhibited": 0.5, "i_over_ki": 1}, "exactly one"),
        (dt.auc_ratio_inhibition, {"fm": 1, "fraction_inhibited": 1}, "unbounded"),
        (dt.auc_ratio_inhibition, {"fm": 0.5, "i_over_ki": -1}, "i_over_ki"),
        (dt.auc_ratio_inhibition, {"fm": 0.5, "fraction_inhibited": 0.5, "fg_before": 0.3}, "both"),
        (dt.auc_ratio_inhibition, {"fm": 0.5, "fraction_inhibited": 0.5, "fg_before": 0, "fg_after": 0.9}, "fg_before"),
        (dt.fm_ceiling, {"fm": 1}, "fm"),
        (dt.inhibition_from_auc_ratio, {"fm": 0.75, "auc_ratio": 4.2}, "exceeds the ceiling"),
        (dt.inhibition_from_auc_ratio, {"fm": 0.75, "auc_ratio": 0.5}, "auc_ratio"),
        (dt.induction_auc_ratio, {"fm": 0.7, "activity_multiplier": 0.5}, "activity_multiplier"),
        (dt.clearance_pathways, {"nonrenal_fraction": 0.6, "renal_fraction": 0.6}, "sum to 1"),
        (dt.clearance_pathways, {"nonrenal_fraction": 0.6, "renal_fraction": 0.4, "renal_function": 0}, "renal_function"),
        (dt.clearance_pathways, {"nonrenal_fraction": 1, "renal_fraction": 0, "nonrenal_inhibition": 1}, "unbounded"),
        (dt.protein_binding_displacement, {"dose_rate": 400, "fu": 0, "clu": 100}, "fu"),
        (dt.protein_binding_displacement, {"dose_rate": -1, "fu": 0.4, "clu": 100}, "dose_rate"),
        (dt.dose_adjusted_exposure, {"auc_ratio": 2, "dose": 0, "reference_dose": 40}, "dose"),
        (dt.auc_mic, {"single_dose_auc": 14.5, "doses_per_day": 2, "mic": 0}, "mic"),
        (dt.time_to_steady_state, {"half_life": 40, "clearance_ratio": 0.6, "auc_ratio": 1.7}, "not both"),
        (dt.time_to_steady_state, {"half_life": 0}, "half_life"),
        (dt.exposure_rise_after_inhibition,
         {"auc_ratio": 3.9, "bioavailability_before": 0.6, "bioavailability_after": 1.2, "half_life": 14, "time_since_start": 58},
         "bioavailability_after"),
        (dt.residual_inhibition, {"half_life": 50, "i_over_ki_at_stop": 4, "time": -1}, "time"),
        (dt.de_induction_remaining, {"half_life": 8, "time": 28, "induced_auc_ratio": 1.5}, "induced_auc_ratio"),
        (dt.washout, {"recovery_half_life": 2.3, "elimination_lag": -1}, "elimination_lag"),
        (dt.qt_correction, {"qt": 4.8, "heart_rate": 0}, "heart_rate"),
        (dt.qt_correction, {"qt": 4800, "heart_rate": 90}, "milliseconds"),
        (dt.exposure_qtc_line, {"multiple_1": 1, "dqtc_1": 6, "multiple_2": 1, "dqtc_2": 18, "multiple": 2}, "differ"),
        (dt.absolute_risk, {"baseline_risk": 0.5, "relative_risk": 3}, "exceeds 1"),
        (dt.absolute_risk, {"baseline_risk": 5, "relative_risk": 1.6}, "baseline_risk"),
        (dt.reporting_rate, {"cases": 4.5, "exposure": 1000}, "whole number"),
        (dt.reporting_rate, {"cases": 47, "exposure": 0}, "exposure"),
        (dt.co_exposure_sensitivity,
         {"cases_with": 21, "cases_without": 26, "total_exposure": 180000, "co_exposure_fraction": 1}, "co_exposure_fraction"),
        (dt.proportion_ratio, {"events_1": 200, "total_1": 100, "events_2": 1, "total_2": 100}, "cannot exceed"),
        (dt.rule_of_three, {"n": 0}, "at least 1"),
        (dt.prr_ror, {"a": 0, "b": 1, "c": 1, "d": 1}, "a must be at least 1"),
        (dt.information_component, {"a": 1, "b": 0, "c": 1, "d": 1}, "b must be at least 1"),
        (dt.four_stratum_expectations,
         {"reports_00": 10, "events_00": 11, "reports_10": 10, "events_10": 1,
          "reports_01": 10, "events_01": 1, "reports_11": 10, "events_11": 1}, "cannot exceed"),
        (dt.omega_shrinkage,
         {"reports_00": 0, "events_00": 0, "reports_10": 10, "events_10": 1,
          "reports_01": 10, "events_01": 1, "reports_11": 10, "events_11": 1}, "reports_00"),
        (dt.liver_injury_r_ratio, {"alt": 1240, "alt_uln": 0, "alp": 180, "alp_uln": 130}, "alt_uln"),
    ],
)
def test_invalid_inputs_raise_value_error(func, kwargs, message):
    with pytest.raises(ValueError, match=message):
        func(**kwargs)


@pytest.mark.parametrize("bad", ["0.5", None, True, float("nan"), float("inf")])
def test_non_numbers_rejected(bad):
    with pytest.raises(ValueError):
        dt.fm_ceiling(fm=bad)


def test_i_over_ki_equals_fraction_form():
    # Calculation 5.1: [I]/Ki = 1 is the same as inhibiting half the pathway.
    a = dt.auc_ratio_inhibition(fm=0.9, i_over_ki=1)["auc_ratio"]
    b = dt.auc_ratio_inhibition(fm=0.9, fraction_inhibited=0.5)["auc_ratio"]
    assert a == pytest.approx(b)


def test_inverse_round_trip():
    i = dt.inhibition_from_auc_ratio(fm=0.75, auc_ratio=2.0)["fraction_inhibited"]
    assert dt.auc_ratio_inhibition(fm=0.75, fraction_inhibited=i)["auc_ratio"] == pytest.approx(2.0)


def test_itraconazole_exceeds_ceiling_message_explains():
    # Calculation 23.1: 4.2 is above the ceiling of 4.0 for fm 0.75.
    with pytest.raises(ValueError) as err:
        dt.inhibition_from_auc_ratio(fm=0.75, auc_ratio=4.2)
    assert "4" in str(err.value) and "pathway alone" in str(err.value)


def test_displacement_alone_leaves_unbound_unchanged():
    r = dt.protein_binding_displacement(dose_rate=400, fu=0.4, clu=100, fu_new=0.9)
    assert r["unbound_concentration_ratio"] == pytest.approx(1.0)


def test_bazett_and_fridericia_agree_at_60():
    r = dt.qt_correction(qt=430, heart_rate=60)
    assert r["qtc_bazett"] == pytest.approx(430) and r["qtc_fridericia"] == pytest.approx(430)


def test_bazett_longer_at_fast_rates():
    r = dt.qt_correction(qt=400, heart_rate=110)
    assert r["qtc_bazett"] > r["qtc_fridericia"]


def test_exposure_qtc_line_flags_extrapolation():
    base = {"multiple_1": 1, "dqtc_1": 6, "multiple_2": 4, "dqtc_2": 18}
    assert dt.exposure_qtc_line(multiple=4.2, **base)["extrapolated"] is True
    assert dt.exposure_qtc_line(multiple=2.1, **base)["extrapolated"] is False


@pytest.mark.parametrize("alt, alp, pattern", [(1240, 180, "hepatocellular"), (80, 260, "cholestatic"), (300, 260, "mixed")])
def test_r_ratio_patterns(alt, alp, pattern):
    r = dt.liver_injury_r_ratio(alt=alt, alt_uln=40, alp=alp, alp_uln=130)
    assert r["pattern"] == pattern


def test_r_ratio_boundaries():
    # Hepatocellular when R is 5 or more; cholestatic when R is 2 or less.
    assert dt.liver_injury_r_ratio(alt=5, alt_uln=1, alp=1, alp_uln=1)["pattern"] == "hepatocellular"
    assert dt.liver_injury_r_ratio(alt=2, alt_uln=1, alp=1, alp_uln=1)["pattern"] == "cholestatic"


def test_absolute_risk_no_excess_gives_no_nnh():
    assert dt.absolute_risk(baseline_risk=0.05, relative_risk=1.0)["number_needed_to_harm"] is None


def test_omega_with_zero_observed():
    r = dt.omega_shrinkage(
        reports_00=9595900, events_00=19192, reports_10=3680, events_10=26,
        reports_01=80000, events_01=200, reports_11=60, events_11=0,
    )
    assert r["omega"] < 0
    assert r["omega025_normal"] is None and r["unshrunk_log2_ratio"] is None
    assert math.isfinite(r["omega025_gamma"])


def test_omega_max_terms_ignore_apparent_protection():
    # Step 2: a drug that appears protective must not lower the expectation.
    r = dt.omega_shrinkage(
        reports_00=10000, events_00=100, reports_10=1000, events_10=1,
        reports_01=1000, events_01=10, reports_11=100, events_11=2,
    )
    g00 = 100 / 9900
    assert r["expected_odds"] == pytest.approx(g00)


def test_washout_before_lag_leaves_full_effect():
    r = dt.washout(recovery_half_life=2.3, elimination_lag=2, washout_duration=1)
    assert r["fraction_remaining_at_washout"] == 1.0


def test_gamma_quantile_inverts_cdf():
    for shape in (0.5, 3.5, 21.5, 47.5, 200.5):
        for p in (0.025, 0.5, 0.975):
            assert gamma_cdf(gamma_quantile(p, shape), shape) == pytest.approx(p, abs=1e-10)


def test_every_calculator_is_exported_and_documented():
    for name, calc in CALCULATORS.items():
        assert getattr(dt, name) is calc.func
        doc = calc.func.__doc__ or ""
        assert "Calculation" in doc or "Section" in doc, name
        module_doc = " ".join(__import__(calc.func.__module__, fromlist=["_"]).__doc__.split())
        assert "Educational use only" in module_doc and "clinical decision" in module_doc
