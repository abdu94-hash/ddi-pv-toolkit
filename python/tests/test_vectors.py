"""Run every test vector in spec/vectors.json through the matching Python function.

The vectors are the worked numbers from the book; the same file tests the
JavaScript port. Educational use only; not for clinical decisions.
"""

import json
import math
from pathlib import Path

import pytest

from ddi_toolkit.registry import CALCULATORS

VECTORS_PATH = Path(__file__).resolve().parents[2] / "spec" / "vectors.json"
DOC = json.loads(VECTORS_PATH.read_text(encoding="utf-8"))
VECTORS = DOC["vectors"]


def _id(vector):
    return f"{vector['calculator']}[{vector['source']}]"


@pytest.mark.parametrize("vector", VECTORS, ids=[_id(v) for v in VECTORS])
def test_vector(vector):
    calc = CALCULATORS[vector["calculator"]]
    result = calc.func(**vector["inputs"])
    assert set(vector["expected"]) == set(vector["tolerance"]), "every expected output needs a tolerance"
    for key, expected in vector["expected"].items():
        assert key in result, f"{key} is not an output of {calc.name}"
        actual = result[key]
        tol = vector["tolerance"][key]
        assert actual is not None and math.isfinite(actual)
        # A tiny slack absorbs binary floating-point error at the rounding boundary.
        assert abs(actual - expected) <= tol * (1 + 1e-9) + 1e-12, (
            f"{calc.name} {key}: got {actual}, book {expected} ± {tol} ({vector['source']})"
        )


def test_every_calculator_has_a_vector():
    covered = {v["calculator"] for v in VECTORS}
    assert covered == set(CALCULATORS)


def test_vectors_are_plain_json_numbers():
    for v in VECTORS:
        for section in ("inputs", "expected", "tolerance"):
            for key, value in v[section].items():
                assert isinstance(value, (int, float)) and not isinstance(value, bool), (_id(v), section, key)
        assert v["source"]


def test_input_names_match_signatures():
    import inspect

    for v in VECTORS:
        params = inspect.signature(CALCULATORS[v["calculator"]].func).parameters
        assert set(v["inputs"]) <= set(params), _id(v)
