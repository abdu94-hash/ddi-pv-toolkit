"""QT calculators: heart-rate correction and crude exposure–QTc reasoning.

Sources: Calculation 7.1 (Chapter 7), Calculation 19.2 (Chapter 19) and
Calculation 25.1 (Chapter 25) of *Drug–Drug Interactions in Drug Safety and
Pharmacovigilance*.

Educational use only. QT correction formulas and a straight line through two
thorough QT means are teaching devices. They describe averages, not
individuals, and must not be used to interpret a patient's ECG for treatment
or any other clinical decision.
"""

from __future__ import annotations

from typing import Dict, Union

from . import _validate as v

Result = Dict[str, Union[float, bool, str, None]]


def qt_correction(qt: float, heart_rate: float) -> Result:
    """QTc by Bazett and by Fridericia from a measured QT and heart rate.

    Calculation 7.1 (Chapter 7): RR = 60 / heart rate (seconds);
    Bazett QTc = QT / RR^(1/2); Fridericia QTc = QT / RR^(1/3). At 60 beats
    per minute both equal the QT; at faster rates Bazett gives the longer QTc.

    ``qt`` in milliseconds, ``heart_rate`` in beats per minute. Record the
    formula, the heart rate, and how the QT was measured.
    """
    qt_ms = v.positive("qt", qt)
    if qt_ms > 1000:
        raise ValueError(f"qt is in milliseconds and must be at most 1000, got {qt_ms:g}")
    hr = v.positive("heart_rate", heart_rate)
    if hr > 300:
        raise ValueError(f"heart_rate is in beats per minute and must be at most 300, got {hr:g}")
    rr = 60.0 / hr
    return {
        "rr": rr,
        "qtc_bazett": qt_ms / rr ** 0.5,
        "qtc_fridericia": qt_ms / rr ** (1.0 / 3.0),
    }


def exposure_qtc_line(
    multiple_1: float,
    dqtc_1: float,
    multiple_2: float,
    dqtc_2: float,
    multiple: float,
) -> Result:
    """Mean ΔQTc read from a straight line through two thorough QT results.

    Calculation 19.2 (Chapter 19): a line through 6 ms at 1 times and 18 ms at
    about 4 times the therapeutic Cmax is ΔQTcF ≈ 2 + 4 × (multiple). Applied
    to 2.1 and 4.2 times it gives about 10 and 19 ms; to 1.3 times, about 7 ms.
    Calculation 25.1 (Chapter 25) uses the same line at about 3-fold exposure:
    about 14 ms.

    ``multiple_*`` are multiples of therapeutic exposure; ``dqtc_*`` in ms.
    A crude line through two means, not a fitted model; ``extrapolated`` is
    True when ``multiple`` lies outside the two anchor points.
    """
    m1 = v.positive("multiple_1", multiple_1)
    m2 = v.positive("multiple_2", multiple_2)
    q1 = v.number("dqtc_1", dqtc_1)
    q2 = v.number("dqtc_2", dqtc_2)
    m = v.nonnegative("multiple", multiple)
    if m1 == m2:
        raise ValueError("multiple_1 and multiple_2 must differ to define a line")
    slope = (q2 - q1) / (m2 - m1)
    intercept = q1 - slope * m1
    return {
        "slope": slope,
        "intercept": intercept,
        "dqtc": intercept + slope * m,
        "extrapolated": not (min(m1, m2) <= m <= max(m1, m2)),
    }
