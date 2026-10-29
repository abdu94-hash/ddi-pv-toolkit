"""Exposure calculators: AUC ratios, clearance pathways, binding, dose, AUC/MIC.

Sources: Calculations 1.1, 2.1, 4.1, 5.1, 5.2, 6.1, 6.2, 10.1, 19.1 and 23.1 of
*Drug–Drug Interactions in Drug Safety and Pharmacovigilance*.

Educational use only. These functions reproduce the simplified static models
worked through in the book (linear pharmacokinetics, AUC inversely proportional
to clearance, named pathways only). They teach the reasoning; they do not
predict what happens in an individual, an AUC ratio is not a dose instruction,
and nothing here may be used for dosing or any other clinical decision.
"""

from __future__ import annotations

import math
from typing import Dict, Optional, Union

from . import _validate as v

Result = Dict[str, Union[float, bool, str, None]]


def auc_ratio_inhibition(
    fm: float,
    fraction_inhibited: Optional[float] = None,
    i_over_ki: Optional[float] = None,
    fg_before: Optional[float] = None,
    fg_after: Optional[float] = None,
) -> Result:
    """AUC ratio of the object drug when one clearance pathway is inhibited.

    Calculation 1.1 (Chapter 1): AUC ratio ≈ 1 / (1 − fm × I), with an optional
    gut-wall term: when inhibition in the gut wall raises the fraction escaping
    gut metabolism from ``fg_before`` to ``fg_after``, bioavailability rises by
    fg_after / fg_before and the effects multiply.

    Calculation 5.1 (Chapter 5): for reversible inhibition,
    AUCR = 1 / (fm / (1 + [I]/Ki) + (1 − fm)), which is the same equation with
    I = ([I]/Ki) / (1 + [I]/Ki).

    Give exactly one of ``fraction_inhibited`` (I, 0 to 1) or ``i_over_ki``
    ([I]/Ki, 0 or more).

    Assumes linear pharmacokinetics and a single inhibited pathway; ignores
    transporters, active metabolites, and variability between individuals.
    """
    fm = v.fraction("fm", fm)
    if (fraction_inhibited is None) == (i_over_ki is None):
        raise ValueError("give exactly one of fraction_inhibited or i_over_ki")
    if i_over_ki is not None:
        ratio = v.nonnegative("i_over_ki", i_over_ki)
        inhibited = ratio / (1.0 + ratio)
    else:
        inhibited = v.fraction("fraction_inhibited", fraction_inhibited)
    remaining = 1.0 - fm * inhibited
    if remaining <= 0:
        raise ValueError(
            "fm = 1 with complete inhibition leaves no clearance: the AUC ratio is unbounded"
        )
    gut_factor = 1.0
    if v.optional_pair("fg_before", fg_before, "fg_after", fg_after):
        before = v.fraction("fg_before", fg_before, allow_zero=False)
        after = v.fraction("fg_after", fg_after, allow_zero=False)
        gut_factor = after / before
    systemic = 1.0 / remaining
    return {
        "fraction_inhibited": inhibited,
        "remaining_clearance": remaining,
        "auc_ratio_systemic": systemic,
        "gut_factor": gut_factor,
        "auc_ratio": systemic * gut_factor,
    }


def fm_ceiling(fm: float) -> Result:
    """Largest AUC ratio that complete inhibition of one pathway can produce.

    Calculation 5.1 (Chapter 5) and Calculation 19.1 (Chapter 19): with complete
    blockade, AUC ratio = 1 / (1 − fm). With fm = 0.20 no inhibitor of that
    pathway raises exposure more than about 25%.

    Assumes linear pharmacokinetics and that the inhibitor affects only this
    pathway of systemic clearance (no gut-wall or transporter effect).
    """
    fm = v.fraction("fm", fm, allow_one=False)
    ceiling = 1.0 / (1.0 - fm)
    return {
        "remaining_clearance": 1.0 - fm,
        "auc_ratio_max": ceiling,
        "max_increase_percent": (ceiling - 1.0) * 100.0,
    }


def inhibition_from_auc_ratio(fm: float, auc_ratio: float) -> Result:
    """Fraction of a pathway that must be inhibited to give an observed AUC ratio.

    Calculation 23.1 (Chapter 23) runs Calculation 1.1 in reverse: an AUC ratio
    of 2.0 with fm = 0.75 corresponds to inhibiting about two-thirds of the
    pathway, 1 / (0.75 × 0.33 + 0.25) ≈ 2.0. Rearranged,
    I = (1 − 1 / AUC ratio) / fm.

    An AUC ratio above the fm ceiling 1 / (1 − fm) cannot come from this
    pathway alone (the book's reading of itraconazole, 4.2 against a ceiling of
    4.0), so it is rejected with an explanation.
    """
    fm = v.fraction("fm", fm, allow_zero=False)
    auc_ratio = v.at_least("auc_ratio", auc_ratio, 1.0)
    ceiling = math.inf if fm == 1 else 1.0 / (1.0 - fm)
    if auc_ratio > ceiling:
        raise ValueError(
            f"auc_ratio {auc_ratio:g} exceeds the ceiling 1 / (1 - fm) = {ceiling:.3g} "
            f"for fm = {fm:g}; the excess cannot come from this pathway alone "
            "(for example, gut-wall or transporter inhibition; Calculation 23.1)"
        )
    inhibited = (1.0 - 1.0 / auc_ratio) / fm
    return {
        "fraction_inhibited": inhibited,
        "remaining_pathway_activity": 1.0 - inhibited,
        "auc_ratio_max": None if math.isinf(ceiling) else ceiling,
    }


def induction_auc_ratio(
    fm: float,
    activity_multiplier: float,
    bioavailability_before: Optional[float] = None,
    bioavailability_after: Optional[float] = None,
    baseline_concentration: Optional[float] = None,
) -> Result:
    """AUC ratio when one pathway's activity is multiplied (induction or recovery).

    Calculation 5.2 (Chapter 5): relative clearance = fm × multiplier + (1 − fm);
    the systemic contribution to the AUC ratio is 1 / relative clearance, and a
    change in bioavailability multiplies it (0.50 to 0.25 gives a factor 0.50).

    Calculation 10.1 (Chapter 10) applies the same arithmetic to relief of
    IL-6-mediated CYP3A4 suppression: with fm 0.90 and an 80% rise in activity,
    clearance becomes 1.72 and a trough of 100 ng/mL falls to about 58 ng/mL at
    the same dose. Give ``baseline_concentration`` to get that last step.

    ``activity_multiplier`` must be at least 1; for reduced activity use
    ``auc_ratio_inhibition``. Assumes linear kinetics and no other changes.
    """
    fm = v.fraction("fm", fm)
    k = v.at_least("activity_multiplier", activity_multiplier, 1.0)
    f_ratio = 1.0
    if v.optional_pair(
        "bioavailability_before", bioavailability_before,
        "bioavailability_after", bioavailability_after,
    ):
        before = v.fraction("bioavailability_before", bioavailability_before, allow_zero=False)
        after = v.fraction("bioavailability_after", bioavailability_after, allow_zero=False)
        f_ratio = after / before
    relative_clearance = fm * k + (1.0 - fm)
    systemic = 1.0 / relative_clearance
    auc_ratio = systemic * f_ratio
    out: Result = {
        "relative_clearance": relative_clearance,
        "auc_ratio_systemic": systemic,
        "bioavailability_ratio": f_ratio,
        "auc_ratio": auc_ratio,
        "percent_change": (auc_ratio - 1.0) * 100.0,
    }
    if baseline_concentration is not None:
        c0 = v.nonnegative("baseline_concentration", baseline_concentration)
        out["concentration_after"] = c0 * auc_ratio
    return out


def clearance_pathways(
    nonrenal_fraction: float,
    renal_fraction: float,
    secretion_fraction: float = 0.0,
    nonrenal_inhibition: float = 0.0,
    secretion_inhibition: float = 0.0,
    renal_function: float = 1.0,
) -> Result:
    """Clearance-pathway arithmetic with inhibition and impaired renal function.

    Calculation 2.1 (Chapter 2) and Calculation 6.2 (Chapter 6). Write down the
    routes and their shares at normal renal function (they must sum to 1):

    * ``nonrenal_fraction``: hepatic or other non-renal routes;
    * ``renal_fraction``: renal clearance the precipitant does not affect
      (filtration in Calculation 6.2; the whole renal route in Calculation 2.1);
    * ``secretion_fraction``: active tubular secretion.

    The precipitant removes ``nonrenal_inhibition`` of the non-renal route and
    ``secretion_inhibition`` of secretion. Renal routes scale with
    ``renal_function`` (1 = normal, 0.4 = 40% of normal). AUC is inversely
    proportional to clearance (linear kinetics).

    Returns the AUC ratio against the patient's own baseline and against a
    person with normal renal function taking the drug alone.
    """
    fn = v.fraction("nonrenal_fraction", nonrenal_fraction)
    fr = v.fraction("renal_fraction", renal_fraction)
    fs = v.fraction("secretion_fraction", secretion_fraction)
    if abs(fn + fr + fs - 1.0) > 1e-6:
        raise ValueError(
            "nonrenal_fraction + renal_fraction + secretion_fraction must sum to 1, "
            f"got {fn + fr + fs:g}"
        )
    i_n = v.fraction("nonrenal_inhibition", nonrenal_inhibition)
    i_s = v.fraction("secretion_inhibition", secretion_inhibition)
    rf = v.fraction("renal_function", renal_function, allow_zero=False)
    baseline = fn + rf * (fr + fs)
    inhibited = fn * (1.0 - i_n) + rf * (fr + fs * (1.0 - i_s))
    if inhibited <= 0:
        raise ValueError("no clearance remains with these inputs: the AUC ratio is unbounded")
    return {
        "baseline_clearance": baseline,
        "inhibited_clearance": inhibited,
        "impairment_alone_ratio": 1.0 / baseline,
        "auc_ratio_vs_own_baseline": baseline / inhibited,
        "auc_ratio_vs_normal_alone": 1.0 / inhibited,
    }


def protein_binding_displacement(
    dose_rate: float,
    fu: float,
    clu: float,
    fu_new: Optional[float] = None,
    clu_new: Optional[float] = None,
) -> Result:
    """Average steady-state total and unbound concentrations before and after displacement.

    Calculation 6.1 (Chapter 6): for a low-extraction oral drug with complete
    bioavailability, total clearance = fu × CLu, total concentration =
    dose rate / total clearance, and unbound concentration = fu × total.
    Displacement alone (fu rises, CLu unchanged) lowers total concentration and
    leaves unbound concentration unchanged; only a fall in CLu raises unbound
    exposure.

    Units: ``dose_rate`` in mass per time (e.g. mg/day) and ``clu`` in volume
    per the same time (e.g. L/day) give concentrations in mass per volume.
    Does not cover the transient rise just after displacement, high-extraction
    drugs given intravenously, or changes in distribution volume.
    """
    dose = v.positive("dose_rate", dose_rate)
    fu0 = v.fraction("fu", fu, allow_zero=False)
    clu0 = v.positive("clu", clu)
    fu1 = fu0 if fu_new is None else v.fraction("fu_new", fu_new, allow_zero=False)
    clu1 = clu0 if clu_new is None else v.positive("clu_new", clu_new)
    cl0, cl1 = fu0 * clu0, fu1 * clu1
    c0, c1 = dose / cl0, dose / cl1
    cu0, cu1 = fu0 * c0, fu1 * c1
    return {
        "total_clearance": cl0,
        "total_concentration": c0,
        "unbound_concentration": cu0,
        "total_clearance_new": cl1,
        "total_concentration_new": c1,
        "unbound_concentration_new": cu1,
        "total_concentration_change": c1 / c0 - 1.0,
        "unbound_concentration_ratio": cu1 / cu0,
    }


def dose_adjusted_exposure(auc_ratio: float, dose: float, reference_dose: float) -> Result:
    """Average exposure relative to the usual dose alone after a dose change.

    Calculation 23.1 (Chapter 23) and Calculation 19.2, Step 5 (Chapter 19):
    exposure relative to the reference dose alone = (dose / reference dose) ×
    AUC ratio. Halving ravolixan to 20 mg with diltiazem (AUC ratio 2.0) gives
    1.0; with itraconazole (4.2) it gives 2.1.

    Assumes linear pharmacokinetics (exposure proportional to dose). Describes
    average exposure only; does not set a dose.
    """
    r = v.positive("auc_ratio", auc_ratio)
    d = v.positive("dose", dose)
    d0 = v.positive("reference_dose", reference_dose)
    return {"dose_fraction": d / d0, "relative_exposure": (d / d0) * r}


def auc_mic(
    single_dose_auc: float,
    doses_per_day: float,
    mic: float,
    target: Optional[float] = None,
) -> Result:
    """24-hour AUC/MIC from a single-dose AUC, compared with an illustrative target.

    Calculation 4.1 (Chapter 4): under linear pharmacokinetics the 24-hour AUC
    at steady state ≈ doses per day × single-dose AUC, and AUC/MIC = that AUC
    divided by the organism's MIC. The book's target of 125 is illustrative,
    not a validated target for any infection, so ``target`` is optional.

    Units: AUC in mg·h/L and MIC in mg/L. Uses total, not free, drug; assumes
    every dose is affected equally; predicts a probability of response in a
    population, not the outcome in one patient.
    """
    auc = v.positive("single_dose_auc", single_dose_auc)
    n = v.positive("doses_per_day", doses_per_day)
    m = v.positive("mic", mic)
    auc24 = n * auc
    out: Result = {"auc_24h": auc24, "auc_mic": auc24 / m}
    if target is not None:
        t = v.positive("target", target)
        out["target_ratio"] = auc24 / m / t
        out["meets_target"] = auc24 / m >= t
    return out
