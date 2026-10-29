# Front-matter figures (unnumbered): the map of the book.
from figlib import *

PARTS = [
    ('Part I', 'From interaction warning to safety question', '1–3', 'Warning, relevance, evidence'),
    ('Part II', 'Mechanisms, exposure, and timing', '4–10', 'How and when an interaction acts'),
    ('Part III', 'Assessing incomplete and ambiguous cases', '11–16', 'One case: exposure to reporting'),
    ('Part IV', 'From individual cases to signals', '17–20', 'Many cases: series to signal'),
    ('Part V', 'Turning assessment into action', '21–24', 'Trials, reports, labels, effect'),
    ('Part VI', 'Integrated practice', '25–26', 'A full case; a committee decision'),
]


def fm_map():
    fig, ax = diagram(4.1)
    x0, bw, bh, gap, top = 0.62, 2.7, 0.5, 0.12, 3.85
    ys = [top - bh - k * (bh + gap) for k in range(len(PARTS))]
    for k, ((lab, title, ch, gist), y) in enumerate(zip(PARTS, ys)):
        style = 'teal' if k in (0, 5) else 'light'
        box(ax, x0, y, bw, bh, '', style=style)
        tc = 'white' if style == 'teal' else INK
        text(ax, x0 + 0.1, y + bh - 0.15, f'{lab.upper()}  ·  Chapters {ch}', size=7, bold=True, ha='left',
             color='white' if style == 'teal' else TEAL)
        text(ax, x0 + 0.1, y + 0.16, title, size=8.5, ha='left', color=tc)
        text(ax, x0 + bw + 0.14, y + bh / 2, gist, size=7.5, ha='left', color=GREY, italic=True, wrapw=24)
        if k < len(PARTS) - 1:
            arrow(ax, (x0 + 0.35, y - 0.01), (x0 + 0.35, y - gap + 0.01), lw=0.9)
    # left scale: foundations -> single case -> population -> action
    def bracket(y_hi, y_lo, label, color):
        xb = x0 - 0.1
        ax.plot([xb + 0.05, xb, xb, xb + 0.05], [y_hi, y_hi, y_lo, y_lo], color=color, lw=1.0)
        text(ax, xb - 0.1, (y_hi + y_lo) / 2, label, size=7, color=color, rotation=90, italic=True)
    bracket(ys[0] + bh, ys[1], 'foundations', TEAL)
    bracket(ys[2] + bh, ys[2], 'one case', TEAL)
    bracket(ys[3] + bh, ys[3], 'many cases', TEAL)
    bracket(ys[4] + bh, ys[5], 'action', RUST)
    # right: the ravolixan thread runs from Chapter 16 (end of Part III) to the end
    xr = TEXT_W - 0.12
    y16 = ys[2] + 0.08
    ax.plot([xr - 0.06, xr, xr, xr - 0.06], [y16, y16, ys[5], ys[5]], color=SAND_DARK, lw=1.2)
    text(ax, xr - 0.14, (y16 + ys[5]) / 2, 'ravolixan (fictional): Chapters 16–26', size=7,
         color=SAND_DARK, rotation=90, italic=True)
    note(ax, 'Every chapter ends in a practice output; the worksheets are collected in Appendix A.', y=0.1)
    save(fig, 'fm_map')


if __name__ == '__main__':
    fm_map()
