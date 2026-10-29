# Figure source code

These are the Python scripts that draw every figure in *Drug–Drug Interactions in Drug Safety and Pharmacovigilance* (H. Selim). They are published so that readers can see how each figure was built, check the numbers behind the charts, and adapt the diagrams for their own teaching.

| File | What it draws |
|---|---|
| `figlib.py` | Shared look for all figures: the book's teal palette, fonts, sizes, and small helpers for boxes, arrows, text and saving |
| `fm.py` | Front-matter figures (`fm_*.png`, unnumbered) |
| `ch01.py` to `ch26.py` | The figures of each chapter, saved as `figNN_K.png` for Figure NN.K |
| `make_all.py` | Runs `fm.py` and every chapter script in turn |

Model curves in the figures use the simplified static models the book teaches, and every ravolixan figure uses the book's fictional teaching data (see `../data/`). The figures are for teaching. They must not be used for dosing or clinical decisions.

## Running

You need Python 3 and matplotlib (numpy is installed with it):

```
pip install matplotlib
```

Then, from this folder:

```
python make_all.py
```

On Windows you can use `py -3 make_all.py`. To redraw one chapter only, run its script, for example `python ch18.py`.

Output goes to `figures/out/` as 300 dpi PNG files drawn at print size (5.3 inches wide, the text width of the book's 7 × 10 inch page). The folder is created if it does not exist and is ignored by git. A full run draws 133 figures and takes under a minute.

## Fonts

The figures use Calibri when it is installed, as in the book. Where Calibri is not available (for example on most Linux systems), matplotlib falls back to DejaVu Sans, which ships with it. Text then sets slightly wider, and a few labels may sit closer to box edges than in the printed book.

## License

The code is released under the MIT License (see `LICENSE` in the repository root).
