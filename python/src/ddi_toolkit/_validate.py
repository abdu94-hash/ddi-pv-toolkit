"""Input checks shared by all calculators.

Every check raises ValueError with a message that names the input, the value
received, and the valid range, so that a reader can see what went wrong.
"""

from __future__ import annotations

import math
from typing import Optional


def number(name: str, value: object) -> float:
    """Return ``value`` as a float, or raise ValueError if it is not a finite number."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number, got {value!r}")
    value = float(value)
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{name} must be a finite number, got {value!r}")
    return value


def positive(name: str, value: object) -> float:
    """A finite number greater than 0."""
    v = number(name, value)
    if v <= 0:
        raise ValueError(f"{name} must be greater than 0, got {v:g}")
    return v


def nonnegative(name: str, value: object) -> float:
    """A finite number greater than or equal to 0."""
    v = number(name, value)
    if v < 0:
        raise ValueError(f"{name} must be 0 or greater, got {v:g}")
    return v


def fraction(
    name: str,
    value: object,
    *,
    allow_zero: bool = True,
    allow_one: bool = True,
) -> float:
    """A proportion between 0 and 1, with the end points allowed or not."""
    v = number(name, value)
    low_ok = v > 0 or (allow_zero and v == 0)
    high_ok = v < 1 or (allow_one and v == 1)
    if not (low_ok and high_ok):
        low = "[0" if allow_zero else "(0"
        high = "1]" if allow_one else "1)"
        raise ValueError(f"{name} must be in the range {low}, {high}, got {v:g}")
    return v


def count(name: str, value: object, *, minimum: int = 0) -> int:
    """A whole-number count of at least ``minimum``."""
    v = number(name, value)
    if v != int(v):
        raise ValueError(f"{name} must be a whole number, got {v:g}")
    if v < minimum:
        raise ValueError(f"{name} must be at least {minimum}, got {int(v)}")
    return int(v)


def at_least(name: str, value: object, minimum: float) -> float:
    """A finite number of at least ``minimum``."""
    v = number(name, value)
    if v < minimum:
        raise ValueError(f"{name} must be at least {minimum:g}, got {v:g}")
    return v


def optional_pair(
    name_a: str, a: Optional[float], name_b: str, b: Optional[float]
) -> bool:
    """Return True if both are given, False if neither; raise if only one is."""
    if (a is None) != (b is None):
        raise ValueError(f"give both {name_a} and {name_b}, or neither")
    return a is not None
