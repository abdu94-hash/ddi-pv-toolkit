# DDI–PV Toolkit

Companion tools for the book *Drug–Drug Interactions in Drug Safety and Pharmacovigilance: From Mechanisms and Case Assessment to Safety Signals and Risk Management* by Dr. Hafez Selim.

The book teaches interaction assessment through worked calculations, case worksheets, and a running example built on a fictional medicine, ravolixan. This repository makes those materials usable outside the book:

| Folder | What it holds |
|---|---|
| [`docs/`](docs/) | **Web calculators.** Every calculation in the book as an interactive page, with no installation. Published with GitHub Pages: https://abdu94-hash.github.io/ddi-pv-toolkit/ |
| [`python/`](python/) | **Python package and command line** (`ddi_toolkit`, `ddi-toolkit`). The same 25 calculators for scripts and notebooks. |
| [`spec/`](spec/) | **Specification.** The formula, inputs, valid ranges, assumptions and book source for each calculator, plus `vectors.json`, the book's worked numbers used to test both the Python and the JavaScript versions. |
| [`worksheets/`](worksheets/) | **The 26 companion worksheets** as editable Word files and as Markdown, one per chapter. |
| [`data/`](data/) | **Teaching datasets.** The fictional ravolixan case listing, screening counts, exposure and effectiveness data as CSV files, with a data dictionary. |
| [`figures/`](figures/) | **Figure source code.** The scripts that draw the book's figures (matplotlib). |

> **Educational use only.** These tools teach the reasoning in the book. The calculators are simplified static models (linear pharmacokinetics, single pathways, first-order kinetics) run on illustrative or fictional values. They do not predict what happens in an individual patient. An AUC ratio is not a dose instruction, a reporting rate is not an incidence, and a disproportionality measure is not a risk estimate. **Do not use any of these tools for dosing or other clinical decisions.** Coadministration establishes an opportunity for an interaction; it does not establish that an interaction caused the event.

## Quick start

**In a browser.** Open the web calculators at https://abdu94-hash.github.io/ddi-pv-toolkit/, or open `docs/index.html` from a downloaded copy. Each calculator starts with the book's worked example filled in.

**From the command line** (Python 3.10 or later, no other dependencies):

```bash
python -m pip install ./python
ddi-toolkit --help
ddi-toolkit auc_ratio_inhibition --fm 0.9 --fraction-inhibited 0.9
ddi-toolkit qt_correction --qt 480 --heart-rate 90
```

On Windows, use `py -3 -m pip install ./python`. See [`python/README.md`](python/README.md) for every calculator and the Python interface.

**Worksheets.** Download a Word file from [`worksheets/docx/`](worksheets/docx/) or browse the [worksheet index](worksheets/markdown/README.md). Each chapter of the book shows a completed example.

**Datasets.** Start with [`data/README.md`](data/README.md), which lists every file, its columns, and the exercises that use it.

## Calculators

| Topic | Calculators | Book chapters |
|---|---|---|
| Exposure and mechanisms | AUC ratio from fm and inhibition (with gut wall); fm ceiling; inhibition implied by an AUC ratio; induction; clearance pathways and renal impairment; protein-binding displacement; dose-adjusted exposure; AUC/MIC | 1, 2, 4, 5, 6, 10, 19, 23 |
| Timing | Time to a new steady state; exposure rise after an inhibitor starts; residual inhibition after stopping; de-induction; washout length | 5, 8, 21, 25 |
| QT | Bazett and Fridericia correction; exposure–QTc reasoning | 7, 19, 25 |
| Epidemiology and exposure | Absolute versus relative risk; reporting rates; co-exposure sensitivity; proportion ratios; rule of three | 9, 17, 19, 20, 22, 24, 26 |
| Signal detection | PRR and ROR; information component; four-stratum additive and multiplicative expectations; Ω shrinkage | 18 |
| Liver injury | R ratio | 14 |

The full list, with each formula as the book states it, is in [`spec/CALCULATORS.md`](spec/CALCULATORS.md).

## Testing

Both implementations are checked against the same book values:

```bash
cd python && python -m pip install pytest && python -m pytest
node docs/test_vectors.mjs
```

GitHub Actions runs both on every push (see [`.github/workflows/tests.yml`](.github/workflows/tests.yml)).

## About the ravolixan data

Ravolixan, its marketing authorization holder Meridian Therapeutics, study RVX-305, Network A, Database B, and every case and participant in the datasets are fictional. They were constructed so that one evidence base could be followed from a case series to a safety committee decision. Do not cite these numbers as evidence about any real medicine.

## License and citation

- Code (`python/`, `docs/`, `spec/`, `figures/*.py`): [MIT](LICENSE).
- Worksheets, datasets and figure images: [CC BY 4.0](LICENSE-content).

Please cite the book when you use these materials:

> Selim H. *Drug–Drug Interactions in Drug Safety and Pharmacovigilance: From Mechanisms and Case Assessment to Safety Signals and Risk Management.* Companion toolkit: https://github.com/abdu94-hash/ddi-pv-toolkit

Corrections are welcome as GitHub issues. If a calculator disagrees with the book, the issue should quote the calculation number.
