"""Timing calculators: steady state, onset, offset, de-induction, and washouts.

Sources: Calculations 5.2, 8.1, 8.2, 8.3, 21.1, 21.2 and 25.1 of
*Drug–Drug Interactions in Drug Safety and Pharmacovigilance*, and the
first-order rules in Sections 8.2 and 21.3.

Educational use only. Every function assumes first-order (single-exponential)
kinetics and constant volume of distribution, as the book's worked
calculations do. Turnover half-lives are uncertain and the book recommends
stating a range rather than a single date. These tools teach the reasoning;
they must not be used to time doses, restarts, or any other clinical decision.

Times and half-lives can be in any unit (hours or days), as long as each call
uses the same unit for all of them.
"""

from __future__ import annotations

from typing import Dict, Optional, Union

from . import _validate as v

Result = Dict[str, Union[float, bool, str, None]]


def time_to_steady_state(
    half_life: float,
    n_half_lives: float = 4.0,
    clearance_ratio: Optional[float] = None,
    auc_ratio: Optional[float] = None,
) -> Result:
    """New half-life, new steady state, and time to approach it after a clearance change.

    Section 8.2 and Calculation 8.1 (Chapter 8): the fraction of the change
    completed after n half-lives is 1 − 0.5^n (50%, 75%, about 94% after four,
    about 97% after five). The half-life that matters is the new one: with
    volume unchanged, new half-life = half-life / clearance ratio, and the
    average steady-state concentration changes by 1 / clearance ratio.

    Calculation 21.2 (Chapter 21) uses the same rule with an AUC ratio as an
    upper bound (14 h × 3.9 ≈ 55 h if the whole AUC increase were systemic).

    Give at most one of ``clearance_ratio`` (new clearance / old, e.g. 0.6 for a
    40% fall) or ``auc_ratio`` (old clearance / new). With neither, clearance is
    unchanged. Assumes first-order elimination and a precipitant effect that
    is constant from the start.
    """
    t_half = v.positive("half_life", half_life)
    n = v.positive("n_half_lives", n_half_lives)
    if clearance_ratio is not None and auc_ratio is not None:
        raise ValueError("give clearance_ratio or auc_ratio, not both")
    if auc_ratio is not None:
        cl = 1.0 / v.positive("auc_ratio", auc_ratio)
    elif clearance_ratio is not None:
        cl = v.positive("clearance_ratio", clearance_ratio)
    else:
        cl = 1.0
    new_half = t_half / cl
    return {
        "new_half_life": new_half,
        "steady_state_ratio": 1.0 / cl,
        "time_to_n_half_lives": n * new_half,
        "fraction_complete": 1.0 - 0.5 ** n,
    }


def exposure_rise_after_inhibition(
    auc_ratio: float,
    bioavailability_before: float,
    bioavailability_after: float,
    half_life: float,
    time_since_start: float,
) -> Result:
    """How far exposure has risen a given time after an inhibitor's effect begins.

    Calculation 25.1 (Chapter 25). The steady-state AUC ratio is split into a
    bioavailability part, which applies to each dose at once
    (F_after / F_before), and a systemic-clearance part
    (AUC ratio / bioavailability ratio). With volume unchanged the half-life
    lengthens by the clearance part. After t, the systemic part has moved a
    fraction 1 − 0.5^(t / new half-life) of the way to its new value:
    systemic now = 1 + fraction × (clearance part − 1), and exposure now =
    bioavailability ratio × systemic now.

    Assumes inhibition fully established at the start time, linear
    pharmacokinetics, and first-order elimination.
    """
    r = v.positive("auc_ratio", auc_ratio)
    f0 = v.fraction("bioavailability_before", bioavailability_before, allow_zero=False)
    f1 = v.fraction("bioavailability_after", bioavailability_after, allow_zero=False)
    t_half = v.positive("half_life", half_life)
    t = v.nonnegative("time_since_start", time_since_start)
    f_ratio = f1 / f0
    clearance_fold = r / f_ratio
    new_half = t_half * clearance_fold
    n = t / new_half
    frac = 1.0 - 0.5 ** n
    systemic_now = 1.0 + frac * (clearance_fold - 1.0)
    return {
        "bioavailability_ratio": f_ratio,
        "clearance_fold": clearance_fold,
        "new_half_life": new_half,
        "n_new_half_lives": n,
        "fraction_to_steady_state": frac,
        "systemic_fold_now": systemic_now,
        "exposure_fold_now": f_ratio * systemic_now,
        "time_to_4_half_lives": 4.0 * new_half,
        "time_to_5_half_lives": 5.0 * new_half,
    }


def residual_inhibition(half_life: float, i_over_ki_at_stop: float, time: float) -> Result:
    """Remaining pathway activity after a reversible inhibitor is stopped.

    Calculation 8.2 (Chapter 8): fraction of inhibitor remaining =
    0.5^(t / half-life); [I]/Ki falls in proportion; remaining activity of the
    affected pathway = 1 / (1 + [I]/Ki). When [I]/Ki is well above 1,
    inhibition declines more slowly than the concentration does.

    Assumes first-order elimination of the inhibitor from steady state and
    competitive inhibition; ignores active metabolites. Tissue inhibition
    constants are rarely known.
    """
    t_half = v.positive("half_life", half_life)
    i0 = v.nonnegative("i_over_ki_at_stop", i_over_ki_at_stop)
    t = v.nonnegative("time", time)
    remaining = 0.5 ** (t / t_half)
    i_t = i0 * remaining
    return {
        "fraction_inhibitor_remaining": remaining,
        "i_over_ki": i_t,
        "pathway_activity": 1.0 / (1.0 + i_t),
        "pathway_activity_at_stop": 1.0 / (1.0 + i0),
    }


def de_induction_remaining(
    half_life: float,
    time: float,
    induced_auc_ratio: Optional[float] = None,
) -> Result:
    """Fraction of the induced enzyme excess remaining after an inducer stops.

    Calculations 5.2 and 8.3 (Chapters 5 and 8): fraction remaining =
    0.5^(t / turnover half-life). The book uses 70 hours and 8 days as two
    published estimates to show the range.

    Calculation 21.1 (Chapter 21): with ``induced_auc_ratio`` (AUC with the
    inducer / without, e.g. 0.18 for rifampin), clearance at stopping is
    1 / ratio, its excess over baseline decays at the same rate, and AUC
    relative to the uninduced value = 1 / (1 + excess × fraction remaining).

    Assumes the inducer is eliminated quickly and the excess decays as a single
    exponential.
    """
    t_half = v.positive("half_life", half_life)
    t = v.nonnegative("time", time)
    remaining = 0.5 ** (t / t_half)
    out: Result = {"fraction_remaining": remaining, "fraction_recovered": 1.0 - remaining}
    if induced_auc_ratio is not None:
        r = v.fraction("induced_auc_ratio", induced_auc_ratio, allow_zero=False)
        clearance_at_stop = 1.0 / r
        excess = clearance_at_stop - 1.0
        clearance_now = 1.0 + excess * remaining
        out.update(
            {
                "clearance_multiple_at_stop": clearance_at_stop,
                "excess_at_stop": excess,
                "clearance_multiple": clearance_now,
                "auc_relative_to_uninduced": 1.0 / clearance_now,
            }
        )
    return out


def washout(
    recovery_half_life: float,
    n_half_lives: float = 5.0,
    elimination_lag: float = 0.0,
    washout_duration: Optional[float] = None,
) -> Result:
    """Washout length from a recovery half-life, and the effect left at a given washout.

    Section 21.3 and Calculation 21.1 (Chapter 21): after the precipitant
    stops, its effect decays exponentially; the fraction remaining after n
    recovery half-lives is 0.5^n (five half-lives leave about 3%). For a
    time-dependent inhibitor, add ``elimination_lag`` (the 1 to 2 days for the
    inhibitor itself to be eliminated) before recovery starts. The time
    required is n × recovery half-life + lag; the effect left at a washout of
    D is 0.5^((D − lag) / recovery half-life).

    Assumes single-exponential recovery, and that probe-based recovery
    estimates (e.g. midazolam) apply to the object drug.
    """
    t_half = v.positive("recovery_half_life", recovery_half_life)
    n = v.positive("n_half_lives", n_half_lives)
    lag = v.nonnegative("elimination_lag", elimination_lag)
    out: Result = {
        "time_required": n * t_half + lag,
        "fraction_remaining_after_n": 0.5 ** n,
    }
    if washout_duration is not None:
        d = v.nonnegative("washout_duration", washout_duration)
        recovering = max(0.0, d - lag)
        out["fraction_remaining_at_washout"] = 0.5 ** (recovering / t_half)
    return out
