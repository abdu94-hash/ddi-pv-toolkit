"""Gamma distribution quantile, used for the IC025 and Omega025 credibility limits.

Chapter 18 reports lower limits "from the gamma posterior". The posterior used
here has shape (observed + 0.5) and rate (expected + 0.5), so the 2.5th
percentile of the observed-to-expected ratio is
``gamma_quantile(0.025, observed + 0.5) / (expected + 0.5)``. This reproduces the
book's values (IC025 1.87; Omega025 1.27 and -0.17).

The quantile is found by bisection on the regularized lower incomplete gamma
function, computed by its series or continued fraction (standard methods). No
third-party libraries are needed.
"""

from __future__ import annotations

import math

_EPS = 1e-15
_MAX_ITER = 500


def _lower_regularized_series(a: float, x: float) -> float:
    term = 1.0 / a
    total = term
    n = a
    for _ in range(_MAX_ITER):
        n += 1.0
        term *= x / n
        total += term
        if abs(term) < abs(total) * _EPS:
            break
    return total * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _upper_regularized_cf(a: float, x: float) -> float:
    # Modified Lentz continued fraction for Q(a, x).
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, _MAX_ITER):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _EPS:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def gamma_cdf(x: float, shape: float) -> float:
    """Regularized lower incomplete gamma function P(shape, x) (rate 1)."""
    if shape <= 0:
        raise ValueError(f"shape must be greater than 0, got {shape:g}")
    if x <= 0:
        return 0.0
    if x < shape + 1.0:
        return _lower_regularized_series(shape, x)
    return 1.0 - _upper_regularized_cf(shape, x)


def gamma_quantile(p: float, shape: float) -> float:
    """The p-th quantile of a gamma distribution with the given shape and rate 1."""
    if not 0 < p < 1:
        raise ValueError(f"p must be strictly between 0 and 1, got {p:g}")
    if shape <= 0:
        raise ValueError(f"shape must be greater than 0, got {shape:g}")
    lo, hi = 0.0, max(1.0, shape)
    while gamma_cdf(hi, shape) < p:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if gamma_cdf(mid, shape) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-14 * max(1.0, hi):
            break
    return 0.5 * (lo + hi)
