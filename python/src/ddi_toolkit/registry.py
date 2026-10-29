"""The list of calculators, with book sources and main assumptions.

Calculator names are snake_case and identical in the Python package, the
command-line interface, ``spec/vectors.json``, and the JavaScript port.

Educational use only: the calculators teach the reasoning in the book with
simplified static models and must not be used for dosing or clinical decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from . import disproportionality, epi, liver, pk, qt, timing


@dataclass(frozen=True)
class Calculator:
    name: str
    func: Callable[..., dict]
    source: str
    assumption: str

    @property
    def summary(self) -> str:
        doc = (self.func.__doc__ or "").strip()
        return doc.splitlines()[0] if doc else self.name


_ENTRIES = [
    Calculator(
        "auc_ratio_inhibition", pk.auc_ratio_inhibition,
        "Calculation 1.1, Chapter 1; Calculation 5.1, Chapter 5",
        "Linear pharmacokinetics and one inhibited pathway; ignores transporters, "
        "metabolites, and individual variability.",
    ),
    Calculator(
        "fm_ceiling", pk.fm_ceiling,
        "Calculation 5.1, Chapter 5; Calculation 19.1, Chapter 19; Calculation 23.1, Chapter 23",
        "Complete blockade of one pathway of systemic clearance; no gut-wall or transporter effect.",
    ),
    Calculator(
        "inhibition_from_auc_ratio", pk.inhibition_from_auc_ratio,
        "Calculation 23.1, Chapter 23",
        "Linear pharmacokinetics; the whole AUC change comes from the one pathway with share fm.",
    ),
    Calculator(
        "induction_auc_ratio", pk.induction_auc_ratio,
        "Calculation 5.2, Chapter 5; Calculation 10.1, Chapter 10",
        "Linear kinetics; only the named pathway (and bioavailability, if given) changes.",
    ),
    Calculator(
        "clearance_pathways", pk.clearance_pathways,
        "Calculation 2.1, Chapter 2; Calculation 6.2, Chapter 6",
        "AUC inversely proportional to clearance; renal routes scale with renal function; "
        "shares are illustrative.",
    ),
    Calculator(
        "protein_binding_displacement", pk.protein_binding_displacement,
        "Calculation 6.1, Chapter 6",
        "Low-extraction oral drug at steady state; average concentrations only; "
        "ignores the transient rise after displacement.",
    ),
    Calculator(
        "dose_adjusted_exposure", pk.dose_adjusted_exposure,
        "Calculation 23.1, Chapter 23; Calculation 19.2, Chapter 19",
        "Exposure proportional to dose (linear pharmacokinetics); average exposure only; not a dose.",
    ),
    Calculator(
        "auc_mic", pk.auc_mic,
        "Calculation 4.1, Chapter 4",
        "Linear pharmacokinetics, every dose affected equally, total drug; "
        "the target of 125 is illustrative, not validated.",
    ),
    Calculator(
        "time_to_steady_state", timing.time_to_steady_state,
        "Section 8.2 and Calculation 8.1, Chapter 8; Calculation 21.2, Chapter 21",
        "First-order elimination, volume unchanged, precipitant effect constant from the start.",
    ),
    Calculator(
        "exposure_rise_after_inhibition", timing.exposure_rise_after_inhibition,
        "Calculation 25.1, Chapter 25",
        "Inhibition fully established at the start time; linear kinetics; volume unchanged.",
    ),
    Calculator(
        "residual_inhibition", timing.residual_inhibition,
        "Calculation 8.2, Chapter 8",
        "First-order elimination of a competitive, reversible inhibitor; ignores active metabolites.",
    ),
    Calculator(
        "de_induction_remaining", timing.de_induction_remaining,
        "Calculation 5.2, Chapter 5; Calculation 8.3, Chapter 8; Calculation 21.1, Chapter 21",
        "Inducer eliminated quickly; induced excess decays as a single exponential; "
        "turnover half-lives are uncertain, so state a range.",
    ),
    Calculator(
        "washout", timing.washout,
        "Section 21.3 and Calculation 21.1, Chapter 21",
        "Single-exponential recovery; probe-based recovery estimates assumed to apply to the object drug.",
    ),
    Calculator(
        "qt_correction", qt.qt_correction,
        "Calculation 7.1, Chapter 7",
        "Bazett overcorrects at fast heart rates; record the formula, heart rate, and measurement method.",
    ),
    Calculator(
        "exposure_qtc_line", qt.exposure_qtc_line,
        "Calculation 19.2, Chapter 19; Calculation 25.1, Chapter 25",
        "A straight line through two means, not a fitted model; averages, not individuals.",
    ),
    Calculator(
        "absolute_risk", epi.absolute_risk,
        "Calculation 9.1, Chapter 9",
        "Relative effect constant across baseline risk (a simplification); not causation in an individual.",
    ),
    Calculator(
        "reporting_rate", epi.reporting_rate,
        "Calculation 17.1, Chapter 17; Calculation 20.1, Chapter 20; Calculation 22.1, Chapter 22",
        "A reporting rate, not an incidence: it depends on under-reporting and case definition.",
    ),
    Calculator(
        "co_exposure_sensitivity", epi.co_exposure_sensitivity,
        "Calculation 17.1, Chapter 17; Calculation 20.1, Chapter 20; Calculation 22.1, Chapter 22",
        "The co-exposure fraction is an assumption, and reporting is assumed equally complete in both groups.",
    ),
    Calculator(
        "proportion_ratio", epi.proportion_ratio,
        "Calculation 24.1, Chapter 24",
        "Groups treated as independent samples; a two-period comparison cannot exclude a pre-existing trend.",
    ),
    Calculator(
        "rule_of_three", epi.rule_of_three,
        "Section 19.4, Chapter 19; Section 26.2, Chapter 26",
        "Zero events observed; the bound applies only to the conditions studied.",
    ),
    Calculator(
        "prr_ror", disproportionality.prr_ror,
        "Section 18.1 and Calculations 18.1 and 18.2, Chapter 18",
        "Describes how reports are distributed, not risk; a threshold is a filter for review, not a finding.",
    ),
    Calculator(
        "information_component", disproportionality.information_component,
        "Section 18.1 and Calculation 18.1, Chapter 18",
        "Describes reporting, not risk; the 0.5 shrinkage is a convention.",
    ),
    Calculator(
        "four_stratum_expectations", disproportionality.four_stratum_expectations,
        "Section 18.2 and Calculation 18.3, Chapter 18",
        "Two models of no interaction; describes reporting, not risk, and inherits confounding and reporting bias.",
    ),
    Calculator(
        "omega_shrinkage", disproportionality.omega_shrinkage,
        "Section 18.2 and Calculations 18.3 and 18.4, Chapter 18",
        "Additive baseline on the odds scale with 0.5 shrinkage; with sparse counts report counts and interval.",
    ),
    Calculator(
        "liver_injury_r_ratio", liver.liver_injury_r_ratio,
        "Section 14.4 and Worked Case 14.1 (Section 14.5), Chapter 14",
        "Classifies the biochemical pattern only; it does not establish a cause or an interaction.",
    ),
]

CALCULATORS: Dict[str, Calculator] = {c.name: c for c in _ENTRIES}

CAVEAT = (
    "Educational use only: simplified static models from the book; "
    "not for dosing or clinical decisions."
)

PARAM_HELP: Dict[str, str] = {
    "fm": "fraction of the object drug's clearance through the affected pathway (0 to 1)",
    "fraction_inhibited": "fraction of the pathway inhibited, I (0 to 1)",
    "i_over_ki": "inhibitor concentration relative to its inhibition constant, [I]/Ki (0 or more)",
    "fg_before": "fraction escaping gut-wall metabolism without the inhibitor (0 to 1)",
    "fg_after": "fraction escaping gut-wall metabolism with the inhibitor (0 to 1)",
    "auc_ratio": "AUC with the precipitant / AUC without",
    "activity_multiplier": "factor by which the pathway's activity is multiplied (1 or more)",
    "bioavailability_before": "oral bioavailability before the change (0 to 1)",
    "bioavailability_after": "oral bioavailability after the change (0 to 1)",
    "baseline_concentration": "concentration before the change (any unit), to scale",
    "nonrenal_fraction": "share of clearance by non-renal (e.g. hepatic) routes at normal renal function",
    "renal_fraction": "share of clearance by renal routes the precipitant does not affect (e.g. filtration)",
    "secretion_fraction": "share of clearance by active tubular secretion",
    "nonrenal_inhibition": "fraction of the non-renal route removed by the precipitant (0 to 1)",
    "secretion_inhibition": "fraction of secretion removed by the precipitant (0 to 1)",
    "renal_function": "renal function as a fraction of normal (1 = normal)",
    "dose_rate": "dose rate, e.g. mg/day",
    "fu": "unbound fraction at baseline (0 to 1)",
    "clu": "clearance of unbound drug at baseline, e.g. L/day",
    "fu_new": "unbound fraction with the precipitant (default: unchanged)",
    "clu_new": "clearance of unbound drug with the precipitant (default: unchanged)",
    "dose": "new dose",
    "reference_dose": "usual dose, in the same unit",
    "single_dose_auc": "single-dose AUC, mg·h/L",
    "doses_per_day": "number of doses per day",
    "mic": "minimum inhibitory concentration, mg/L",
    "target": "illustrative AUC/MIC target (the book uses 125)",
    "half_life": "half-life (hours or days; use the same unit for all times)",
    "n_half_lives": "number of half-lives",
    "clearance_ratio": "new clearance / old clearance (e.g. 0.6 for a 40% fall)",
    "time_since_start": "time since the inhibitor's effect began (same unit as half_life)",
    "i_over_ki_at_stop": "[I]/Ki when the inhibitor is stopped",
    "time": "time since stopping (same unit as half_life)",
    "induced_auc_ratio": "AUC with the inducer / without (0 to 1), e.g. 0.18",
    "recovery_half_life": "recovery (turnover) half-life",
    "elimination_lag": "time for the precipitant itself to be eliminated before recovery starts",
    "washout_duration": "washout length to evaluate (same unit)",
    "qt": "measured QT interval, ms",
    "heart_rate": "heart rate, beats per minute",
    "multiple_1": "first anchor: multiple of therapeutic exposure",
    "dqtc_1": "first anchor: mean ΔQTc, ms",
    "multiple_2": "second anchor: multiple of therapeutic exposure",
    "dqtc_2": "second anchor: mean ΔQTc, ms",
    "multiple": "multiple of therapeutic exposure to read off the line",
    "baseline_risk": "baseline risk as a proportion (0.005 for 0.5%)",
    "relative_risk": "relative risk (multiplier)",
    "cases": "number of cases",
    "exposure": "exposure, e.g. patient-years",
    "per": "rate denominator (e.g. 100000 or 1000)",
    "cases_with": "cases with the co-medication",
    "cases_without": "cases without the co-medication",
    "total_exposure": "total exposure, e.g. patient-years",
    "co_exposure_fraction": "assumed fraction of exposure with the co-medication (0 to 1)",
    "events_1": "events in group 1 (reference, e.g. before)",
    "total_1": "total in group 1",
    "events_2": "events in group 2 (comparison, e.g. after)",
    "total_2": "total in group 2",
    "n": "number of patients with no events",
    "a": "drug of interest, event of interest",
    "b": "drug of interest, all other events",
    "c": "all other drugs, event of interest",
    "d": "all other drugs, all other events",
    "reports_00": "reports with neither drug",
    "events_00": "event reports with neither drug",
    "reports_10": "reports with drug 1 only",
    "events_10": "event reports with drug 1 only",
    "reports_01": "reports with drug 2 only",
    "events_01": "event reports with drug 2 only",
    "reports_11": "reports with both drugs",
    "events_11": "event reports with both drugs",
    "alt": "ALT (any unit)",
    "alt_uln": "ALT upper limit of normal (same unit)",
    "alp": "ALP (any unit)",
    "alp_uln": "ALP upper limit of normal (same unit)",
    "bilirubin": "total bilirubin (any unit)",
    "bilirubin_uln": "bilirubin upper limit of normal (same unit)",
}


def get(name: str) -> Calculator:
    """Return the calculator called ``name`` or raise KeyError with the valid names."""
    try:
        return CALCULATORS[name]
    except KeyError:
        raise KeyError(f"unknown calculator {name!r}; valid names: {', '.join(CALCULATORS)}") from None
