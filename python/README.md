# ddi-toolkit (Python)

Calculators from the book *Drug–Drug Interactions in Drug Safety and Pharmacovigilance* (Dr. Hafez Selim). Each one reproduces a worked calculation in the book, cites it, and is tested against the book's numbers.

> **Educational use only.** These calculators teach the reasoning in the book. They use simplified static models (linear pharmacokinetics, single pathways, first-order kinetics) and illustrative or fictional values. They do not predict what happens in an individual patient. An AUC ratio is not a dose instruction, a reporting rate is not an incidence, and a disproportionality measure is not a risk estimate. **Do not use them for dosing or any other clinical decision.** Ravolixan and Meridian Therapeutics, which appear in the examples, are fictional.

The full specification of every calculator (formula as the book states it, inputs, units, valid ranges, outputs, assumptions, and source) is in [`../spec/CALCULATORS.md`](../spec/CALCULATORS.md). The test values are in [`../spec/vectors.json`](../spec/vectors.json), which also tests the JavaScript calculators.

## Install

Python 3.9 or later. There are no runtime dependencies.

From the repository root:

```
python -m pip install ./python          # regular install
python -m pip install -e ./python       # editable install, for development
```

On Windows, use `py -3 -m pip ...`. This installs the `ddi_toolkit` package and the `ddi-toolkit` command. Without installing, you can run `python -m ddi_toolkit` from the `python/src` folder.

## Command line

`ddi-toolkit --help` lists every calculator. `ddi-toolkit <calculator> --help` shows its inputs, its source in the book, and its main assumption. Inputs are flags (underscores become hyphens), and `--json` prints the result as JSON.

| Calculator | What it does | Book source |
|---|---|---|
| `auc_ratio_inhibition` | AUC ratio from fm and the fraction inhibited or [I]/Ki, with a gut-wall term | Calculations 1.1 and 5.1 |
| `fm_ceiling` | Largest AUC ratio from complete inhibition, 1 / (1 − fm) | Calculations 5.1, 19.1, 23.1 |
| `inhibition_from_auc_ratio` | Fraction inhibited implied by an observed AUC ratio | Calculation 23.1 |
| `induction_auc_ratio` | AUC ratio when a pathway's activity is multiplied | Calculations 5.2 and 10.1 |
| `clearance_pathways` | Route shares, inhibition, and impaired renal function | Calculations 2.1 and 6.2 |
| `protein_binding_displacement` | Total and unbound concentrations after displacement | Calculation 6.1 |
| `dose_adjusted_exposure` | Exposure after a dose change, relative to the usual dose alone | Calculations 23.1 and 19.2 |
| `auc_mic` | 24-hour AUC/MIC against an illustrative target | Calculation 4.1 |
| `time_to_steady_state` | New half-life, new steady state, and time to approach it | Section 8.2, Calculations 8.1 and 21.2 |
| `exposure_rise_after_inhibition` | How far exposure has risen since an inhibitor started | Calculation 25.1 |
| `residual_inhibition` | Pathway activity after a reversible inhibitor is stopped | Calculation 8.2 |
| `de_induction_remaining` | Induced excess remaining after an inducer is stopped | Calculations 5.2, 8.3, 21.1 |
| `washout` | Washout length from a recovery half-life | Section 21.3, Calculation 21.1 |
| `qt_correction` | QTc by Bazett and Fridericia | Calculation 7.1 |
| `exposure_qtc_line` | Mean ΔQTc from a line through two thorough QT results | Calculations 19.2 and 25.1 |
| `absolute_risk` | Absolute and excess risk and number needed to harm | Calculation 9.1 |
| `reporting_rate` | Cases per unit of exposure | Calculations 17.1, 20.1, 22.1 |
| `co_exposure_sensitivity` | Reporting rates under an assumed co-exposure share | Calculations 17.1, 20.1, 22.1 |
| `proportion_ratio` | Ratio and difference of two proportions with a 95% CI | Calculation 24.1 |
| `rule_of_three` | Upper bound when no events are seen, 3 / n | Sections 19.4 and 26.2 |
| `prr_ror` | PRR and ROR with 95% CIs | Calculations 18.1 and 18.2 |
| `information_component` | IC and IC025 | Calculation 18.1 |
| `four_stratum_expectations` | Multiplicative and additive expectations for a combination | Calculation 18.3 |
| `omega_shrinkage` | The Ω interaction measure and Ω025 | Calculations 18.3 and 18.4 |
| `liver_injury_r_ratio` | R ratio and injury pattern | Section 14.4, Worked Case 14.1 |

### Examples with the book's numbers

Calculation 1.1, with the gut-wall extension (fm 0.9, I 0.9, fraction escaping gut metabolism 0.3 to 0.9; the book gives 5.3 and about 16):

```
$ ddi-toolkit auc_ratio_inhibition --fm 0.9 --fraction-inhibited 0.9 --fg-before 0.3 --fg-after 0.9
auc_ratio_inhibition  (Calculation 1.1, Chapter 1; Calculation 5.1, Chapter 5)
  fraction_inhibited   0.9
  remaining_clearance  0.19
  auc_ratio_systemic   5.26316
  gut_factor           3
  auc_ratio            15.7895
Assumption: Linear pharmacokinetics and one inhibited pathway; ignores transporters, metabolites, and individual variability.
Educational use only: simplified static models from the book; not for dosing or clinical decisions.
```

Calculation 6.2, renal function at 40% of normal (book: 2.2 without the inhibitor, 1.4 against the patient's own baseline, 2.9 against a healthy person):

```
$ ddi-toolkit clearance_pathways --nonrenal-fraction 0.1 --renal-fraction 0.4 --secretion-fraction 0.5 --secretion-inhibition 0.6 --renal-function 0.4
  baseline_clearance         0.46
  inhibited_clearance        0.34
  impairment_alone_ratio     2.17391
  auc_ratio_vs_own_baseline  1.35294
  auc_ratio_vs_normal_alone  2.94118
```

Calculation 7.1 (book: 588 ms by Bazett, 549 ms by Fridericia):

```
$ ddi-toolkit qt_correction --qt 480 --heart-rate 90
  rr              0.666667
  qtc_bazett      587.878
  qtc_fridericia  549.463
```

Calculation 8.2, 28 days after stopping an inhibitor with a 50-day half-life and [I]/Ki = 4 (book: 0.68 remaining, [I]/Ki about 2.7, activity about 27%):

```
$ ddi-toolkit residual_inhibition --half-life 50 --i-over-ki-at-stop 4 --time 28
  fraction_inhibitor_remaining  0.678302
  i_over_ki                     2.71321
  pathway_activity              0.269309
  pathway_activity_at_stop      0.2
```

Calculation 21.1, 28 days after rifampin (book: about 9% of the induction left, clearance about 1.4 times baseline, AUC about 0.7 of the uninduced value):

```
$ ddi-toolkit de_induction_remaining --half-life 8 --time 28 --induced-auc-ratio 0.18
  fraction_remaining          0.0883883
  fraction_recovered          0.911612
  clearance_multiple_at_stop  5.55556
  excess_at_stop              4.55556
  clearance_multiple          1.40266
  auc_relative_to_uninduced   0.712932
```

Calculation 18.2, within-drug comparison (book: PRR 7.08, 95% CI 4.02 to 12.47; ROR 7.40, 4.12 to 13.27):

```
$ ddi-toolkit prr_ror --a 21 --b 399 --c 26 --d 3654
  prr        7.07692
  se_ln_prr  0.288839
  prr_lower  4.01772
  prr_upper  12.4655
  ror        7.39676
  se_ln_ror  0.298095
  ror_lower  4.12381
  ror_upper  13.2674
```

Calculation 18.4, the sparse diltiazem stratum (book: E111 0.45, Ω 1.88, Ω025 0.24 by the normal approximation and −0.17 from the gamma posterior):

```
$ ddi-toolkit omega_shrinkage --reports-00 9595900 --events-00 19192 --reports-10 3680 --events-10 26 --reports-01 80000 --events-01 200 --reports-11 60 --events-11 3
  g00                  0.00200403
  g10                  0.00711549
  g01                  0.00250627
  expected_odds        0.00761773
  expected_proportion  0.00756014
  expected_count       0.453608
  observed             3
  unshrunk_log2_ratio  2.72544
  omega                1.87589
  omega025_normal      0.243323
  omega025_gamma       -0.174557
```

Calculation 22.1, if 2% of the 180,000 patient-years involved a CYP3A4 inhibitor (book: 583 and 14.7 per 100,000, ratio about 40):

```
$ ddi-toolkit co_exposure_sensitivity --cases-with 21 --cases-without 26 --total-exposure 180000 --co-exposure-fraction 0.02
  exposure_with     3600
  exposure_without  176400
  rate_with         583.333
  rate_without      14.7392
  rate_ratio        39.5769
```

Each result ends with the calculator's main assumption and the educational-use reminder (shown in full in the first example only). An input outside its valid range gives an error message and exit status 2:

```
$ ddi-toolkit inhibition_from_auc_ratio --fm 0.75 --auc-ratio 4.2
ddi-toolkit inhibition_from_auc_ratio: error: auc_ratio 4.2 exceeds the ceiling 1 / (1 - fm) = 4 for fm = 0.75; the excess cannot come from this pathway alone (for example, gut-wall or transporter inhibition; Calculation 23.1)
```

## Python

Every calculator takes keyword inputs and returns a dict of named outputs. Invalid inputs raise `ValueError` with a message naming the input and its valid range.

```python
from ddi_toolkit import (
    auc_ratio_inhibition, fm_ceiling, time_to_steady_state,
    exposure_rise_after_inhibition, prr_ror, information_component,
)

# Calculation 5.1: fm 0.90 with [I]/Ki = 1, and the ceiling for fm 0.20
auc_ratio_inhibition(fm=0.9, i_over_ki=1)["auc_ratio"]      # 1.818...  (book: 1.8)
fm_ceiling(fm=0.2)["max_increase_percent"]                   # 25.0      (book: about 25%)

# Calculation 8.1: half-life 40 h, clearance falls by 40%
r = time_to_steady_state(half_life=40, clearance_ratio=0.6, n_half_lives=4)
r["new_half_life"], r["time_to_n_half_lives"]                # (66.7, 266.7) hours, about 11 days

# Calculation 25.1: clarithromycin, ravolixan half-life 14 h, 58 h after the start of Day 3
r = exposure_rise_after_inhibition(auc_ratio=3.9, bioavailability_before=0.6,
                                   bioavailability_after=0.9, half_life=14, time_since_start=58)
r["exposure_fold_now"]                                       # 3.10      (book: about 3.1-fold)

# Calculation 18.1: single-drug screen (fictional data)
prr_ror(a=47, b=4053, c=21992, d=9973908)["prr"]             # 5.21
information_component(a=47, b=4053, c=21992, d=9973908)["ic025"]   # 1.87
```

`ddi_toolkit.CALCULATORS` maps each calculator name to its function, book source, and main assumption.

## Tests

```
python -m pip install pytest
python -m pytest python/tests
```

The tests run every vector in `spec/vectors.json` through the matching function (99 vectors taken from the book's worked numbers, with tolerances that reflect the book's rounding), check input validation, and check the command-line interface.

## License

Code: MIT (see `LICENSE` at the repository root).
