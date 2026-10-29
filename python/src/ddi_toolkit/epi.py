"""Epidemiology calculators: absolute risk, reporting rates, proportions, rule of three.

Sources: Calculation 9.1 (Chapter 9), Calculations 17.1, 20.1 and 22.1
(Chapters 17, 20 and 22), Calculation 24.1 (Chapter 24), and the rule of
three in Sections 19.4 and 26.2 of *Drug–Drug Interactions in Drug Safety
and Pharmacovigilance*.

Educational use only. A reporting rate from spontaneous reports is not an
incidence, and a ratio of reporting rates is not a relative risk; both depend
on under-reporting and on denominators that are often assumed rather than
measured. These tools teach the reasoning in the book and must not be used
for clinical decisions.
"""

from __future__ import annotations

import math
from typing import Dict, Union

from . import _validate as v

Result = Dict[str, Union[float, bool, str, None]]


def absolute_risk(baseline_risk: float, relative_risk: float) -> Result:
    """Absolute risk, excess risk, and number needed to harm from a relative effect.

    Calculation 9.1 (Chapter 9): risk with exposure = baseline risk × relative
    risk; excess risk = the difference; number needed to harm = 1 / excess.
    The same 1.6-fold effect gives 1 extra case per 333 people at 0.5%
    baseline risk and 1 per 33 at 5%.

    Risks are proportions (0.005 for 0.5%). Assumes the relative effect is
    constant across baseline risk, which is a simplification; says nothing
    about causation in an individual.
    """
    p0 = v.fraction("baseline_risk", baseline_risk, allow_zero=False, allow_one=False)
    rr = v.positive("relative_risk", relative_risk)
    p1 = p0 * rr
    if p1 > 1:
        raise ValueError(
            f"baseline_risk × relative_risk = {p1:g} exceeds 1; the multiplicative "
            "model cannot apply at this baseline risk"
        )
    excess = p1 - p0
    return {
        "risk_exposed": p1,
        "excess_risk": excess,
        "number_needed_to_harm": 1.0 / excess if excess > 0 else None,
    }


def reporting_rate(cases: int, exposure: float, per: float = 100000.0) -> Result:
    """Reporting rate: cases per unit of exposure, e.g. per 100,000 patient-years.

    Calculations 17.1, 20.1 and 22.1: 47 cases / about 180,000 patient-years
    ≈ 26 per 100,000 patient-years (0.26 per 1,000).

    A reporting rate, not an incidence: it depends on under-reporting,
    stimulated reporting, and case definition.
    """
    n = v.count("cases", cases)
    e = v.positive("exposure", exposure)
    p = v.positive("per", per)
    return {"rate": n / e * p}


def co_exposure_sensitivity(
    cases_with: int,
    cases_without: int,
    total_exposure: float,
    co_exposure_fraction: float,
    per: float = 100000.0,
) -> Result:
    """Reporting rates with and without a co-medication under an assumed co-exposure share.

    Calculations 17.1, 20.1 and 22.1: if a fraction f of the total exposure
    involved the co-medication, the cases with it occurred in total × f and
    the others in total × (1 − f). With 21 and 26 cases in 180,000
    patient-years, the ratio of rates is about 40 at f = 2%, 15 at 5%, and 7 at
    10%.

    The fraction is an assumption, not data; the calculation also assumes that
    reporting is equally complete in both groups. Not an incidence or a
    relative risk.
    """
    n1 = v.count("cases_with", cases_with)
    n0 = v.count("cases_without", cases_without)
    total = v.positive("total_exposure", total_exposure)
    f = v.fraction("co_exposure_fraction", co_exposure_fraction, allow_zero=False, allow_one=False)
    p = v.positive("per", per)
    e1 = total * f
    e0 = total * (1.0 - f)
    r1 = n1 / e1 * p
    r0 = n0 / e0 * p
    return {
        "exposure_with": e1,
        "exposure_without": e0,
        "rate_with": r1,
        "rate_without": r0,
        "rate_ratio": r1 / r0 if r0 > 0 else None,
    }


def proportion_ratio(events_1: int, total_1: int, events_2: int, total_2: int) -> Result:
    """Ratio and difference of two proportions with an approximate 95% CI.

    Calculation 24.1 (Chapter 24): co-dispensing before (group 1) and after
    (group 2) a risk minimization measure. Ratio = p2 / p1; SE of ln ratio =
    √(1/events_2 − 1/total_2 + 1/events_1 − 1/total_1); 95% CI =
    exp(ln ratio ± 1.96 SE). Difference = p2 − p1 (negative for a fall), also
    given per 1,000.

    Treats the two groups as independent samples. When the same people appear
    in both, the interval is too narrow, and a two-period comparison cannot
    exclude a pre-existing trend.
    """
    e1 = v.count("events_1", events_1, minimum=1)
    n1 = v.count("total_1", total_1, minimum=1)
    e2 = v.count("events_2", events_2, minimum=1)
    n2 = v.count("total_2", total_2, minimum=1)
    if e1 > n1:
        raise ValueError(f"events_1 ({e1}) cannot exceed total_1 ({n1})")
    if e2 > n2:
        raise ValueError(f"events_2 ({e2}) cannot exceed total_2 ({n2})")
    p1, p2 = e1 / n1, e2 / n2
    ratio = p2 / p1
    se = math.sqrt(1 / e2 - 1 / n2 + 1 / e1 - 1 / n1)
    return {
        "proportion_1": p1,
        "proportion_2": p2,
        "ratio": ratio,
        "ratio_lower": math.exp(math.log(ratio) - 1.96 * se),
        "ratio_upper": math.exp(math.log(ratio) + 1.96 * se),
        "difference": p2 - p1,
        "difference_per_1000": (p2 - p1) * 1000.0,
    }


def rule_of_three(n: int) -> Result:
    """Approximate upper 95% confidence bound for a risk when no events are seen in n.

    Section 19.4 (Chapter 19) and Section 26.2 (Chapter 26): with zero events in n patients
    the upper bound is about 3 / n; no torsade de pointes in about 2,900
    patients gives roughly 1 in 1,000.

    The bound applies only to the conditions studied (for example, trials that
    excluded strong inhibitors). Absence of events does not exclude a rare harm.
    """
    n = v.count("n", n, minimum=1)
    return {"upper_bound": 3.0 / n, "one_in": n / 3.0}
