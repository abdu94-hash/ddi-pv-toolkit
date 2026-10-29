"""Tests for the ddi-toolkit command-line interface."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ddi_toolkit.cli import main
from ddi_toolkit.registry import CALCULATORS, CAVEAT

SRC = Path(__file__).resolve().parents[1] / "src"


def test_help_lists_every_calculator(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    for name in CALCULATORS:
        assert name in out
    assert "not for dosing" in out
    assert out.isascii(), "help must print on any console encoding"


def test_no_subcommand_prints_help(capsys):
    assert main([]) == 1
    assert "calculators" in capsys.readouterr().out


@pytest.mark.parametrize("name", list(CALCULATORS))
def test_each_subcommand_has_help(name, capsys):
    with pytest.raises(SystemExit) as exc:
        main([name, "--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert CALCULATORS[name].source.split(";")[0] in out.replace("\n", " ")
    assert out.isascii()


def test_auc_ratio_output(capsys):
    assert main(["auc_ratio_inhibition", "--fm", "0.9", "--fraction-inhibited", "0.9"]) == 0
    out = capsys.readouterr().out
    assert "auc_ratio" in out and "5.26316" in out
    assert "Assumption:" in out
    assert CAVEAT in out


def test_qt_output(capsys):
    assert main(["qt_correction", "--qt", "480", "--heart-rate", "90"]) == 0
    out = capsys.readouterr().out
    assert "587.8" in out and "549.4" in out


def test_json_output(capsys):
    assert main(["--json", "prr_ror", "--a", "47", "--b", "4053", "--c", "21992", "--d", "9973908"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["calculator"] == "prr_ror"
    assert data["inputs"]["a"] == 47
    assert round(data["result"]["prr"], 2) == 5.21


def test_optional_inputs_and_strings(capsys):
    args = ["liver_injury_r_ratio", "--alt", "1240", "--alt-uln", "40", "--alp", "180", "--alp-uln", "130"]
    assert main(args) == 0
    out = capsys.readouterr().out
    assert "hepatocellular" in out and "bilirubin_x_uln" not in out


def test_invalid_input_exits_2(capsys):
    assert main(["fm_ceiling", "--fm", "1.5"]) == 2
    err = capsys.readouterr().err
    assert "error" in err and "fm" in err


def test_missing_required_input_exits():
    with pytest.raises(SystemExit) as exc:
        main(["fm_ceiling"])
    assert exc.value.code == 2


def test_integer_inputs_parsed_as_int(capsys):
    with pytest.raises(SystemExit):
        main(["rule_of_three", "--n", "2900.5"])
    capsys.readouterr()
    assert main(["rule_of_three", "--n", "2900"]) == 0
    assert "0.00103448" in capsys.readouterr().out


def test_python_dash_m():
    env = dict(os.environ, PYTHONPATH=str(SRC) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    proc = subprocess.run(
        [sys.executable, "-m", "ddi_toolkit", "fm_ceiling", "--fm", "0.75"],
        capture_output=True, text=True, env=env, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "auc_ratio_max" in proc.stdout and "4" in proc.stdout
