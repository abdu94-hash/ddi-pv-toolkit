# Calculator specification

This file specifies every calculator in the companion toolkit to *Drug–Drug Interactions in Drug Safety and Pharmacovigilance* (Dr. Hafez Selim). The Python package (`python/`) and the web calculators (`docs/`) both implement it, and both are tested against the same file of book values, `spec/vectors.json`.

> **Educational use only.** Each calculator reproduces a worked calculation in the book. It teaches the reasoning with simplified static models and illustrative or fictional values. It does not predict what happens in an individual patient. An AUC ratio is not a dose instruction, and a disproportionality measure is not a risk estimate. Do not use any of these tools for dosing or other clinical decisions.

## Conventions

- **Names.** Calculator names and input and output names are snake_case. They are the same in Python, in the command-line interface (where inputs are written as flags, for example `--fraction-inhibited`), in `vectors.json`, and in the JavaScript port.
- **Inputs and outputs.** Each calculator takes named numeric inputs and returns a set of named outputs. Most outputs are numbers. A few calculators also return a flag (`meets_target`, `extrapolated`) or a label (`pattern`); these are not used in `vectors.json`. An output that cannot be defined for the given inputs (for example, a number needed to harm when there is no excess risk) is returned as `null` (Python `None`).
- **Fractions** are proportions from 0 to 1 (write 0.9, not 90). Risks are proportions too (0.005 for 0.5%).
- **Times.** Times and half-lives can be in hours or days, as long as one call uses the same unit for all of them. Outputs come back in that unit.
- **Validation.** An input outside its valid range is an error (Python raises `ValueError`). The message names the input, the value received, and the valid range. Ranges are given below as [a, b] (end points included) or (a, b) (end points excluded).
- **Numbers.** The 95% limits use z = 1.96. "log2" is the base-2 logarithm and "ln" the natural logarithm.

## Test vectors

`vectors.json` is a JSON object whose `vectors` array holds the test cases:

```json
{
  "calculator": "qt_correction",
  "inputs": {"qt": 480, "heart_rate": 90},
  "expected": {"rr": 0.667, "qtc_bazett": 588, "qtc_fridericia": 549},
  "tolerance": {"rr": 0.0005, "qtc_bazett": 0.5, "qtc_fridericia": 0.5},
  "source": "Calculation 7.1"
}
```

- `expected` holds the number the book prints for some or all outputs. Outputs it does not list are not checked.
- `tolerance` gives an absolute tolerance for each expected output. A test passes if |actual − expected| ≤ tolerance. Implementations may add a slack of about 1e-9 relative to absorb floating-point error.
- The tolerance is half a unit in the last digit the book prints (588 → 0.5; 1.8 → 0.05; 0.0247 → 0.00005). Where the book states an approximate value ("about 40", "under 0.01", "Days 9 to 11"), the vector has a wider tolerance and a `note` that explains it.
- Inputs that a vector leaves out take their defaults.
- Every value in `inputs`, `expected` and `tolerance` is a plain JSON number.

---

## Pharmacokinetic exposure (`pk`)

### auc_ratio_inhibition

**Purpose.** Expected AUC ratio of the object drug when a precipitant inhibits one clearance pathway, with an optional gut-wall term.

**Formula (book).**
- Calculation 1.1: "the expected AUC ratio is approximately 1 / (1 − *fm* × *I*)", where *fm* is the fraction of the object drug's clearance through the pathway and *I* the fraction of the pathway inhibited. Gut wall: "If the fraction escaping gut metabolism rises from 0.3 to 0.9, bioavailability triples, and the effects multiply."
- Section 5.6 and Calculation 5.1: AUCR = 1 / (fm / (1 + [I] / Ki) + (1 − fm)). This is the same equation with *I* = ([I]/Ki) / (1 + [I]/Ki); [I]/Ki = 1 leaves the pathway half its activity.

Computed as: remaining_clearance = 1 − fm × I; auc_ratio_systemic = 1 / remaining_clearance; gut_factor = fg_after / fg_before (1 if not given); auc_ratio = auc_ratio_systemic × gut_factor.

| Input | Unit | Valid range | Notes |
|---|---|---|---|
| `fm` | fraction | [0, 1] | |
| `fraction_inhibited` | fraction | [0, 1] | give exactly one of this or `i_over_ki` |
| `i_over_ki` | ratio | ≥ 0 | [I]/Ki |
| `fg_before` | fraction | (0, 1] | optional; give with `fg_after` |
| `fg_after` | fraction | (0, 1] | optional |

fm = 1 with complete inhibition is an error (no clearance left).

**Outputs.** `fraction_inhibited`, `remaining_clearance`, `auc_ratio_systemic`, `gut_factor`, `auc_ratio`.

**Assumptions and limits (book).** Linear pharmacokinetics and a single inhibited pathway. Ignores transporters, active metabolites, and variability between individuals; inhibitor at steady state; no change in protein binding or renal function. Not a prediction for an individual: fm varies between people and with organ impairment and genotype. An AUC ratio is not a dose instruction and does not establish that an interaction caused an event.

**Source.** Calculation 1.1, Chapter 1; Section 5.6 and Calculation 5.1, Chapter 5.

### fm_ceiling

**Purpose.** The largest AUC ratio that complete inhibition of one pathway can produce: the ceiling that fm puts on inhibition.

**Formula (book).** "If that share is fm and inhibition is complete, the AUC ratio is 1 / (1 − fm)" (Calculation 19.1); with fm = 0.90, "remaining clearance is 0.10 of baseline and AUCR = 10" (Calculation 5.1).

Outputs: remaining_clearance = 1 − fm; auc_ratio_max = 1 / (1 − fm); max_increase_percent = (auc_ratio_max − 1) × 100.

| Input | Unit | Valid range |
|---|---|---|
| `fm` | fraction | [0, 1) |

**Assumptions and limits (book).** The inhibitor blocks only that share of systemic clearance. The formula ignores inhibition of intestinal CYP3A4 and P-gp during first-pass absorption, which is why the observed itraconazole ratio for ravolixan (4.2) can sit slightly above the ceiling of 4.0. With fm = 0.20, no inhibitor of that pathway raises exposure more than about 25%.

**Source.** Calculation 5.1, Chapter 5; Calculation 19.1, Chapter 19; Calculation 23.1, Chapter 23.

### inhibition_from_auc_ratio

**Purpose.** The fraction of a pathway that must be inhibited to produce an observed AUC ratio (Calculation 1.1 run in reverse).

**Formula (book).** "An AUC ratio of 2.0 corresponds to inhibiting about two-thirds of CYP3A4 clearance: 1 / (0.75 × 0.33 + 0.25) ≈ 2.0." Rearranged: fraction_inhibited = (1 − 1 / auc_ratio) / fm.

| Input | Unit | Valid range | Notes |
|---|---|---|---|
| `fm` | fraction | (0, 1] | |
| `auc_ratio` | ratio | ≥ 1 and ≤ 1 / (1 − fm) | above the ceiling is an error |

An AUC ratio above the fm ceiling is rejected with a message: the excess cannot come from this pathway alone (the book's reading of the itraconazole result, 4.2 against 4.0, as near-complete inhibition plus a gut-wall or P-gp contribution).

**Outputs.** `fraction_inhibited`, `remaining_pathway_activity` (= 1 − fraction_inhibited), `auc_ratio_max` (null when fm = 1).

**Assumptions and limits.** Linear pharmacokinetics; fm applies to systemic clearance; the remaining clearance is unaffected.

**Source.** Calculation 23.1, Chapter 23.

### induction_auc_ratio

**Purpose.** AUC ratio when the activity of one pathway is multiplied: induction (Chapter 5) or recovery of suppressed activity when inflammation is relieved (Chapter 10).

**Formula (book).** Calculation 5.2: "Relative clearance = 0.70 × 4 + 0.30 = 3.10, so the systemic contribution to the AUC ratio is 1 / 3.10 ≈ 0.32." "Bioavailability falls from 0.50 to 0.25, a factor of 0.50. Combined AUC ratio ≈ 0.16, an 84% reduction." Calculation 10.1: "Clearance = 0.90 × 1.8 + 0.10 = 1.72. The trough falls to 1 / 1.72 ≈ 0.58 of its previous value."

Computed as: relative_clearance = fm × activity_multiplier + (1 − fm); auc_ratio_systemic = 1 / relative_clearance; bioavailability_ratio = bioavailability_after / bioavailability_before (1 if not given); auc_ratio = auc_ratio_systemic × bioavailability_ratio; percent_change = (auc_ratio − 1) × 100; concentration_after = baseline_concentration × auc_ratio.

| Input | Unit | Valid range | Notes |
|---|---|---|---|
| `fm` | fraction | [0, 1] | share of clearance through the induced pathway |
| `activity_multiplier` | factor | ≥ 1 | 4 for a 4-fold induction; 1.8 for an 80% rise |
| `bioavailability_before` | fraction | (0, 1] | optional; give with `bioavailability_after` |
| `bioavailability_after` | fraction | (0, 1] | optional |
| `baseline_concentration` | any | ≥ 0 | optional; e.g. a trough in ng/mL |

**Outputs.** `relative_clearance`, `auc_ratio_systemic`, `bioavailability_ratio`, `auc_ratio`, `percent_change`, and `concentration_after` if a baseline concentration is given.

**Assumptions and limits (book).** Linear kinetics, no other changes. The multiplier is illustrative and varies by enzyme, inducer, dose, and person. The model says nothing about exposure–response. For Calculation 10.1, steady-state trough concentration is proportional to dose divided by clearance; the size of de-suppression varies between patients and is not known in advance, so it does not give a dose. For reduced activity use `auc_ratio_inhibition`.

**Source.** Calculation 5.2, Chapter 5; Calculation 10.1, Chapter 10.

### clearance_pathways

**Purpose.** Clearance-pathway arithmetic: write down the routes and their shares, which one the precipitant affects, and what the patient's renal function leaves of the rest. Gives the AUC ratio against the patient's own baseline and against a person with normal renal function taking the drug alone.

**Formula (book).** Calculation 2.1: "Baseline clearance = 0.60 + 0.40 = 1.00 (relative units). With the inhibitor: 0.60 × 0.20 + 0.40 = 0.52. The AUC ratio is 1.00 / 0.52 ≈ 1.9." With renal clearance reduced by 75%: "Baseline clearance = 0.60 + 0.10 = 0.70. With the inhibitor: 0.12 + 0.10 = 0.22 … 0.70 / 0.22 ≈ 3.2 … 1.00 / 0.22 ≈ 4.5." Calculation 6.2: "Baseline clearance = 0.40 + 0.50 + 0.10 = 1.00 … With the inhibitor: 0.40 + 0.20 + 0.10 = 0.70"; at 40% renal function "Baseline = 0.16 + 0.20 + 0.10 = 0.46 … With the inhibitor: 0.16 + 0.08 + 0.10 = 0.34."

Computed as:
- baseline_clearance = nonrenal_fraction + renal_function × (renal_fraction + secretion_fraction)
- inhibited_clearance = nonrenal_fraction × (1 − nonrenal_inhibition) + renal_function × (renal_fraction + secretion_fraction × (1 − secretion_inhibition))
- impairment_alone_ratio = 1 / baseline_clearance
- auc_ratio_vs_own_baseline = baseline_clearance / inhibited_clearance
- auc_ratio_vs_normal_alone = 1 / inhibited_clearance

| Input | Unit | Valid range | Default | Notes |
|---|---|---|---|---|
| `nonrenal_fraction` | fraction | [0, 1] | | hepatic or other non-renal routes |
| `renal_fraction` | fraction | [0, 1] | | renal clearance the precipitant does not affect: filtration in 6.2, the whole renal route in 2.1 |
| `secretion_fraction` | fraction | [0, 1] | 0 | active tubular secretion |
| `nonrenal_inhibition` | fraction | [0, 1] | 0 | |
| `secretion_inhibition` | fraction | [0, 1] | 0 | |
| `renal_function` | fraction of normal | (0, 1] | 1 | renal routes scale with it |

The three shares must sum to 1 (within 1e-6). No clearance left is an error.

**Outputs.** `baseline_clearance`, `inhibited_clearance`, `impairment_alone_ratio`, `auc_ratio_vs_own_baseline`, `auc_ratio_vs_normal_alone`.

**Assumptions and limits (book).** Linear pharmacokinetics, so AUC is inversely proportional to clearance; filtration and secretion scale with functioning nephron mass. The shares are illustrative; secretion may not scale with filtration; the inhibitor may also affect reabsorption, non-renal routes, or (for clarithromycin and colchicine) renal P-gp. Exposure only: nothing about a pharmacodynamic interaction or causality in an individual. A relative ratio from a volunteer study understates what a vulnerable patient reaches.

**Source.** Calculation 2.1, Chapter 2; Section 6.4 and Calculation 6.2, Chapter 6.

### protein_binding_displacement

**Purpose.** What displacement from plasma proteins does and does not change at steady state.

**Formula (book).** "Total clearance = unbound fraction (fu) × CLu." "Total concentration = 400 / 40 = 10 mg/L; unbound concentration = 4.0 mg/L." Displacement alone (fu 0.55): total 7.3 mg/L, unbound 4.0 mg/L; with CLu halved: total 14.5 mg/L, unbound 8.0 mg/L.

Computed for baseline (fu, clu) and new (fu_new, clu_new) states: total_clearance = fu × clu; total_concentration = dose_rate / total_clearance; unbound_concentration = fu × total_concentration. Also total_concentration_change = new total / baseline total − 1, and unbound_concentration_ratio = new unbound / baseline unbound.

| Input | Unit | Valid range | Default |
|---|---|---|---|
| `dose_rate` | e.g. mg/day | > 0 | |
| `fu` | fraction | (0, 1] | |
| `clu` | e.g. L/day | > 0 | |
| `fu_new` | fraction | (0, 1] | `fu` |
| `clu_new` | same as `clu` | > 0 | `clu` |

**Outputs.** `total_clearance`, `total_concentration`, `unbound_concentration`, `total_clearance_new`, `total_concentration_new`, `unbound_concentration_new`, `total_concentration_change`, `unbound_concentration_ratio`.

**Assumptions and limits (book).** Oral drug with a low hepatic extraction ratio, linear kinetics, complete bioavailability, average steady-state concentrations only. Ignores the transient rise in unbound concentration immediately after displacement (which can matter for a narrow-margin drug). Does not apply to high-extraction drugs given intravenously, nor to changes in distribution volume; says nothing about pharmacodynamics.

**Source.** Section 6.3 and Calculation 6.1, Chapter 6.

### dose_adjusted_exposure

**Purpose.** Average exposure relative to the usual dose taken alone, after a dose change during coadministration.

**Formula (book).** "Halving the dose to 20 mg. Relative to 40 mg alone: diltiazem 0.5 × 2.0 = 1.0; fluconazole (PBPK) 0.5 × 2.6 = 1.3; itraconazole 0.5 × 4.2 = 2.1; clarithromycin (PBPK) 0.5 × 3.9 ≈ 2.0." Calculation 19.2, Step 5: "exposure is about 2.6 / 2 = 1.3 times the 40 mg reference."

Computed as: dose_fraction = dose / reference_dose; relative_exposure = dose_fraction × auc_ratio.

| Input | Unit | Valid range |
|---|---|---|
| `auc_ratio` | ratio | > 0 |
| `dose` | any | > 0 |
| `reference_dose` | same as `dose` | > 0 |

**Outputs.** `dose_fraction`, `relative_exposure`.

**Assumptions and limits (book).** Linear pharmacokinetics; average exposure only. During repeated dosing, reduced clearance also increases accumulation, so a single-dose Cmax ratio may understate peak exposure at steady state. The calculation does not set a dose.

**Source.** Calculation 23.1, Chapter 23; Calculation 19.2, Chapter 19.

### auc_mic

**Purpose.** Whether an absorption interaction moves 24-hour AUC/MIC across an exposure target.

**Formula (book).** "Linear pharmacokinetics, so the 24-hour AUC at steady state is about twice the single-dose AUC" (twice-daily dosing). "24-hour AUC ≈ 2 × 14.5 = 29 mg·h/L." AUC/MIC is the 24-hour AUC divided by the MIC (29 / 0.03 ≈ 967).

Computed as: auc_24h = doses_per_day × single_dose_auc; auc_mic = auc_24h / mic; if a target is given, target_ratio = auc_mic / target and meets_target = auc_mic ≥ target.

| Input | Unit | Valid range | Notes |
|---|---|---|---|
| `single_dose_auc` | mg·h/L | > 0 | |
| `doses_per_day` | count | > 0 | 2 for twice daily |
| `mic` | mg/L | > 0 | |
| `target` | ratio | > 0 | optional; the book uses 125 as an illustrative threshold |

**Outputs.** `auc_24h`, `auc_mic`, and with a target, `target_ratio` and `meets_target`.

**Assumptions and limits (book).** Every dose affected equally; data from single doses in healthy volunteers; total rather than free drug; reduced renal function raises ciprofloxacin exposure and partly offsets an absorption loss. The target of 125 is illustrative, not validated for any infection. AUC/MIC predicts a probability of response in a population, not the outcome in one patient.

**Source.** Calculation 4.1, Chapter 4.

---

## Timing (`timing`)

### time_to_steady_state

**Purpose.** The new half-life, the new steady state, and the time to approach it after a precipitant changes clearance.

**Formula (book).** Section 8.2: "the fraction of the change completed after *n* half-lives is 1 − 0.5^*n*: 50% after one, 75% after two, about 94% after four, and about 97% after five." Calculation 8.1: "Clearance falls to 0.6 of baseline, so average steady-state concentration rises by 1 / 0.6 ≈ 1.7-fold." "Half-life is inversely proportional to clearance when volume is constant: 40 / 0.6 ≈ 67 hours." "Four new half-lives = 4 × 67 ≈ 267 hours." Calculation 21.2: "if the whole 3.9-fold AUC increase reflected systemic clearance, half-life would be about 14 × 3.9 ≈ 55 hours."

Computed with clearance_ratio = new clearance / old clearance (or 1 / auc_ratio): new_half_life = half_life / clearance_ratio; steady_state_ratio = 1 / clearance_ratio; time_to_n_half_lives = n_half_lives × new_half_life; fraction_complete = 1 − 0.5^n_half_lives.

| Input | Unit | Valid range | Default | Notes |
|---|---|---|---|---|
| `half_life` | h or days | > 0 | | half-life before the change |
| `n_half_lives` | count | > 0 | 4 | |
| `clearance_ratio` | ratio | > 0 | 1 | e.g. 0.6 for a 40% fall; give at most one of this and `auc_ratio` |
| `auc_ratio` | ratio | > 0 | | taken as old clearance / new clearance |

**Outputs.** `new_half_life`, `steady_state_ratio`, `time_to_n_half_lives`, `fraction_complete`.

**Assumptions and limits (book).** First-order elimination; volume of distribution unchanged; the precipitant's effect constant from the first dose, which is false for a precipitant that itself accumulates over weeks. Covers concentration only, not the delay between concentration and clinical response. Using an AUC ratio gives an upper bound for the half-life when part of the increase reflects first-pass metabolism (Calculation 21.2).

**Source.** Section 8.2 and Calculation 8.1, Chapter 8; Calculation 21.2, Chapter 21.

### exposure_rise_after_inhibition

**Purpose.** How far the object drug's exposure has risen a given time after an inhibitor's effect begins, splitting the AUC ratio into an immediate bioavailability part and a slower systemic-clearance part.

**Formula (book).** "Assume inhibition of gut-wall CYP3A4 and P-gp raises [bioavailability] to about 90%, a 1.5-fold increase that applies to each dose immediately. The remaining effect must then come from systemic clearance: 3.9 / 1.5 ≈ 2.6-fold lower clearance. … the half-life lengthens from about 14 h to about 14 × 2.6 ≈ 36 h." "58 / 36 ≈ 1.6 new half-lives. The fraction of the way to the new steady state is 1 − 0.5^1.6 ≈ 0.67. The clearance component has therefore risen from 1 to about 1 + 0.67 × (2.6 − 1) ≈ 2.1-fold. Combined with the bioavailability effect: 1.5 × 2.1 ≈ 3.1-fold." "A new steady state … would be approached 4 to 5 half-lives after Day 3."

Computed as: bioavailability_ratio = bioavailability_after / bioavailability_before; clearance_fold = auc_ratio / bioavailability_ratio; new_half_life = half_life × clearance_fold; n_new_half_lives = time_since_start / new_half_life; fraction_to_steady_state = 1 − 0.5^n_new_half_lives; systemic_fold_now = 1 + fraction_to_steady_state × (clearance_fold − 1); exposure_fold_now = bioavailability_ratio × systemic_fold_now; time_to_4_half_lives = 4 × new_half_life; time_to_5_half_lives = 5 × new_half_life.

| Input | Unit | Valid range |
|---|---|---|
| `auc_ratio` | ratio | > 0 (steady-state AUC ratio) |
| `bioavailability_before` | fraction | (0, 1] |
| `bioavailability_after` | fraction | (0, 1] |
| `half_life` | h or days | > 0 (half-life without the inhibitor) |
| `time_since_start` | same unit | ≥ 0 |

**Outputs.** `bioavailability_ratio`, `clearance_fold`, `new_half_life`, `n_new_half_lives`, `fraction_to_steady_state`, `systemic_fold_now`, `exposure_fold_now`, `time_to_4_half_lives`, `time_to_5_half_lives`.

**Assumptions and limits (book).** Inhibition taken as fully established from the start time (clarithromycin is a time-dependent inhibitor whose effect builds over several days); the PBPK-predicted AUC ratio is clinically unconfirmed; volume unchanged; linear pharmacokinetics. Supports the direction and approximate size of an exposure change; does not establish what happened in a patient and is not a dose instruction.

**Source.** Calculation 25.1, Chapter 25.

### residual_inhibition

**Purpose.** How much of an affected pathway's activity has returned at a given time after a reversible inhibitor with a long half-life is stopped.

**Formula (book).** "Competitive inhibition, so the remaining activity of the affected pathway is 1 / (1 + I/Ki)." "Fraction of inhibitor remaining = 0.5^(t / 50)." "At 28 days, I/Ki ≈ 2.7: activity ≈ 1 / 3.7 ≈ 27%."

Computed as: fraction_inhibitor_remaining = 0.5^(time / half_life); i_over_ki = i_over_ki_at_stop × fraction_inhibitor_remaining; pathway_activity = 1 / (1 + i_over_ki); pathway_activity_at_stop = 1 / (1 + i_over_ki_at_stop).

| Input | Unit | Valid range |
|---|---|---|
| `half_life` | h or days | > 0 (inhibitor terminal half-life) |
| `i_over_ki_at_stop` | ratio | ≥ 0 |
| `time` | same unit | ≥ 0 (time since stopping) |

**Outputs.** `fraction_inhibitor_remaining`, `i_over_ki`, `pathway_activity`, `pathway_activity_at_stop`.

**Assumptions and limits (book).** The inhibitor is stopped after reaching steady state; first-order elimination. When the inhibitor concentration is well above its inhibition constant, inhibition declines more slowly than the concentration does. Real inhibition constants in tissue are rarely known, and the model ignores active metabolites.

**Source.** Section 8.4 and Calculation 8.2, Chapter 8.

### de_induction_remaining

**Purpose.** The fraction of the induced enzyme excess remaining after an inducer is stopped, and (optionally) what that means for the object drug's clearance and AUC.

**Formula (book).** Calculation 8.3: "Fraction of the induced excess remaining = 0.5^(t / half-life)." Calculation 5.2: "With an 8-day recovery half-life, about half the excess activity is gone by day 8, three-quarters by day 16, and about 90% by day 27." Calculation 21.1: "Rifampin reduced ravolixan AUC to 0.18, so clearance was about 5.6 times baseline, an excess of 4.6. If the excess decays at the same rate, 9% of 4.6 ≈ 0.4 remains: clearance about 1.4 times baseline, ravolixan AUC about 0.7 of the uninduced value."

Computed as: fraction_remaining = 0.5^(time / half_life); fraction_recovered = 1 − fraction_remaining. With `induced_auc_ratio`: clearance_multiple_at_stop = 1 / induced_auc_ratio; excess_at_stop = clearance_multiple_at_stop − 1; clearance_multiple = 1 + excess_at_stop × fraction_remaining; auc_relative_to_uninduced = 1 / clearance_multiple.

| Input | Unit | Valid range | Notes |
|---|---|---|---|
| `half_life` | h or days | > 0 | turnover (recovery) half-life; the book uses 70 h and 8 days |
| `time` | same unit | ≥ 0 | time since the inducer stopped |
| `induced_auc_ratio` | ratio | (0, 1] | optional; AUC with the inducer / without |

**Outputs.** `fraction_remaining`, `fraction_recovered`, and with `induced_auc_ratio`: `clearance_multiple_at_stop`, `excess_at_stop`, `clearance_multiple`, `auc_relative_to_uninduced`.

**Assumptions and limits (book).** The inducer is eliminated quickly after stopping; the excess decays with first-order kinetics. Turnover half-lives are uncertain (no consensus for key CYP enzymes), so a timing assessment should state the range, not a single date. Probe-based estimates (oral midazolam after rifampin) are assumed to apply to the object drug, with hepatic and intestinal enzyme recovering at similar rates. For an inducer with a long half-life of its own, such as phenobarbital, the sequence starts later. If the object drug's dose was raised during induction, exposure climbs through this period.

**Source.** Calculation 5.2, Chapter 5; Calculation 8.3, Chapter 8; Calculation 21.1, Chapter 21.

### washout

**Purpose.** Derive a washout from a recovery half-life, and the effect left at a given washout length.

**Formula (book).** Section 21.3: "five inhibitor half-lives remove about 97% of it." Calculation 21.1: "The fraction remaining after *n* recovery half-lives is 0.5 to the power *n*." "Working recovery half-life 2.3 days. Five half-lives ≈ 11.5 days, leaving about 3% of the inhibition. Add 1 to 2 days for the inhibitor to be eliminated: about 13 days."

Computed as: time_required = n_half_lives × recovery_half_life + elimination_lag; fraction_remaining_after_n = 0.5^n_half_lives; with a washout length D, fraction_remaining_at_washout = 0.5^(max(0, D − elimination_lag) / recovery_half_life).

| Input | Unit | Valid range | Default | Notes |
|---|---|---|---|---|
| `recovery_half_life` | h or days | > 0 | | |
| `n_half_lives` | count | > 0 | 5 | |
| `elimination_lag` | same unit | ≥ 0 | 0 | time for the precipitant itself to be eliminated before enzyme recovery starts |
| `washout_duration` | same unit | ≥ 0 | | optional |

**Outputs.** `time_required`, `fraction_remaining_after_n`, and with a washout length, `fraction_remaining_at_washout`.

**Assumptions and limits (book).** The effect decays as a single exponential; midazolam-based recovery estimates are assumed to apply to the object drug; hepatic and intestinal enzyme recover at similar rates. Reversible inhibition ends as the inhibitor is eliminated; time-dependent inhibition and induction end at the rate of enzyme turnover. The calculation makes the reasoning visible; it does not prove a washout correct.

**Source.** Section 21.3 and Calculation 21.1, Chapter 21.

---

## QT (`qt`)

### qt_correction

**Purpose.** Correct a measured QT for heart rate by Bazett's and Fridericia's formulas, to show how the formula and the heart rate change the QTc.

**Formula (book).** "The RR interval is 60 / 90 = 0.667 s." "Bazett. QTc = QT / RR^(1/2)." "Fridericia. QTc = QT / RR^(1/3)."

| Input | Unit | Valid range |
|---|---|---|
| `qt` | ms | (0, 1000] |
| `heart_rate` | beats per minute | (0, 300] |

**Outputs.** `rr` (s), `qtc_bazett` (ms), `qtc_fridericia` (ms).

**Assumptions and limits (book).** At 60 beats per minute both formulas give the measured QT; at faster heart rates Bazett's gives a longer QTc. A change in heart rate between ECGs, or a change of formula, can create or erase an apparent prolongation. Record the formula, the heart rate, and whether the QT was measured manually or by machine; U waves in hypokalemia make the T-wave end hard to define.

**Source.** Calculation 7.1, Chapter 7.

### exposure_qtc_line

**Purpose.** Crude exposure–QTc reasoning: read the mean ΔQTc at a multiple of therapeutic exposure from a straight line through two thorough QT results.

**Formula (book).** "Draw a straight line through the two thorough QT means: 6 ms at 1 times and 18 ms at about 4 times the therapeutic Cmax. The line is ΔQTcF ≈ 2 + 4 × (multiple of therapeutic Cmax)."

Computed as: slope = (dqtc_2 − dqtc_1) / (multiple_2 − multiple_1); intercept = dqtc_1 − slope × multiple_1; dqtc = intercept + slope × multiple; extrapolated = multiple outside [min(multiple_1, multiple_2), max(multiple_1, multiple_2)].

| Input | Unit | Valid range |
|---|---|---|
| `multiple_1`, `multiple_2` | multiple of therapeutic exposure | > 0, and different from each other |
| `dqtc_1`, `dqtc_2` | ms | any number |
| `multiple` | multiple of therapeutic exposure | ≥ 0 |

**Outputs.** `slope` (ms per multiple), `intercept` (ms), `dqtc` (ms), `extrapolated` (flag).

**Assumptions and limits (book).** The line uses two means, not a fitted model; it mixes peak and average concentrations; it describes averages, not individuals; it ignores any QT effect of the inhibitor itself; extrapolation beyond the studied range is less reliable. Thorough QT data come from volunteers with normal potassium, and hypokalemia increases the effect of IKr block. None of it shows that the interaction caused a reported event.

**Source.** Calculation 19.2, Chapter 19; Calculation 25.1, Chapter 25.

---

## Epidemiology and reporting (`epi`)

### absolute_risk

**Purpose.** Show how the same relative effect gives very different absolute harm depending on baseline risk.

**Formula (book).** "Risk with the NSAID: 0.5% × 1.6 = 0.8%. Excess risk: 0.3 percentage points, or about 1 additional case per 333 people treated for a year."

Computed as: risk_exposed = baseline_risk × relative_risk; excess_risk = risk_exposed − baseline_risk; number_needed_to_harm = 1 / excess_risk (null if excess_risk ≤ 0).

| Input | Unit | Valid range |
|---|---|---|
| `baseline_risk` | proportion | (0, 1) |
| `relative_risk` | ratio | > 0, with baseline_risk × relative_risk ≤ 1 |

**Outputs.** `risk_exposed`, `excess_risk`, `number_needed_to_harm`.

**Assumptions and limits (book).** The relative effect is assumed constant across baseline risk, which is a simplification; real relative effects may themselves be larger in high-risk groups. It does not show that a drug caused an event in any individual.

**Source.** Calculation 9.1, Chapter 9.

### reporting_rate

**Purpose.** Reporting rate: cases per unit of exposure.

**Formula (book).** "47 QT-related cases / about 180,000 patient-years ≈ 26 cases per 100,000 patient-years." rate = cases / exposure × per.

| Input | Unit | Valid range | Default |
|---|---|---|---|
| `cases` | count | whole number ≥ 0 | |
| `exposure` | e.g. patient-years | > 0 | |
| `per` | units of exposure | > 0 | 100000 |

**Outputs.** `rate` (cases per `per` units of exposure).

**Assumptions and limits (book).** A reporting rate, not an incidence: it depends on under-reporting (a median of 94% in one systematic review), stimulated reporting, and case definition, which may change over time. A rising reporting rate can reflect rising risk, rising awareness, or both.

**Source.** Calculation 17.1, Chapter 17; Calculation 20.1, Chapter 20; Section 22.3 and Calculation 22.1, Chapter 22.

### co_exposure_sensitivity

**Purpose.** Sensitivity analysis for the unknown denominator: reporting rates with and without a co-medication under an assumed share of exposure.

**Formula (book).** "Suppose a fraction *f* of the 180,000 patient-years involved a concurrent CYP3A4 inhibitor. Then 21 cases occurred in 180,000 × *f* patient-years and 26 in the remainder." "*f* = 2%: 21 / 3,600 = 583 per 100,000; 26 / 176,400 = 14.7. Ratio about 40."

Computed as: exposure_with = total_exposure × f; exposure_without = total_exposure × (1 − f); rate_with = cases_with / exposure_with × per; rate_without = cases_without / exposure_without × per; rate_ratio = rate_with / rate_without (null if rate_without is 0).

| Input | Unit | Valid range | Default |
|---|---|---|---|
| `cases_with` | count | whole number ≥ 0 | |
| `cases_without` | count | whole number ≥ 0 | |
| `total_exposure` | e.g. patient-years | > 0 | |
| `co_exposure_fraction` | fraction | (0, 1) | |
| `per` | units of exposure | > 0 | 100000 |

**Outputs.** `exposure_with`, `exposure_without`, `rate_with`, `rate_without`, `rate_ratio`.

**Assumptions and limits (book).** The fraction is an assumption, not data. The calculation also assumes that reporting is equally complete with and without the co-medication, which is unlikely when an interaction warning is in the label. The direction can be robust while the size is not. None of these figures is an incidence or a relative risk; the calculation supports prioritization and defines the information needed (a drug utilization estimate).

**Source.** Calculation 17.1, Chapter 17; Calculation 20.1, Chapter 20; Calculation 22.1, Chapter 22.

### proportion_ratio

**Purpose.** Compare a proportion between two periods or groups: ratio with an approximate 95% CI, and the absolute difference.

**Formula (book).** "Before: 198 / 10,400 = 1.90%. After: 101 / 11,200 = 0.90%." "Risk ratio. 0.90 / 1.90 = 0.47; approximate 95% CI 0.37 to 0.60, treating the periods as independent samples." "Absolute difference. About 1.0 percentage point, or about 10 fewer ravolixan users per 1,000."

The book does not print the interval formula. The standard log-scale interval, which reproduces the book's values, is used: SE = √(1/events_2 − 1/total_2 + 1/events_1 − 1/total_1); CI = exp(ln ratio ± 1.96 × SE).

Computed as: proportion_1 = events_1 / total_1 (reference, e.g. before); proportion_2 = events_2 / total_2; ratio = proportion_2 / proportion_1; difference = proportion_2 − proportion_1 (negative for a fall); difference_per_1000 = difference × 1000.

| Input | Unit | Valid range |
|---|---|---|
| `events_1`, `events_2` | count | whole number ≥ 1 |
| `total_1`, `total_2` | count | whole number ≥ the matching events |

**Outputs.** `proportion_1`, `proportion_2`, `ratio`, `ratio_lower`, `ratio_upper`, `difference`, `difference_per_1000`.

**Assumptions and limits (book).** Treats the groups as independent samples. When the same patients appear in both periods, the samples are not independent and the interval is too narrow. A two-period comparison cannot exclude a pre-existing downward trend (the full evaluation uses an interrupted time series). For co-dispensing, overlap is inferred from days' supply, not confirmed ingestion.

**Source.** Calculation 24.1, Chapter 24.

### rule_of_three

**Purpose.** Upper bound for a risk when no events have been observed.

**Formula (book).** "When no events are observed in *n* patients, the upper 95% confidence bound for the event rate is approximately 3/*n*." upper_bound = 3 / n; one_in = n / 3.

| Input | Unit | Valid range |
|---|---|---|
| `n` | count | whole number ≥ 1 |

**Outputs.** `upper_bound` (proportion), `one_in` (the bound as "1 in N").

**Assumptions and limits (book).** Zero events observed. The bound applies only to the conditions studied (for example, pivotal trials that excluded strong CYP3A4 inhibitors), so it may say almost nothing about a combination. Absence of events does not exclude a rare harm.

**Source.** Section 19.4, Chapter 19; Section 26.2, Chapter 26.

---

## Disproportionality (`disproportionality`)

All four calculators describe how reports are distributed in a spontaneous reporting database. They do not measure risk and they do not establish an interaction. A threshold is a filter for clinical review, never a finding (Principle box, Section 18.6). Every bias of single-drug disproportionality applies, plus co-prescription and indication, the precipitant's own effect, notoriety and stimulated reporting, selective recording of co-medication, and duplicates (Section 18.5).

The 2×2 table (Section 18.1):

| | Event of interest | All other events |
|---|---|---|
| Drug of interest | a | b |
| All other drugs | c | d |

### prr_ror

**Purpose.** Proportional reporting ratio and reporting odds ratio with 95% confidence intervals.

**Formula (book).** "PRR = [a / (a + b)] / [c / (c + d)]." "ROR = (a × d) / (b × c)." "Standard error of ln ROR = √(1/47 + 1/4,053 + 1/21,992 + 1/9,973,908) = 0.147, so the 95% CI is 3.94 to 7.01."

The book reports PRR intervals (3.92 to 6.93; 4.02 to 12.47) without printing their formula. The standard log-normal interval reproduces them and is used: SE of ln PRR = √(1/a − 1/(a + b) + 1/c − 1/(c + d)); 95% CI = exp(ln PRR ± 1.96 × SE). ROR CI = exp(ln ROR ± 1.96 × SE of ln ROR).

| Input | Unit | Valid range |
|---|---|---|
| `a`, `b`, `c`, `d` | report counts | whole numbers ≥ 1 |

**Outputs.** `prr`, `se_ln_prr`, `prr_lower`, `prr_upper`, `ror`, `se_ln_ror`, `ror_lower`, `ror_upper`.

**Assumptions and limits (book).** A commonly used screening threshold is at least 3 cases, PRR at least 2, and chi-squared at least 4; the measures broadly agree once a combination has about four or more cases. A within-drug comparison (drug with versus without an inhibitor) controls for anything common to the drug's reports but cannot separate an interaction from the inhibitor's own effect on the event.

**Source.** Section 18.1 and Calculations 18.1 and 18.2, Chapter 18.

### information_component

**Purpose.** The BCPNN information component, a shrunk observed-to-expected measure, and its lower 95% credibility limit.

**Formula (book).** "IC … = log2[(O + 0.5) / (E + 0.5)], where O = a and E = (a + b)(a + c) / N, the count expected if drug and event were reported independently." "IC025 = 1.87 (from the gamma posterior)."

The book does not print the posterior. The implementation uses a gamma posterior with shape O + 0.5 and rate E + 0.5, which reproduces the book's IC025 (and its Ω025 values below): IC025 = log2[Q(0.025; shape O + 0.5, rate 1) / (E + 0.5)], where Q is the gamma quantile function. Any accurate gamma quantile (absolute error below 1e-6) is acceptable; the Python version inverts the regularized lower incomplete gamma function by bisection.

| Input | Unit | Valid range |
|---|---|---|
| `a` | report count | whole number ≥ 0 |
| `b`, `c`, `d` | report counts | whole numbers ≥ 1 |

N = a + b + c + d.

**Outputs.** `observed` (= a), `expected` (E), `ic`, `ic025`.

**Assumptions and limits (book).** The added 0.5 shrinks the measure towards zero when counts are small; an IC of 1 means twice the expected count; IC025 > 0 is the usual screening criterion. Shrinkage defends against over-reading noise but also delays the point at which a true rare signal crosses a threshold.

**Source.** Section 18.1 and Calculation 18.1, Chapter 18.

### four_stratum_expectations

**Purpose.** Expected proportion of event reports for a drug combination under the two models of "no interaction", and the observed excess.

**Formula (book).** Section 18.2: for each stratum, f is the proportion of reports that describe the event: f00 (neither), f10 (drug 1 only), f01 (drug 2 only), f11 (both). "Multiplicative model … expected f11 = f10 × f01 / f00." "Additive model … expected f11 = f10 + f01 − f00." Calculation 18.3: "expected count = 0.0247 × 420 = 10.4. Observed 21; ratio observed to expected = 2.0." "excess proportion = 0.0500 − 0.0121 = 0.038."

Computed as: f_xy = events_xy / reports_xy; multiplicative_expected_f11 = f10 × f01 / f00; additive_expected_f11 = f10 + f01 − f00; each expected count = expected f11 × reports_11; each ratio = events_11 / expected count (null if the expected count is not positive); additive_excess = f11 − additive_expected_f11.

| Input | Unit | Valid range |
|---|---|---|
| `reports_00`, `reports_10`, `reports_01`, `reports_11` | report counts | whole numbers ≥ 1 |
| `events_00`, `events_10`, `events_01`, `events_11` | report counts | whole numbers ≥ 0 and below the matching reports; `events_00` ≥ 1 |

**Outputs.** `f00`, `f10`, `f01`, `f11`, `multiplicative_expected_f11`, `multiplicative_expected_count`, `multiplicative_ratio`, `additive_expected_f11`, `additive_expected_count`, `additive_excess`, `additive_ratio`.

**Assumptions and limits (book).** When both drugs are individually associated with the event, the multiplicative expectation is much higher, so an interaction must be larger to stand out; the additive model identified known interactions that the multiplicative model missed. The four-stratum table addresses the precipitant's own effect only to the extent that the inhibitor-only reports resemble the patients who took both drugs.

**Source.** Section 18.2 and Calculation 18.3, Chapter 18 (diltiazem stratum proportions from Calculation 18.4).

### omega_shrinkage

**Purpose.** The Ω shrinkage interaction measure (Norén and colleagues) on an additive baseline, as the book defines it, with its lower 95% limit.

**Formula (book, Section 18.2).**
1. "Convert each stratum proportion to odds: g = f / (1 − f)."
2. "Expected odds for the combination = max(g00, g10) + max(g00, g01) − g00. The max terms stop a drug that appears protective from lowering the expectation."
3. "Convert back to an expected proportion and multiply by the number of reports with both drugs to get E111." (proportion = odds / (1 + odds))
4. "Ω = log2[(n111 + 0.5) / (E111 + 0.5)], where n111 is the observed number of reports with both drugs and the event."
5. "A lower 95% limit, Ω025, can be approximated as Ω − 1.96 / (ln 2 × √n111), or obtained from a gamma posterior distribution. Ω025 above 0 is the screening criterion."

The gamma posterior has shape n111 + 0.5 and rate E111 + 0.5, as for the IC: omega025_gamma = log2[Q(0.025; shape n111 + 0.5, rate 1) / (E111 + 0.5)]. Calculation 18.4 also reports the unshrunk ratio log2(n111 / E111).

| Input | Unit | Valid range |
|---|---|---|
| `reports_00`, `reports_10`, `reports_01`, `reports_11` | report counts | whole numbers ≥ 1 |
| `events_00`, `events_10`, `events_01`, `events_11` | report counts | whole numbers ≥ 0 and below the matching reports |

**Outputs.** `g00`, `g10`, `g01`, `expected_odds`, `expected_proportion`, `expected_count` (E111), `observed` (n111), `unshrunk_log2_ratio` (null if n111 = 0), `omega`, `omega025_normal` (null if n111 = 0), `omega025_gamma`.

**Assumptions and limits (book).** The 0.5 pulls the measure towards zero when counts are small; the value is a convention, not a derived quantity. With very small counts the normal and gamma lower limits can fall on opposite sides of 0 (Calculation 18.4); report the observed count, the expected count, and the interval, not only whether a threshold was crossed. A database-wide screen evaluates very many triplets, so chance crossings are expected; a pre-specified, mechanism-driven analysis is in a different position from a screening hit.

**Source.** Sections 18.2 and 18.4 and Calculations 18.3 and 18.4, Chapter 18.

---

## Liver (`liver`)

### liver_injury_r_ratio

**Purpose.** Classify the biochemical pattern of suspected drug-induced liver injury.

**Formula (book).** "R, calculated as (ALT/ULN) ÷ (ALP/ULN): hepatocellular when R is 5 or more, cholestatic when R is 2 or less, and mixed in between." Worked Case 14.1: "R = (1,240 ÷ 40) ÷ (180 ÷ 130) = 31 ÷ 1.38 ≈ 22, a hepatocellular pattern, with bilirubin about 4.4 times the upper limit of normal."

Computed as: alt_x_uln = alt / alt_uln; alp_x_uln = alp / alp_uln; r_ratio = alt_x_uln / alp_x_uln; pattern = "hepatocellular" if r_ratio ≥ 5, "cholestatic" if r_ratio ≤ 2, otherwise "mixed"; bilirubin_x_uln = bilirubin / bilirubin_uln if given.

| Input | Unit | Valid range |
|---|---|---|
| `alt`, `alt_uln` | U/L (same unit) | > 0 |
| `alp`, `alp_uln` | U/L (same unit) | > 0 |
| `bilirubin` | any (optional; give with `bilirubin_uln`) | ≥ 0 |
| `bilirubin_uln` | same unit | > 0 |

**Outputs.** `alt_x_uln`, `alp_x_uln`, `r_ratio`, `pattern` (label), and `bilirubin_x_uln` if bilirubin is given.

**Assumptions and limits (book).** The pattern matters for causality because drugs tend to produce characteristic patterns and acute viral hepatitis is typically hepatocellular; hepatocellular injury with jaundice signals a risk of serious outcome (Hy's law). The R ratio classifies the injury; it does not identify the cause, and DILI remains a diagnosis of exclusion.

**Source.** Section 14.4 and the discussion of Worked Case 14.1 (Section 14.5), Chapter 14.

---

## Calculations not offered as calculators

These worked calculations are arithmetic on one case rather than a general method, so they are not separate tools.

| Calculation | Why not a calculator |
|---|---|
| Calculation 11.1, Chapter 11 (dating the conception window) | Date arithmetic for one case (subtract the gestational age, add 14 days, allow ±7 days). |
| Calculation 13.1, Chapter 13 (Naranjo totals) | Sums of published item scores for one case; the point of the box is what the algorithm cannot express, not the totals. |
| Section 18.6, Chapter 18 (multiple testing) | A single multiplication (200,000 × 2.5% = 5,000) used to make a point. |
| Calculation 19.2, Steps 1 and 2, Chapter 19 | Average concentration scales with the AUC ratio, and peak lies in a 2.1 to 4.2 bracket: statements, not formulas. Steps 3 to 5 are covered by `exposure_qtc_line` and `dose_adjusted_exposure`. |
| Calculation 21.2, Chapter 21 (restart dates) | Calendar dates for one participant; the arithmetic behind them is covered by `time_to_steady_state` and `washout`. |

## Map from book calculations to calculators

| Book source | Calculator(s) |
|---|---|
| Calculation 1.1, Chapter 1 | `auc_ratio_inhibition` |
| Calculation 2.1, Chapter 2 | `clearance_pathways` |
| Calculation 4.1, Chapter 4 | `auc_mic` |
| Calculation 5.1, Chapter 5 | `auc_ratio_inhibition`, `fm_ceiling` |
| Calculation 5.2, Chapter 5 | `induction_auc_ratio`, `de_induction_remaining` |
| Calculation 6.1, Chapter 6 | `protein_binding_displacement` |
| Calculation 6.2, Chapter 6 | `clearance_pathways` |
| Calculation 7.1, Chapter 7 | `qt_correction` |
| Section 8.2 and Calculation 8.1, Chapter 8 | `time_to_steady_state` |
| Calculation 8.2, Chapter 8 | `residual_inhibition` |
| Calculation 8.3, Chapter 8 | `de_induction_remaining` |
| Calculation 9.1, Chapter 9 | `absolute_risk` |
| Calculation 10.1, Chapter 10 | `induction_auc_ratio` |
| Calculation 11.1, Chapter 11 | not offered (see above) |
| Calculation 13.1, Chapter 13 | not offered (see above) |
| Section 14.4 and Worked Case 14.1, Chapter 14 | `liver_injury_r_ratio` |
| Calculation 17.1, Chapter 17 | `reporting_rate`, `co_exposure_sensitivity` |
| Calculations 18.1 and 18.2, Chapter 18 | `prr_ror`, `information_component` |
| Calculation 18.3, Chapter 18 | `four_stratum_expectations`, `omega_shrinkage` |
| Calculation 18.4, Chapter 18 | `omega_shrinkage`, `four_stratum_expectations` |
| Calculation 19.1, Chapter 19 | `fm_ceiling` |
| Calculation 19.2, Chapter 19 | `exposure_qtc_line`, `dose_adjusted_exposure` |
| Section 19.4, Chapter 19; Section 26.2, Chapter 26 | `rule_of_three` |
| Calculation 20.1, Chapter 20 | `reporting_rate`, `co_exposure_sensitivity` |
| Section 21.3 and Calculation 21.1, Chapter 21 | `washout`, `de_induction_remaining` |
| Calculation 21.2, Chapter 21 | `time_to_steady_state` |
| Calculation 22.1, Chapter 22 | `reporting_rate`, `co_exposure_sensitivity` |
| Calculation 23.1, Chapter 23 | `fm_ceiling`, `inhibition_from_auc_ratio`, `dose_adjusted_exposure` |
| Calculation 24.1, Chapter 24 | `proportion_ratio` |
| Calculation 25.1, Chapter 25 | `exposure_rise_after_inhibition`, `exposure_qtc_line` |
