# Figures for Chapter 7.
from figlib import *


def fig07_1():
    """Three patterns of pharmacodynamic interaction (Section 7.1)."""
    fig, ax = diagram(3.45)
    cx = [1.22, 2.72, 4.12]          # left edges of the three columns
    cw = [1.22, 1.12, 1.08]          # widths
    for x, w, t in zip(cx, cw, ['Drugs', 'Where they act', 'Shared consequence']):
        text(ax, x + w / 2, 3.3, t, size=7.5, color=GREY, bold=True)
    rows = [(2.42, 0.72), (1.22, 1.02), (0.12, 0.92)]   # (bottom, height) of each band
    labels = [('Same target', 'Both drugs act on one channel'),
              ('Same system,\ndifferent mechanisms', 'Different routes, one outcome'),
              ('Through an\nintermediary', 'One drug changes a variable the other depends on')]
    for (y, h), (t, s) in zip(rows, labels):
        text(ax, 0.1, y + h - 0.12, t, size=8.5, bold=True, color=TEAL, ha='left', va='top')
        nl = t.count('\n') + 1
        text(ax, 0.1, y + h - 0.16 - nl * 0.155, s, size=7, color=GREY, ha='left', va='top', italic=True, wrapw=20)
    for yb in (2.3, 1.1):
        ax.plot([0.1, TEXT_W - 0.1], [yb, yb], color=RULE, lw=0.6)

    def harrow(x1, y1, x2, y2, color=GREY):
        arrow(ax, (x1 + 0.03, y1), (x2 - 0.03, y2), color=color, lw=1.0)

    # Row 1: same target
    y, h = rows[0]
    bh = 0.27
    ys = [y + h - bh - 0.03, y + 0.03]
    for yy, t in zip(ys, ['IKr-blocking drug A', 'IKr-blocking drug B']):
        box(ax, cx[0], yy, cw[0], bh, t, style='light', size=7.5)
    mb = box(ax, cx[1], y + h / 2 - 0.2, cw[1], 0.4, 'IKr potassium channel', style='white', size=7.5)
    for yy in ys:
        harrow(cx[0] + cw[0], yy + bh / 2, cx[1], y + h / 2)
    box(ax, cx[2], y + h / 2 - 0.22, cw[2], 0.44, 'Slower repolarization; longer QT', style='rust', size=7.5)
    harrow(cx[1] + cw[1], y + h / 2, cx[2], y + h / 2)

    # Row 2: same system, different mechanisms
    y, h = rows[1]
    bh = 0.27
    trio = [('Anticoagulant', 'Coagulation'), ('NSAID', 'Platelets; gastric mucosa'), ('SSRI', 'Platelet serotonin')]
    for k, (d, m) in enumerate(trio):
        yy = y + h - 0.03 - bh - k * (bh + 0.08)
        box(ax, cx[0], yy, cw[0], bh, d, style='light', size=7.5)
        box(ax, cx[1], yy, cw[1], bh, m, style='white', size=7)
        harrow(cx[0] + cw[0], yy + bh / 2, cx[1], yy + bh / 2)
        harrow(cx[1] + cw[1], yy + bh / 2, cx[2], y + h / 2)
    box(ax, cx[2], y + h / 2 - 0.2, cw[2], 0.4, 'Bleeding', style='rust', size=7.5)

    # Row 3: through an intermediary
    y, h = rows[2]
    bh = 0.3
    ytop, ybot = y + h - bh - 0.03, y + 0.06
    box(ax, cx[0], ytop, cw[0], bh, 'Loop diuretic', style='light', size=7.5)
    box(ax, cx[0], ybot, cw[0], bh, 'IKr-blocking drug', style='light', size=7.5)
    box(ax, cx[1], ytop - 0.04, cw[1], bh + 0.04, 'Low potassium\n(a lab value)', style='sand', size=7.5)
    box(ax, cx[1], ybot, cw[1], bh, 'IKr block', style='white', size=7.5)
    harrow(cx[0] + cw[0], ytop + bh / 2, cx[1], ytop + bh / 2)
    harrow(cx[0] + cw[0], ybot + bh / 2, cx[1], ybot + bh / 2)
    arrow(ax, (cx[1] + cw[1] / 2, ytop - 0.07), (cx[1] + cw[1] / 2, ybot + bh + 0.03), color=SAND_DARK, lw=1.1)
    text(ax, cx[1] + cw[1] / 2 + 0.06, (ytop + ybot + bh) / 2, 'makes block more potent', size=6.5,
         color=SAND_DARK, ha='left', italic=True)
    box(ax, cx[2], ybot - 0.02, cw[2], 0.36, 'Longer QT', style='rust', size=7.5)
    harrow(cx[1] + cw[1], ybot + bh / 2, cx[2], ybot + bh / 2)
    save(fig, 'fig07_1')


def fig07_3():
    """Repolarization reserve: hits accumulate toward a threshold (Section 7.4). Schematic."""
    fig, ax = diagram(2.55)
    x0, seg, bh = 1.62, 0.5, 0.42
    thr = x0 + 5 * seg
    rows = [
        (1.78, 'One hit', 'usually tolerated', [('QT drug', 'light')]),
        (1.08, 'Less reserve', 'same drug, less margin', [('Female sex', 'grey'), ('Heart failure', 'grey'), ('QT drug', 'light')]),
        (0.38, 'Several coincident hits', 'torsade de pointes more likely',
         [('Female sex', 'grey'), ('Heart failure', 'grey'), ('QT drug', 'light'), ('Second QT drug', 'light'),
          ('Low K or Mg', 'sand'), ('Slow heart rate', 'sand')]),
    ]
    for y, t, s, segs in rows:
        text(ax, 0.1, y + bh - 0.06, t, size=8.5, bold=True, color=TEAL, ha='left', va='top')
        text(ax, 0.1, y + 0.1, s, size=7, color=RUST if 'torsade' in s else GREY, ha='left', italic=True)
        for k, (lab, st) in enumerate(segs):
            box(ax, x0 + k * seg, y, seg, bh, lab, style=st, size=6.5, radius=0.03, lw=0.7, wrapw=9)
    # threshold
    ax.plot([thr, thr], [0.22, 2.36], color=RUST, lw=1.2, ls=(0, (4, 2)), zorder=1)
    text(ax, thr + 0.07, 2.26, 'Threshold for\ntorsade de pointes\n(varies between\npatients)', size=7, color=RUST,
         ha='left', va='top')
    arrow(ax, (x0, 2.38), (thr - 0.04, 2.38), color=GREY, lw=0.8)
    text(ax, (x0 + thr) / 2, 2.47, 'repolarization reserve used up', size=7, color=GREY, italic=True)
    note(ax, 'Grey: patient factors.  Teal: QT-prolonging drugs.  Sand: intermediaries.  Segment sizes are not measured effects.',
         y=0.1, size=6.5)
    save(fig, 'fig07_3')


def fig07_5():
    """Worked Case 7.1: exposures, electrolytes and QTc over days 0 to 10 (fictional)."""
    fig = plt.figure(figsize=(TEXT_W, 3.7))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.15, 1.0], hspace=0.18,
                          left=0.2, right=0.9, top=0.93, bottom=0.11)
    axd, axq, axk = (fig.add_subplot(gs[i]) for i in range(3))
    xl = (-1.6, 10.6)
    for a in (axd, axq, axk):
        a.set_xlim(*xl)
        a.spines[['top', 'right']].set_visible(False)
        a.tick_params(length=3, width=0.6)
        a.axvline(4, color=RUST, lw=1.0, ls=(0, (4, 2)), zorder=0)
    # exposures
    axd.set_ylim(-0.6, 3.6)
    axd.axis('off')
    bars = [(3, 'Citalopram 20 mg', -1.6, 4, TEAL_MID, 'long-standing'),
            (2, 'Levofloxacin', 0, 4, TEAL_MID, None),
            (1, 'IV furosemide', 0, None, SAND_BORDER, None)]
    for y, lab, a0, a1, c, extra in bars:
        end = a1 if a1 is not None else 10.6
        axd.barh(y, end - a0, left=a0, height=0.5, color=c, lw=0)
        axd.text(-1.75, y, lab, ha='right', va='center', fontsize=7.5, color=INK)
    axd.text(-1.75, 0, 'Ondansetron', ha='right', va='center', fontsize=7.5, color=INK)
    axd.plot([3], [0], marker='v', color=RUST, ms=6)
    axd.text(2.75, 0, 'day 3; found at follow-up', fontsize=6.5, color=RUST, va='center', ha='right', style='italic')
    axd.text(4.2, 2.5, 'stopped', fontsize=6.5, color=GREY, va='center', style='italic')
    axd.text(8.0, 1.0, 'stop date not reported', fontsize=6.5, color=GREY, va='center', style='italic', ha='center')
    axd.text(4, 3.75, 'Torsade de pointes, day 4', fontsize=7.5, color=RUST, ha='center', va='bottom', fontweight='bold')
    # QTc
    d, q = [0, 4, 6, 10], [452, 548, 478, 461]
    axq.plot(d, q, color=TEAL, marker='o', ms=4)
    for x, v, dx, dy, ha in zip(d, q, [-0.3, 0.3, 0.2, -0.25], [0, -2, 8, 8], ['right', 'left', 'left', 'right']):
        axq.text(x + dx, v + dy, f'{v}', fontsize=7.5, color=INK, ha=ha, va='bottom' if dy > 0 else 'center')
    axq.set_ylim(420, 575)
    axq.set_yticks([450, 500, 550])
    axq.set_ylabel('QTc (ms)', fontsize=8)
    axq.text(2.2, 432, 'no ECG on day 3', fontsize=6.5, color=GREY, ha='center', style='italic')
    axq.tick_params(labelbottom=False)
    # potassium (magnesium as labels)
    dk, k, mg = [0, 3, 6], [4.1, 2.9, 4.2], [0.80, 0.62, 0.95]
    axk.plot(dk, k, color=SAND_DARK, marker='o', ms=4)
    for x, v, m in zip(dk, k, mg):
        axk.text(x - 0.3 if x == 3 else x + 0.25, v if x == 3 else v + 0.08, f'K {v:.1f}; Mg {m:.2f}', fontsize=7,
                 color=INK, va='center' if x == 3 else 'bottom', ha='right' if x == 3 else 'left')
    axk.set_ylim(2.4, 4.9)
    axk.set_yticks([3, 4])
    axk.set_ylabel('Potassium\n(mmol/L)', fontsize=8)
    axk.set_xticks([0, 2, 4, 6, 8, 10])
    axk.set_xlabel('Day of admission', fontsize=8)
    save(fig, 'fig07_5')


def forest(ax, rows, xlim, ticks, label_x=None):
    """Dot-and-interval rows on a log axis; rows = (label, est, lo, hi, text, color)."""
    n = len(rows)
    for i, (lab, est, lo, hi, txt, c) in enumerate(rows):
        y = n - 1 - i
        ax.plot([lo, hi], [y, y], color=c, lw=1.6, solid_capstyle='butt')
        ax.plot(est, y, 's', color=c, ms=5)
    ax.axvline(1, color=GREY, lw=0.8)
    ax.set_xscale('log')
    ax.set_xlim(*xlim)
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'))
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=7.5)
    ax.tick_params(axis='y', length=0)
    ax.spines['left'].set_visible(False)


def fig07_2():
    """Outcome evidence for specific combinations, as stated in Sections 7.1 to 7.3."""
    rows = [
        ('Opioid + benzodiazepine: overdose visit or admission', 2.14, 2.05, 2.24, 'aOR 2.14 (2.05–2.24) [6]', TEAL),
        ('Opioid + benzodiazepine: overdose death', 3.86, 3.49, 4.26, 'aHR 3.86 (3.49–4.26) [9]', TEAL),
        ('Opioid + gabapentin: opioid-related death', 1.49, 1.18, 1.88, 'aOR 1.49 (1.18–1.88) [12]', TEAL),
        ('NSAID during antithrombotic therapy: bleeding', 2.02, 1.81, 2.26, 'HR 2.02 (1.81–2.26) [7]', RUST),
        ('TMP-SMX with ACE inhibitor or ARB: hyperkalemia', 6.7, 4.5, 10.0, 'aOR 6.7 (4.5–10.0) [11]', SAND_DARK),
        ('TMP-SMX with ACE inhibitor or ARB: sudden death', 1.38, 1.09, 1.76, 'aOR 1.38 (1.09–1.76) [14]', SAND_DARK),
        ('Glyburide + co-trimoxazole: hypoglycemia', 6.6, 4.5, 9.7, 'aOR 6.6 (4.5–9.7) [3]', GREY),
    ]
    fig, ax = chart(2.75)
    fig.subplots_adjust(left=0.47, right=0.73, top=0.97, bottom=0.17)
    forest(ax, rows, (0.8, 12), [1, 2, 4, 8])
    for i, r in enumerate(rows):
        ax.text(1.03, len(rows) - 1 - i, r[4], transform=ax.get_yaxis_transform(), fontsize=7, va='center',
                color=INK)
    ax.set_xlabel('Ratio (log scale; 1 = no association)', fontsize=7.5)
    save(fig, 'fig07_2')


def fig07_4():
    """Calculation 7.1 as curves: QTc from a measured QT of 480 ms by heart rate, Bazett versus Fridericia."""
    import numpy as np
    hr = np.linspace(45, 115, 300)
    rr = 60 / hr
    baz, fri = 480 / rr ** 0.5, 480 / rr ** (1 / 3)
    fig, ax = chart(2.6)
    fig.subplots_adjust(left=0.13, right=0.8, top=0.95, bottom=0.17)
    ax.plot(hr, baz, color=RUST, lw=1.8)
    ax.plot(hr, fri, color=TEAL, lw=1.8)
    ax.axhline(480, color=GREY, lw=0.7, ls=(0, (3, 2)))
    for x, v, c in [(60, 480, INK), (90, 588, RUST), (90, 549, TEAL)]:
        ax.plot(x, v, 'o', color=c, ms=4.5, zorder=3)
    ax.text(62, 470, '480 ms at 60 per minute\n(both formulas)', fontsize=7, color=INK, va='top')
    ax.text(88, 590, '588', fontsize=7.5, color=RUST, ha='right', va='bottom')
    ax.text(92, 546, '549', fontsize=7.5, color=TEAL, ha='left', va='top')
    ax.plot([90, 90], [549, 588], color=GREY, lw=0.8)
    ax.text(116, baz[-1], 'Bazett', fontsize=8, color=RUST, va='center')
    ax.text(116, fri[-1], 'Fridericia', fontsize=8, color=TEAL, va='center')
    ax.text(114, 484, 'measured QT 480 ms', fontsize=6.8, color=GREY, va='bottom', ha='right')
    ax.set_xlim(45, 115)
    ax.set_ylim(420, 690)
    ax.set_xlabel('Heart rate (beats per minute)')
    ax.set_ylabel('Corrected QT (ms)')
    save(fig, 'fig07_4')


if __name__ == '__main__':
    fig07_1(); fig07_2(); fig07_3(); fig07_4(); fig07_5()
