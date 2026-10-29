"""Liver injury pattern: the R ratio.

Source: Section 14.4 and the discussion of Worked Case 14.1 in Section 14.5 (Chapter 14) of
*Drug–Drug Interactions in Drug Safety and Pharmacovigilance*.

Educational use only. The R ratio classifies the biochemical pattern of an
injury; it does not establish a cause or an interaction. These tools teach
the reasoning in the book and must not be used for clinical decisions.
"""

from __future__ import annotations

from typing import Dict, Optional, Union

from . import _validate as v

Result = Dict[str, Union[float, bool, str, None]]


def liver_injury_r_ratio(
    alt: float,
    alt_uln: float,
    alp: float,
    alp_uln: float,
    bilirubin: Optional[float] = None,
    bilirubin_uln: Optional[float] = None,
) -> Result:
    """R ratio and injury pattern for suspected drug-induced liver injury.

    Section 14.4 (Chapter 14): R = (ALT / ULN) ÷ (ALP / ULN); hepatocellular
    when R is 5 or more, cholestatic when R is 2 or less, mixed in between. In
    Worked Case 14.1, R = (1,240 ÷ 40) ÷ (180 ÷ 130) ≈ 22, with bilirubin about
    4.4 times the upper limit of normal.

    Each value and its upper limit of normal must be in the same units.
    """
    a = v.positive("alt", alt)
    a_uln = v.positive("alt_uln", alt_uln)
    p = v.positive("alp", alp)
    p_uln = v.positive("alp_uln", alp_uln)
    alt_x = a / a_uln
    alp_x = p / p_uln
    r = alt_x / alp_x
    if r >= 5:
        pattern = "hepatocellular"
    elif r <= 2:
        pattern = "cholestatic"
    else:
        pattern = "mixed"
    out: Result = {"alt_x_uln": alt_x, "alp_x_uln": alp_x, "r_ratio": r, "pattern": pattern}
    if v.optional_pair("bilirubin", bilirubin, "bilirubin_uln", bilirubin_uln):
        b = v.nonnegative("bilirubin", bilirubin)
        b_uln = v.positive("bilirubin_uln", bilirubin_uln)
        out["bilirubin_x_uln"] = b / b_uln
    return out
