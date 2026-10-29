"""Disproportionality calculators for spontaneous report data.

Sources: Sections 18.1 and 18.2 and Calculations 18.1 to 18.4 (Chapter 18) of
*Drug–Drug Interactions in Drug Safety and Pharmacovigilance*.

Educational use only. A disproportionality measure describes how reports are
distributed. It does not measure risk, and it does not establish an
interaction; thresholds are a filter for clinical review, never a finding.
These tools teach the reasoning in the book and must not be used for clinical
decisions.

2×2 table layout (Section 18.1)::

                       Event of interest   All other events
    Drug of interest   a                   b
    All other drugs    c                   d
"""

from __future__ import annotations

import math
from typing import Dict, Union

from . import _validate as v
from ._gamma import gamma_quantile

Result = Dict[str, Union[float, bool, str, None]]

_Z = 1.96
_LN2 = math.log(2.0)


def _table(a: float, b: float, c: float, d: float):
    a = v.count("a", a, minimum=1)
    b = v.count("b", b, minimum=1)
    c = v.count("c", c, minimum=1)
    d = v.count("d", d, minimum=1)
    return a, b, c, d


def prr_ror(a: int, b: int, c: int, d: int) -> Result:
    """PRR and ROR with 95% confidence intervals from a 2×2 table.

    Section 18.1 and Calculations 18.1 and 18.2 (Chapter 18):
    PRR = [a / (a + b)] / [c / (c + d)]; ROR = (a × d) / (b × c);
    SE of ln ROR = √(1/a + 1/b + 1/c + 1/d); 95% CI = exp(ln ROR ± 1.96 SE).

    The book reports PRR confidence intervals without printing their formula;
    the standard log-normal interval used here, SE of ln PRR =
    √(1/a − 1/(a + b) + 1/c − 1/(c + d)), reproduces the book's values.
    All four cells must be at least 1.
    """
    a, b, c, d = _table(a, b, c, d)
    prr = (a / (a + b)) / (c / (c + d))
    se_prr = math.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
    ror = (a * d) / (b * c)
    se_ror = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return {
        "prr": prr,
        "se_ln_prr": se_prr,
        "prr_lower": math.exp(math.log(prr) - _Z * se_prr),
        "prr_upper": math.exp(math.log(prr) + _Z * se_prr),
        "ror": ror,
        "se_ln_ror": se_ror,
        "ror_lower": math.exp(math.log(ror) - _Z * se_ror),
        "ror_upper": math.exp(math.log(ror) + _Z * se_ror),
    }


def information_component(a: int, b: int, c: int, d: int) -> Result:
    """Information component (IC) and its lower 95% credibility limit IC025.

    Section 18.1 and Calculation 18.1 (Chapter 18): O = a,
    E = (a + b)(a + c) / N, IC = log2[(O + 0.5) / (E + 0.5)]. IC025 is taken
    from the gamma posterior with shape O + 0.5 and rate E + 0.5:
    IC025 = log2[q0.025(Gamma(O + 0.5, 1)) / (E + 0.5)].

    ``a`` may be 0; ``b``, ``c`` and ``d`` must be at least 1.
    """
    a = v.count("a", a, minimum=0)
    b = v.count("b", b, minimum=1)
    c = v.count("c", c, minimum=1)
    d = v.count("d", d, minimum=1)
    n = a + b + c + d
    expected = (a + b) * (a + c) / n
    ic = math.log2((a + 0.5) / (expected + 0.5))
    ic025 = math.log2(gamma_quantile(0.025, a + 0.5) / (expected + 0.5))
    return {"observed": float(a), "expected": expected, "ic": ic, "ic025": ic025}


def _strata(
    reports_00, events_00, reports_10, events_10, reports_01, events_01, reports_11, events_11
):
    names = ("00", "10", "01", "11")
    reports = (reports_00, reports_10, reports_01, reports_11)
    events = (events_00, events_10, events_01, events_11)
    f = {}
    n11 = 0
    r11 = 0
    for name, r, e in zip(names, reports, events):
        r = v.count(f"reports_{name}", r, minimum=1)
        e = v.count(f"events_{name}", e, minimum=0)
        if e > r:
            raise ValueError(f"events_{name} ({e}) cannot exceed reports_{name} ({r})")
        if e == r:
            raise ValueError(f"events_{name} must be less than reports_{name} so that the odds are finite")
        f[name] = e / r
        if name == "11":
            n11, r11 = e, r
    return f, n11, r11


def four_stratum_expectations(
    reports_00: int,
    events_00: int,
    reports_10: int,
    events_10: int,
    reports_01: int,
    events_01: int,
    reports_11: int,
    events_11: int,
) -> Result:
    """Expected proportion for a combination under the multiplicative and additive models.

    Section 18.2 and Calculation 18.3 (Chapter 18). For each exposure stratum
    (00 neither drug, 10 drug 1 only, 01 drug 2 only, 11 both), f = events /
    reports. Multiplicative model: expected f11 = f10 × f01 / f00. Additive
    model: expected f11 = f10 + f01 − f00. Expected counts are the expected f11
    times the reports with both drugs.

    Describes reporting, not risk; inherits every bias of single-drug
    disproportionality (Section 18.5).
    """
    f, n11, r11 = _strata(
        reports_00, events_00, reports_10, events_10, reports_01, events_01, reports_11, events_11
    )
    if f["00"] == 0:
        raise ValueError("events_00 must be at least 1 for the multiplicative model")
    mult = f["10"] * f["01"] / f["00"]
    add = f["10"] + f["01"] - f["00"]
    mult_count = mult * r11
    add_count = add * r11
    return {
        "f00": f["00"],
        "f10": f["10"],
        "f01": f["01"],
        "f11": f["11"],
        "multiplicative_expected_f11": mult,
        "multiplicative_expected_count": mult_count,
        "multiplicative_ratio": n11 / mult_count if mult_count > 0 else None,
        "additive_expected_f11": add,
        "additive_expected_count": add_count,
        "additive_excess": f["11"] - add,
        "additive_ratio": n11 / add_count if add_count > 0 else None,
    }


def omega_shrinkage(
    reports_00: int,
    events_00: int,
    reports_10: int,
    events_10: int,
    reports_01: int,
    events_01: int,
    reports_11: int,
    events_11: int,
) -> Result:
    """The Ω shrinkage interaction measure and its lower limits, as the book defines it.

    Section 18.2 and Calculations 18.3 and 18.4 (Chapter 18):

    1. g = f / (1 − f) for each stratum.
    2. Expected odds = max(g00, g10) + max(g00, g01) − g00.
    3. Expected proportion = odds / (1 + odds); E111 = proportion × reports_11.
    4. Ω = log2[(n111 + 0.5) / (E111 + 0.5)].
    5. Ω025 ≈ Ω − 1.96 / (ln 2 × √n111) (normal approximation), or from the
       gamma posterior with shape n111 + 0.5 and rate E111 + 0.5.

    Ω025 above 0 is the screening criterion. The 0.5 is a convention, not a
    derived quantity. The unshrunk ratio log2(n111 / E111) is also returned.
    """
    f, n11, r11 = _strata(
        reports_00, events_00, reports_10, events_10, reports_01, events_01, reports_11, events_11
    )
    g = {k: val / (1.0 - val) for k, val in f.items()}
    odds = max(g["00"], g["10"]) + max(g["00"], g["01"]) - g["00"]
    proportion = odds / (1.0 + odds)
    e111 = proportion * r11
    omega = math.log2((n11 + 0.5) / (e111 + 0.5))
    normal = omega - _Z / (_LN2 * math.sqrt(n11)) if n11 > 0 else None
    gamma = math.log2(gamma_quantile(0.025, n11 + 0.5) / (e111 + 0.5))
    unshrunk = math.log2(n11 / e111) if n11 > 0 and e111 > 0 else None
    return {
        "g00": g["00"],
        "g10": g["10"],
        "g01": g["01"],
        "expected_odds": odds,
        "expected_proportion": proportion,
        "expected_count": e111,
        "observed": float(n11),
        "unshrunk_log2_ratio": unshrunk,
        "omega": omega,
        "omega025_normal": normal,
        "omega025_gamma": gamma,
    }
