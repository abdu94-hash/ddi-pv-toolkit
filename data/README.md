# Ravolixan teaching datasets

> **Fictional data.** Ravolixan and its marketing authorization holder, Meridian Therapeutics, are invented. They were constructed for teaching in *Drug–Drug Interactions in Drug Safety and Pharmacovigilance* (H. Selim), and every value in these files is invented. Network A, Database B, the reference database, study RVX-305 and all case and participant identifiers are fictional too. Do not cite these numbers as evidence about any real drug, and do not use them for dosing or clinical decisions.

These CSV files hold the fictional data used in the running example of Parts IV to VI of the book (Chapters 16 to 26). The values match the book. Where the book rounds, the file keeps the book's rounding, and columns ending in `_as_printed` hold results exactly as the book prints them, so you can check your own calculations against them.

## Conventions

- Every file name starts with `ravolixan_`, and the first column of every file is `fictional_teaching_data`, which is `yes` on every row.
- UTF-8, comma-separated, one header row, no comment lines. Numbers have no thousands separators. Empty cells mean the book gives no value.
- Dates are ISO 8601 (`YYYY-MM-DD`) where the book gives a full date; otherwise they are written as in the book.
- "Inhibitor" means a moderate or strong CYP3A4 inhibitor as defined in Chapter 17 (clarithromycin, itraconazole, fluconazole, diltiazem in the series). "Strong" or "moderate" follows the class used in the book (ICH M12).
- Reference points: data lock point (DLP) 30 June 2026; PBRER interval 1 July 2025 to 30 June 2026; search with the broad SMQ *Torsade de pointes/QT prolongation*.

The files were transcribed from the manuscript by a script that also checks the totals (for example, 21 + 26 = 47, and every classification of the 21 cases sums to 21).

## Data dictionary

### Case series (Chapter 17)

**`ravolixan_search_funnel.csv`**: retrieval funnel for the QT series. Source: Table in Section 17.6 (`rvxfunnel`), Figure 17.4.
| Column | Meaning | Units |
|---|---|---|
| `step_order` | Order of the step in the funnel | integer |
| `step` | Step description | text |
| `cases` | Cases at this step | reports |
| `parent_step` | `step_order` of the step this one splits from | integer |
| `note` | Note from the book's table | text |

Used in: Worked Case 17.1, Exercise 17.1, Worksheet 17.

**`ravolixan_duplicates_merged.csv`**: the 5 duplicates merged between 52 retrieved and 47 unique reports (illustrative reasons). Source: Section 17.6. Columns: `reason_for_merge` (text), `reports_merged` (reports). Used in: Exercise 17.2.

**`ravolixan_case_listing.csv`**: clinical line listing, 8 of the 21 inhibitor cases, chosen in the book to show the range of documentation. Source: Table in Section 17.7 (`rvxlisting`). The column `event_ecg_electrolytes_as_listed` keeps the book's cell text; the other columns split it into fields.
| Column | Meaning | Units |
|---|---|---|
| `case_id` | Fictional case identifier (MT-YY-NNNN) | text |
| `sex`, `age_years`, `country`, `reporter_type` | Patient and source | F/M, years, ISO country code, text |
| `ravolixan_dose` | Ravolixan dose as reported | text (mg once daily) |
| `inhibitor`, `inhibitor_class`, `inhibitor_dose` | Co-reported CYP3A4 inhibitor, its class, its regimen | text |
| `other_drugs` | Other relevant drugs listed | text |
| `overlap` | Exposure overlap category (Section 17.5): Confirmed, Probable, Unknown, None | category |
| `onset_as_listed` | Onset, as days after the inhibitor was started | text |
| `qtc_ms`, `qtc_note` | QTc value and correction or ECG note | ms, text |
| `potassium_mmol_L`, `magnesium` | Electrolytes where reported | mmol/L; text with units |
| `event_ecg_electrolytes_as_listed` | The book's cell text | text |
| `outcome` | Outcome | text |
| `label_advice` | Whether the label advice was followed | category |
| `information_grade` | Information quality, A, B or C (Section 17.5) | category |

Used in: Worked Case 17.1 (line listing), Exercise 17.2, Worksheet 17, Figure 17.3.

**`ravolixan_inhibitor_cases.csv`**: the 21 inhibitor cases by inhibitor and label advice, with a total row. Source: Table in Section 26.3 (`series`); the same split as Section 17.6 and Worked Case 23.1. Columns: `inhibitor`, `ich_m12_class`, `cases`, `advice_not_followed` (for strong inhibitors, used with ravolixan; for moderate, dose not reduced), `dose_reduced_to_20mg` (empty for strong inhibitors, "not applicable" in the book), `not_applicable_or_not_assessable`; all counts are reports. Used in: Worked Cases 19.1, 23.1 and 26.1, Exercise 23.3.

**`ravolixan_series_characteristics.csv`**: every count the book gives for the 21 cases with an inhibitor and the 26 without, in long format. Sources: Section 17.6, Worked Cases 19.1, 22.1 and 23.1.
| Column | Meaning | Units |
|---|---|---|
| `group` | With inhibitor (n = 21) or without (n = 26) | category |
| `characteristic` | Classification (inhibitor, exposure overlap, label advice, information quality, clinical feature, time to onset, prescriber, receipt period, co-factor) | text |
| `category` | Category within the classification | text |
| `value` | Count, or days for time to onset | see `unit` |
| `unit` | `cases` or `days after inhibitor start` | text |
| `source` | Section or worked case | text |

Used in: Worked Cases 17.1, 18.1, 19.1, 20.1, 22.1, 23.1, 26.1; Figure 17.5.

### Quantitative screening (Chapter 18)

**`ravolixan_screening_strata.csv`**: four-stratum counts in the illustrative reference database of 10,000,000 deduplicated reports. Source: Table in Section 18.7 (`rvxstrata`) and Calculation 18.4. The `diltiazem only` set repeats the ravolixan-alone and background strata, as Calculation 18.4 does ("as in Calculation 18.3").
| Column | Meaning | Units |
|---|---|---|
| `analysis_set` | All moderate or strong CYP3A4 inhibitors, or diltiazem only | text |
| `stratum` | Exposure stratum | text |
| `ravolixan`, `inhibitor` | Exposure flags | yes/no |
| `reports` | Reports in the stratum | reports |
| `qt_related_reports` | Reports with a QT-related event (SMQ broad) | reports |
| `proportion_percent_as_printed` | QT-related proportion as printed | percent |
| `symbol` | Book's notation (f00, f10, f01, f11) | text |
| `source` | Table or calculation | text |

Used in: Calculations 18.3 and 18.4, Exercise 18.1, Figure 18.4, Worksheet 18.

**`ravolixan_disproportionality_2x2.csv`**: the two 2 × 2 tables. Source: Calculations 18.1 and 18.2. Columns: `analysis`, `source`, `a_exposed_qt_related`, `b_exposed_other_events`, `c_comparator_qt_related`, `d_comparator_other_events` (all reports). Used in: Calculations 18.1 and 18.2, Figure 18.5.

**`ravolixan_screening_results.csv`**: the book's results for checking your work: PRR, ROR, IC, expected counts and Ω. Source: Calculations 18.1 to 18.4 and the annotated table in Section 18.8 (`rvxannot`). Columns: `source`, `analysis`, `measure`, `estimate_as_printed`, `lower_as_printed` (95% CI lower bound, IC025 or Ω025), `upper_as_printed` (95% CI upper bound). Used in: Worked Case 18.1, Worksheet 18.

### Pharmacology (Chapters 19 and 21)

**`ravolixan_ddi_studies.csv`**: clinical interaction studies in healthy volunteers and PBPK predictions. Source: Table in Section 21.1 (`rvxddi`), Section 19.3.
| Column | Meaning | Units |
|---|---|---|
| `precipitant`, `precipitant_regimen` | Precipitant drug and dose | text |
| `precipitant_role` | Class of the precipitant | text |
| `evidence_type` | Clinical DDI study or PBPK prediction only | text |
| `auc_ratio` | Ravolixan AUC with / without the precipitant | ratio |
| `auc_ratio_90ci_lower`, `auc_ratio_90ci_upper` | 90% confidence interval where given | ratio |
| `cmax_ratio` | Ravolixan Cmax with / without the precipitant | ratio |
| `source` | Table or section | text |

Used in: Calculations 19.1, 19.2, 21.1, 21.2, 23.1 and 25.1; Figures 16.4, 19.3 and 23.4; Worked Cases 21.1 and 23.1.

**`ravolixan_thorough_qt.csv`**: thorough QT study results. Source: Section 19.3, Table `rvxddi`. Columns: `dose_level`, `multiple_of_therapeutic_cmax` (ratio), `mean_placebo_corrected_dqtcf_ms` (ms), `upper_90ci_ms` (ms), `source`. Used in: Calculations 19.2 and 25.1, Figure 19.4.

**`ravolixan_product_profile.csv`**: product facts used throughout Chapters 16 to 26 (dose, pharmacokinetics, development program, post-marketing exposure). Columns: `domain`, `parameter`, `value`, `unit`, `note`. Source: the running-example facts stated in Chapters 17, 19, 20, 22 and 23.

### Exposure and reporting rates (Chapters 17, 20 and 22)

**`ravolixan_reporting_periods.csv`**: QT-related cases and exposure by period. Source: Calculation 22.1 and Worked Case 22.1. Columns: `period`, `start`, `end`, `patient_years` (patient-years, approximate), `qt_related_cases`, `qt_cases_with_inhibitor`, `ecg_documented_tdp_with_inhibitor` (reports), `rate_all_per_100000_py_as_printed`, `rate_with_inhibitor_per_100000_py_as_printed` (reports per 100,000 patient-years; the inhibitor rate uses all ravolixan exposure as denominator, as in the book), `source`. The before-interval torsade count (2) is the cumulative 6 minus the 4 received in the interval; the book does not print it separately. Used in: Calculation 22.1, Figure 22.2, Worksheet 22.

**`ravolixan_coexposure_scenarios.csv`**: sensitivity analysis for the unknown share of patient-years with a concurrent CYP3A4 inhibitor. Source: Calculations 17.1, 20.1 and 22.1 (rates as printed in 22.1; Calculation 20.1 gives the same rates per 1,000 patient-years). Columns: `assumed_coexposure_percent` (percent of 180,000 patient-years; an assumption, not data), `patient_years_with_inhibitor`, `cases_with_inhibitor`, `patient_years_without_inhibitor`, `cases_without_inhibitor`, `rate_with_per_100000_py_as_printed`, `rate_without_per_100000_py_as_printed`, `ratio_as_printed`. Used in: Calculations 17.1, 20.1 and 22.1, Figures 20.3 and 22.2. These are reporting rates, not incidence.

**`ravolixan_inducer_reports.csv`**: loss-of-efficacy reports with a co-reported inducer (signal RVX-SIG-2026-005; 11 reports, timing established in 3, none serious). Source: Worked Case 20.1. Columns: `inducer`, `loss_of_efficacy_reports` (reports). Used in: Worked Case 20.1, Exercises 20.2, 20.3 and 22.2.

**`ravolixan_pbrer_case_table.csv`**: the case-characteristics table of the model PBRER Section 16.3, kept as printed (cells hold lists such as "9, 2"). Source: Table in Section 22.6 (`pbrercases`). Columns: `characteristic`, `with_cyp3a4_inhibitor_n21`, `without_n26`. Used in: Worked Case 22.1, Exercise 22.3.

### Individual cases (Chapters 21 and 25)

**`ravolixan_trial_114-0087_qtcf.csv`**: RVX-305 participant 114-0087, central QTcF and electrolytes around a prohibited clarithromycin course. Source: Worked Case 21.1 and Section 21.7. Columns: `date`, `visit`, `exposure`, `central_qtcf_ms` (ms), `potassium_mmol_L`, `magnesium_mmol_L` (mmol/L), `note`. Protocol thresholds (illustrative): interrupt if the confirmed QTcF increase is above 30 ms or QTcF is above 480 ms; discontinue if QTcF is above 500 ms or the increase is above 60 ms. Used in: Worked Case 21.1, Calculation 21.2, Figure 21.5, Worksheet 21.

**`ravolixan_case25_1_timeline.csv`**: exposure timeline of Worked Case 25.1 (torsade de pointes on Day 5 of clarithromycin), kept as text. Source: Table in Section 25.7 (`timeline`). Columns: `date`, `day` (Day 1 = first clarithromycin dose), `ravolixan`, `clarithromycin`, `other_exposures`, `events_and_tests`. Used in: Calculation 25.1, Figure 25.2, Worksheet 25.

### Effectiveness of risk minimization (Chapter 24)

Month 0 is the label update and DHPC.

**`ravolixan_alerts_network_a.csv`**: EHR alert displays, overrides and follow-up actions in Network A, months 1 to 6 (about 3,140 patients with an active ravolixan prescription). Source: Worked Case 24.1. Columns: `alert`, `measure`, `count`, `denominator`, `percent_as_printed`. Used in: Worked Case 24.1, Figure 24.3, Exercise 24.1.

**`ravolixan_dhpc_survey.csv`**: DHPC recall and knowledge survey at month 4 (1,050 respondents; the book gives percentages only). Source: Worked Case 24.1. Columns: `respondent_group`, `measure`, `percent_as_printed`. Used in: Worked Case 24.1, Worksheet 24.

**`ravolixan_codispensing_database_b.csv`**: claims-based co-dispensing of ravolixan with strong CYP3A4 inhibitors and fluconazole, and moderate-inhibitor episodes still at 40 mg. Source: Worked Case 24.1 (including the 12-month continuation) and Calculation 24.1 (risk ratio 0.47, approximate 95% CI 0.37 to 0.60, for months 1 to 6 against months −6 to −1). Columns: `measure`, `period`, `numerator`, `denominator`, `percent_as_printed`, `denominator_unit`. Overlap is inferred from days' supply, not confirmed ingestion. Used in: Calculation 24.1, Figure 24.4, Worksheet 24.

**`ravolixan_reports_after_rmm.csv`**: new QT-related spontaneous reports with a CYP3A4 inhibitor in months 1 to 12. Source: Worked Case 24.1 (continued). Columns: `inhibitor`, `qt_related_reports_months_1_to_12` (reports), `note`. Read these as pointers, not rates: the DHPC is expected to have increased reporting.

## License

The datasets are released under CC BY 4.0 (see `LICENSE-content` in the repository root).
