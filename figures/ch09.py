# Figures for Chapter 9.
import numpy as np
from figlib import *


def fig09_1():
    """Susceptibility modifies the chain from combination to event; it does not start it (Section 9.1)."""
    fig, ax = diagram(2.35)
    bw, bh, y = 1.0, 0.5, 0.45
    gap = (TEXT_W - 0.2 - 4 * bw) / 3
    xs = [0.1 + k * (bw + gap) for k in range(4)]
    chain = [('Drug combination', 'teal'), ('Exposure\n(concentration)', 'light'),
             ('Response\n(size of effect)', 'light'), ('Event', 'rust')]
    for x, (t, st) in zip(xs, chain):
        box(ax, x, y, bw, bh, t, style=st, size=8)
    for k in range(3):
        arrow(ax, (xs[k] + bw + 0.03, y + bh / 2), (xs[k + 1] - 0.03, y + bh / 2), lw=1.2)
    mods = [(1, 'Changes exposure', 'Organ impairment, genotype, inflammation'),
            (2, 'Changes response', 'Age, disease, other drugs'),
            (3, 'Reduces reserve', 'Frailty, volume depletion, chronic organ disease')]
    mw, mh, my = 1.2, 0.72, 1.48
    for k, t, s in mods:
        cx = xs[k] + bw / 2
        mx = min(max(cx - mw / 2, 0.08), TEXT_W - mw - 0.08)
        box(ax, mx, my, mw, mh, s, style='sand', size=7.2, title=t, align='left')
        arrow(ax, (cx, my - 0.03), (cx, y + bh + 0.04), color=SAND_DARK, lw=1.0, ls=(0, (3, 2)))
    text(ax, xs[0] + bw / 2, my + mh / 2, 'Susceptibility\nfactors act\non each link', size=7.5,
         color=SAND_DARK, italic=True)
    note(ax, 'The same combination can be harmless in most people and harmful in one: susceptibility sets the size, not the start.',
         y=0.16, size=7)
    save(fig, 'fig09_1')


def fig09_2():
    """The 'triple whammy': three supports of glomerular filtration, each removed by one drug (Section 9.3)."""
    fig, ax = diagram(3.3)
    py = 2.15                      # centre line of the vessels
    pr = 0.07                      # half-width of an arteriole
    box(ax, 0.1, py - 0.3, 1.0, 0.6, 'Circulating volume', style='light', size=8)

    def pipe(x0, x1):
        for dy in (-pr, pr):
            ax.plot([x0, x1], [py + dy, py + dy], color=TEAL, lw=1.4, zorder=2)
    pipe(1.1, 2.25)
    gx, gr = 2.62, 0.37
    ax.add_patch(matplotlib.patches.Circle((gx, py), gr, fc=TEAL_LIGHT, ec=TEAL, lw=1.2, zorder=2))
    text(ax, gx, py, 'Glomerulus', size=7.5, color=TEAL, bold=True)
    pipe(gx + gr, 3.85)
    arrow(ax, (3.85, py), (4.15, py), color=TEAL, lw=1.2)
    # supports (teal) above
    text(ax, 1.68, 2.75, 'Afferent arteriole:\nprostaglandins dilate it', size=7.5, color=TEAL)
    text(ax, 3.42, 2.75, 'Efferent arteriole:\nangiotensin II constricts it', size=7.5, color=TEAL)
    text(ax, 0.6, 2.75, 'Volume sustains\nrenal perfusion', size=7.5, color=TEAL)
    text(ax, gx, 3.18, 'Three supports of filtration pressure', size=7.5, color=GREY, italic=True)
    # drugs (rust) below
    dy, dh = 1.05, 0.48
    drugs = [(0.1, 1.0, 0.6, 'Diuretic reduces volume'), (1.18, 1.0, 1.68, 'NSAID blocks prostaglandin synthesis'),
             (2.92, 1.0, 3.42, 'ACE inhibitor or ARB removes angiotensin II')]
    for x, w, cx, t in drugs:
        box(ax, x, dy, w, dh, t, style='rust', size=7.2)
        arrow(ax, (cx, dy + dh + 0.03), (cx, py - (0.3 if cx < 1 else pr) - 0.04), color=RUST, lw=1.0)
    # result
    arrow(ax, (gx, py - gr - 0.03), (gx, 0.6), color=GREY, lw=1.2)
    box(ax, 1.25, 0.15, 2.3, 0.42, 'Filtration falls: acute kidney injury', style='accent', size=8)
    box(ax, 3.75, 0.15, 1.47, 0.78, 'Each drug alone is usually tolerated. Together, and with vomiting, diarrhea or heat, '
        'they remove all three supports. No drug concentration changes.', style='sand', size=6.8, align='left')
    save(fig, 'fig09_2')


def fig09_5():
    """Codeine pathways, usual and in the Gasche case (Section 9.4). Arrow widths schematic."""
    fig, ax = diagram(3.3)
    rows = [(2.05, 'Usual\npathways', False), (0.6, 'Gasche case', True)]
    cx0, cw = 0.95, 0.85
    mx, mw = 2.75, 0.95
    ex, ew = 4.3, 0.92
    bh = 0.36
    mo, co, no = 0.8, 0.35, -0.1        # vertical offsets of morphine, codeine and norcodeine boxes
    for y, lab, case in rows:
        text(ax, 0.08, y + co + bh / 2, lab, size=8.5, bold=True, color=RUST if case else TEAL, ha='left')
        box(ax, cx0, y + co, cw, bh, 'Codeine', style='light', size=8)
        box(ax, mx, y + mo, mw, bh, 'More morphine' if case else 'Morphine', style='accent' if case else 'teal', size=8)
        box(ax, mx, y + no, mw, bh, 'Norcodeine', style='grey', size=8)
        box(ax, ex, y + mo, ew, bh, 'Glucuronides out via kidney', style='white', size=7, wrapw=16)
        c_r = (cx0 + cw + 0.03, y + co + bh / 2)
        arrow(ax, c_r, (mx - 0.03, y + mo + bh / 2), color=RUST if case else TEAL, lw=3.0 if case else 1.3,
              head=10 if case else 7)
        arrow(ax, c_r, (mx - 0.03, y + no + bh / 2), color=GREY, lw=0.8 if case else 1.3,
              ls=(0, (3, 2)) if case else '-')
        arrow(ax, (mx + mw + 0.03, y + mo + bh / 2), (ex - 0.03, y + mo + bh / 2), color=GREY,
              lw=0.8 if case else 1.3, ls=(0, (3, 2)) if case else '-')
        if case:
            text(ax, 2.05, y + 0.92, 'CYP2D6: ultrarapid\ngenotype, more capacity', size=6.8, color=RUST, ha='right')
            text(ax, 2.05, y + 0.02, 'CYP3A4: blocked by\nco-medications', size=6.8, color=RUST, ha='right')
            text(ax, (mx + mw + ex) / 2, y + 0.6, 'reduced renal\nfunction', size=6.8, color=RUST)
        else:
            text(ax, 2.05, y + 0.85, 'CYP2D6', size=7.5, color=TEAL, ha='right')
            text(ax, 2.05, y + 0.1, 'CYP3A4', size=7.5, color=GREY, ha='right')
    ax.plot([0.08, TEXT_W - 0.08], [1.85, 1.85], color=RULE, lw=0.6)
    note(ax, 'Arrow widths are schematic, not measured fractions.', y=0.2, size=6.8)
    save(fig, 'fig09_5')


def fig09_3():
    """Two nested case-control studies of NSAID combinations and AKI (Section 9.3), forest-style."""
    rows = [
        ('UK, hospital-coded AKI [10]', None, None, None, '', None),
        ('Triple combination, current use', 1.31, 1.12, 1.53, '1.31 (1.12–1.53)', TEAL),
        ('Triple combination, first 30 days', 1.82, 1.35, 2.46, '1.82 (1.35–2.46)', TEAL),
        ('Double combinations with an NSAID', None, None, None, 'no increased risk', GREY),
        ('Scotland, laboratory-defined AKI [11]', None, None, None, '', None),
        ('Triple combination', 1.64, 1.25, 2.14, '1.64 (1.25–2.14)', RUST),
        ('NSAID + renin–angiotensin inhibitor', 1.60, 1.18, 2.17, '1.60 (1.18–2.17)', RUST),
        ('NSAID + diuretic', 1.64, 1.17, 2.29, '1.64 (1.17–2.29)', RUST),
    ]
    fig, ax = chart(2.75)
    fig.subplots_adjust(left=0.4, right=0.76, top=0.97, bottom=0.16)
    n = len(rows)
    labels = []
    for i, (lab, est, lo, hi, txt, c) in enumerate(rows):
        y = n - 1 - i
        if est is not None:
            ax.plot([lo, hi], [y, y], color=c, lw=1.6)
            ax.plot(est, y, 's', color=c, ms=5)
        if txt:
            ax.text(1.03, y, txt, transform=ax.get_yaxis_transform(), fontsize=7.5, va='center',
                    color=GREY if est is None else INK, style='italic' if est is None else 'normal')
        labels.append(lab)
    ax.axvline(1, color=GREY, lw=0.8)
    ax.set_xscale('log')
    ax.set_xlim(0.8, 3)
    ax.set_xticks([1, 1.5, 2, 3])
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'))
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels[::-1], fontsize=7.5)
    for t, (lab, est, *_rest) in zip(ax.get_yticklabels()[::-1], rows):
        if est is None and _rest[2] == '':
            t.set_fontweight('bold'); t.set_color(TEAL)
    ax.tick_params(axis='y', length=0)
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Rate ratio for AKI (log scale)', fontsize=7.5)
    save(fig, 'fig09_3')


def fig09_4():
    """Calculation 9.1 as bars: the same relative effect in a low-risk and a high-risk person."""
    fig, ax = chart(2.5)
    fig.subplots_adjust(left=0.12, right=0.97, top=0.95, bottom=0.12)
    groups = ['Low-risk person', 'High-risk person']
    base, nsaid = [0.5, 5.0], [0.8, 8.0]
    x = np.array([0, 1.25])
    w = 0.36
    ax.bar(x - w / 2 - 0.02, base, w, color=RULE)
    ax.bar(x + w / 2 + 0.02, nsaid, w, color=RUST)
    for xi, b, v in zip(x, base, nsaid):
        ax.text(xi - w / 2 - 0.02, b + 0.15, f'{b:g}%', ha='center', va='bottom', fontsize=7.5)
        ax.text(xi + w / 2 + 0.02, v + 0.15, f'{v:g}%', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    ax.text(x[0] - w / 2 - 0.02, 1.4, 'baseline', ha='center', fontsize=7, color=GREY)
    ax.text(x[0] + w / 2 + 0.02, 1.7, 'with NSAID\n(× 1.6)', ha='center', fontsize=7, color=RUST)
    ax.text(x[0], 4.1, 'excess 0.3 points:\nabout 1 per 333\ntreated for a year', fontsize=7.2, color=INK,
            va='center', ha='center')
    ax.text(x[1] + 0.45, 6.2, 'excess 3 points:\nabout 1 per 33\ntreated for a year', fontsize=7.2, color=INK,
            va='center', fontweight='bold')
    ax.set_xticks(x, groups)
    ax.set_xlim(-0.5, 2.3)
    ax.set_ylim(0, 9.5)
    ax.set_ylabel('One-year risk of AKI (%)', fontsize=8)
    save(fig, 'fig09_4')


def fig09_6():
    """Worked Case 9.1 chronology after follow-up (fictional)."""
    fig = plt.figure(figsize=(TEXT_W, 3.3))
    gs = fig.add_gridspec(2, 1, height_ratios=[0.9, 1.4], hspace=0.12, left=0.2, right=0.96, top=0.97, bottom=0.12)
    axe, axc = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    xl = (-10.5, 13)
    for a in (axe, axc):
        a.set_xlim(*xl)
        a.spines[['top', 'right']].set_visible(False)
        a.tick_params(length=3, width=0.6)
        a.axvline(5, color=GREY, lw=0.7, ls=(0, (3, 2)), zorder=0)
    axe.axis('off')
    axe.set_ylim(-0.4, 3.6)
    tracks = [(3, 'Furosemide 40 mg', -8, 8, SAND_BORDER, 'doubled 9 days before day 1'),
              (2, 'Ibuprofen', 1, 7.99, RUST, 'days 1 to 7'),
              (1, 'Gastroenteritis', 6, 8, GREY, 'from day 6'),
              (0, 'Lisinopril', -10.5, 8, TEAL_MID, 'long-standing')]
    for y, lab, a0, a1, c, note_ in tracks:
        axe.barh(y, a1 - a0, left=a0, height=0.5, color=c, lw=0)
        axe.text(-10.8, y, lab, ha='right', va='center', fontsize=7.5)
    axe.text(-7.7, 3, 'doubled 9 days before day 1', ha='left', va='center', fontsize=6.8, color=INK)
    axe.text(4.4, 2, 'days 1 to 7', ha='right', va='center', fontsize=6.8, color='white', fontweight='bold')
    axe.text(8.3, 0.5, 'all withheld on\nadmission, day 8', ha='left', va='center', fontsize=6.8, color=GREY,
             style='italic')
    # creatinine
    axc.axhline(98, color=TEAL, lw=0.8, ls=(0, (3, 2)))
    axc.text(-10.3, 103, 'baseline 98, four months earlier', fontsize=6.8, color=TEAL, va='bottom')
    d, cr, k = [5, 8, 12], [139, 248, 141], [5.4, 6.0, 4.6]
    axc.plot(d, cr, color=SAND_DARK, marker='o', ms=5, lw=1.6)
    for x, v, kk, dx, dy, ha, va in zip(d, cr, k, [0.35, 0, 0], [-6, 8, -10], ['left', 'center', 'center'],
                                         ['top', 'bottom', 'top']):
        axc.text(x + dx, v + dy, f'{v}  (K {kk})', fontsize=7.2, color=INK, ha=ha, va=va)
    axc.text(4.8, 200, 'creatinine already up\nby about 40% on day 5,\nbefore the gastroenteritis', fontsize=6.8,
             color=RUST, ha='right', va='center', style='italic')
    axc.set_ylim(70, 280)
    axc.set_yticks([100, 150, 200, 250])
    axc.set_ylabel('Creatinine (µmol/L)', fontsize=8)
    axc.set_xticks([-8, 1, 5, 8, 12])
    axc.set_xlabel('Day', fontsize=8)
    save(fig, 'fig09_6')


if __name__ == '__main__':
    fig09_1(); fig09_2(); fig09_3(); fig09_4(); fig09_5(); fig09_6()
