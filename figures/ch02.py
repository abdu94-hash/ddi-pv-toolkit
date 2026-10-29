# Figures for Chapter 2.
from figlib import *


def inhibit(ax, p, q, color=RUST, lw=1.2, ls='-', bar=0.09):
    """Line from p to q ending in a flat bar (inhibition)."""
    import math
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=1, solid_capstyle='butt')
    a = math.atan2(q[1] - p[1], q[0] - p[0]) + math.pi / 2
    dx, dy = bar * math.cos(a), bar * math.sin(a)
    ax.plot([q[0] - dx, q[0] + dx], [q[1] - dy, q[1] + dy], color=color, lw=lw + 0.6, zorder=1,
            solid_capstyle='butt')


def fig02_2():
    """Colchicine elimination routes, where clarithromycin acts, and where renal impairment acts."""
    fig, ax = diagram(3.1)
    # middle row: liver route, colchicine, kidney route
    my, mh = 1.25, 0.72
    box(ax, 0.1, my, 1.6, mh, 'CYP3A4 metabolism and P-gp efflux', style='light', size=8, title='Hepatic route')
    box(ax, 2.05, my + 0.08, 1.2, mh - 0.16, 'Colchicine\nin the body', style='teal', size=8.5)
    box(ax, 3.6, my, 1.6, mh, 'Elimination by the kidney, partly P-gp-mediated secretion', style='light', size=8,
        title='Renal route')
    arrow(ax, (2.03, my + mh / 2), (1.72, my + mh / 2), color=TEAL)
    arrow(ax, (3.27, my + mh / 2), (3.58, my + mh / 2), color=TEAL)
    text(ax, 1.875, my + mh / 2 + 0.12, 'cleared', size=6.5, color=GREY, italic=True)
    text(ax, 3.425, my + mh / 2 + 0.12, 'cleared', size=6.5, color=GREY, italic=True)
    # top row: clarithromycin (precipitant) and renal impairment (patient factor)
    ty, th = 2.4, 0.58
    box(ax, 0.1, ty, 2.3, th, 'Inhibits CYP3A4 and P-gp', style='rust', size=8, title='Clarithromycin')
    box(ax, 2.9, ty, 2.3, th, 'Removes much of the renal route', style='sand', size=8,
        title='Renal impairment')
    inhibit(ax, (0.9, ty - 0.02), (0.9, my + mh + 0.06))
    inhibit(ax, (2.2, ty - 0.02), (3.85, my + mh + 0.06), ls=(0, (3, 2)))
    text(ax, 2.27, 2.1, 'may also inhibit', size=6.5, color=RUST, italic=True, ha='left')
    inhibit(ax, (4.75, ty - 0.02), (4.75, my + mh + 0.06), color=SAND_DARK)
    # bottom row: consequence
    by, bh = 0.12, 0.72
    box(ax, 1.95, by + 0.1, 1.4, bh - 0.2, 'Colchicine exposure rises', style='white', size=8.5, bold=True)
    box(ax, 3.6, by, 1.6, bh, 'GI symptoms first; then myopathy or neuromyopathy, marrow suppression, multiorgan failure',
        style='accent', size=7.5, bold=False)
    arrow(ax, (2.65, my + 0.06), (2.65, by + bh - 0.08), color=GREY)
    arrow(ax, (3.37, by + bh / 2), (3.58, by + bh / 2), color=RUST)
    text(ax, 0.1, by + bh / 2, 'What is left? When both routes are reduced, little capacity remains to compensate.',
         wrapw=26, size=7.5, color=GREY, italic=True, ha='left')
    save(fig, 'fig02_2')


def fig02_4():
    """Calculation 2.1 drawn as clearance bars: what the inhibitor removes and what is left."""
    fig, ax = chart(2.55)
    rows = [  # label, hepatic, renal, hepatic removed by inhibitor, renal removed by impairment
        ('Normal kidneys\nalone', 0.60, 0.40, 0, 0),
        ('Normal kidneys\nwith inhibitor', 0.12, 0.40, 0.48, 0),
        ('Renal clearance −75%\nalone', 0.60, 0.10, 0, 0.30),
        ('Renal clearance −75%\nwith inhibitor', 0.12, 0.10, 0.48, 0.30),
    ]
    ys = [3.35, 2.45, 1.0, 0.1]
    hgt = 0.56
    for (lab, hep, ren, hrem, rrem), y in zip(rows, ys):
        ax.barh(y, hep, height=hgt, color=TEAL, zorder=2)
        if hrem:
            ax.barh(y, hrem, left=hep, height=hgt, color='white', ec=TEAL_MID, ls=(0, (3, 2)), lw=0.8, zorder=2)
        x = hep + hrem
        ax.barh(y, ren, left=x, height=hgt, color=TEAL_MID, zorder=2)
        if rrem:
            ax.barh(y, rrem, left=x + ren, height=hgt, color='white', ec=SAND_BORDER, ls=(0, (3, 2)), lw=0.8, zorder=2)
        tot = hep + ren
        ax.text(1.04, y, f'CL {tot:.2f}', va='center', fontsize=8, color=INK, fontweight='bold')
    ax.text(0.30, ys[0], 'hepatic 0.60', ha='center', va='center', fontsize=7.5, color='white')
    ax.text(0.80, ys[0], 'renal 0.40', ha='center', va='center', fontsize=7.5, color=INK)
    ax.text(0.36, ys[1], 'removed by inhibitor', ha='center', va='center', fontsize=7, color=GREY, style='italic')
    ax.text(0.85, ys[2], 'lost to\nimpairment', ha='center', va='center', fontsize=6.5, color=SAND_DARK,
            style='italic', linespacing=1.0)
    # AUC ratios
    kw = dict(va='center', fontsize=7.5, color=RUST, fontweight='bold')
    ax.text(1.27, ys[1], 'AUC ratio ≈ 1.9', **kw)
    ax.text(1.27, ys[3] + 0.13, 'AUC ratio ≈ 3.2 vs own baseline', **kw)
    ax.text(1.27, ys[3] - 0.15, '≈ 4.5 vs normal kidneys alone', **kw)
    ax.set_yticks(ys, [r[0] for r in rows], fontsize=8)
    ax.set_xlim(0, 1.95); ax.set_ylim(-0.35, 3.75)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel('Total clearance (relative units)', fontsize=8.5)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    ax.spines['bottom'].set_bounds(0, 1.0)
    ax.xaxis.set_label_coords(0.5 / 1.95, -0.16)
    ax.axhline(1.72, color=RULE, lw=0.6, xmin=0, xmax=0.53)
    fig.tight_layout()
    save(fig, 'fig02_4')


def fig02_5():
    """Same combination, two patients: the six-dimension profile without a score."""
    fig, ax = diagram(4.6)
    W = TEXT_W
    lx, lw_ = 0.08, 1.32
    cw, gap = 1.84, 0.08
    xa = lx + lw_ + gap
    xb = xa + cw + gap
    styles = {'S': ('light', 'Supports'), 'L': ('sand', 'Limited'), 'A': ('grey', 'Against'),
              'P': ('sand', 'Partly against')}
    rows = [
        ('1. Mechanistic plausibility', ('S', 'established CYP3A4 and P-gp mechanism'), ('S', 'same as Patient A')),
        ('2. Evidence strength', ('L', 'shows exposure change; says little about mild diarrhea'), ('S', 'exposure change and serious harm documented')),
        ('3. Exposure relevance', ('L', 'full-dose overlap, but one 7-day course'), ('S', 'full-dose overlap for six days before admission')),
        ('4. Patient susceptibility', ('A', 'eGFR 88; no other strong inhibitor'), ('S', 'eGFR 24 (stage 4 CKD); dose high for this renal function')),
        ('5. Clinical consequence', ('L', 'mild, reversible, non-specific diarrhea'), ('S', 'typical toxicity pattern; hospitalized')),
        ('6. Actionability', ('L', 'missed dose adjustment: a preventability point only'), ('S', 'combination advised against in renal impairment')),
        ('Competing explanations', ('A', 'diarrhea common with either drug or the infection'), ('P', 'sepsis, dehydration, allopurinol')),
    ]
    top = 4.12
    rh, rg = 0.43, 0.06
    text(ax, xa + cw / 2, top + 0.2, 'Patient A', size=9, bold=True, color=TEAL)
    text(ax, xb + cw / 2, top + 0.2, 'Patient B', size=9, bold=True, color=TEAL)
    text(ax, lx, top + 0.2, 'Same flag for both: major', size=7.5, color=GREY, italic=True, ha='left')
    for k, (dim, a, b) in enumerate(rows):
        y = top - (k + 1) * rh - k * rg - (0.1 if k == 6 else 0)
        is_sus = k == 3
        text(ax, lx, y + rh / 2, dim, size=8, ha='left', bold=is_sus, color=RUST if is_sus else INK, wrapw=19)
        for (code, why), x in ((a, xa), (b, xb)):
            st, word = styles[code]
            fill, edge, _, _ = STYLES[st]
            ax.add_patch(FancyBboxPatch((x, y), cw, rh, boxstyle='round,pad=0,rounding_size=0.05',
                                        fc=fill, ec=RUST if is_sus else edge, lw=1.3 if is_sus else 0.8, zorder=2))
            ax.text(x + 0.08, y + rh - 0.05, word, ha='left', va='top', fontsize=7.5, fontweight='bold',
                    color=TEAL if code == 'S' else (GREY if code == 'A' else SAND_DARK), zorder=3)
            ax.text(x + 0.08, y + rh - 0.18, wrap(why, 38), ha='left', va='top',
                    fontsize=7, color=INK, zorder=3, linespacing=1.1)
    # separator before competing explanations
    ysep = top - 6 * rh - 5 * rg - 0.08
    ax.plot([lx, W - 0.08], [ysep, ysep], color=RULE, lw=0.6)
    # overall statements
    sy, sh = 0.12, 0.5
    text(ax, lx, sy + sh / 2, 'Statement', size=8, ha='left', bold=True)
    box(ax, xa, sy, cw, sh, 'possible contributor; event mild and non-specific', style='white', size=7.5)
    box(ax, xb, sy, cw, sh, 'plausible and important contributor', style='accent', size=7.5)
    save(fig, 'fig02_5')


def fig02_1():
    """Profile, not score: the same six dimensions down two paths."""
    fig, ax = diagram(3.0)
    dims = ['Mechanistic plausibility', 'Evidence strength', 'Exposure relevance', 'Patient susceptibility',
            'Clinical consequence', 'Actionability']
    bh, bg = 0.36, 0.08
    y0 = 0.3
    for k, d in enumerate(dims):
        y = y0 + (5 - k) * (bh + bg)
        box(ax, 0.08, y, 1.32, bh, d, style='light', size=7.5)
    top = y0 + 6 * bh + 5 * bg
    ax.plot([1.52, 1.52], [y0 + 0.05, top - 0.05], color=GREY, lw=1.0)
    for k in range(6):
        y = y0 + k * (bh + bg) + bh / 2
        ax.plot([1.42, 1.52], [y, y], color=GREY, lw=1.0)
    # wrong path
    uy = 2.05
    text(ax, 1.95, uy + 0.68, 'Not this', size=8, bold=True, color=RUST, ha='left')
    arrow(ax, (1.52, uy + 0.3), (1.93, uy + 0.3), color=RUST)
    box(ax, 1.95, uy, 1.15, 0.6, 'Convert each to points and add them', style='rust', size=7.5)
    arrow(ax, (3.12, uy + 0.3), (3.38, uy + 0.3), color=RUST)
    box(ax, 3.4, uy, 1.82, 0.6, 'A total presented as a probability of causation', style='accent', size=7.5, bold=False)
    text(ax, 1.95, 1.62, 'The dimensions are not independent and share no common scale; a strong mechanism '
         'cannot make up for a drug that was never taken.', size=7, color=GREY, italic=True, ha='left', wrapw=72)
    # right path
    ly = 0.3
    text(ax, 1.95, ly + 1.03, 'This', size=8, bold=True, color=TEAL, ha='left')
    arrow(ax, (1.52, ly + 0.47), (1.93, ly + 0.47), color=TEAL)
    box(ax, 1.95, ly, 1.15, 0.94, 'For each: supports, against, neutral or unknown, with a reason', style='light',
        size=7.5)
    arrow(ax, (3.12, ly + 0.47), (3.38, ly + 0.47), color=TEAL)
    box(ax, 3.4, ly, 1.82, 0.94, 'overall judgment\ndriving dimensions\nmost important uncertainty\nnext action',
        style='teal', size=7.5, bold=False, title='Relevance statement', align='left')
    text(ax, 3.4, 0.13, 'Causality of the event is judged separately.', size=7, color=GREY, italic=True, ha='left')
    save(fig, 'fig02_1')


def fig02_3():
    """Hung et al.: factors independently associated with death on concomitant therapy."""
    fig, ax = chart(2.45)
    rows = [('Longer overlap of the two drugs', 2.16, 1.41, 3.31),
            ('Baseline renal impairment', 9.1, 1.75, 47.06),
            ('Developed pancytopenia', 23.4, 4.48, 122.7)]
    ys = [2, 1, 0]
    for (lab, rr, lo, hi), y in zip(rows, ys):
        col = RUST if 'renal' in lab else TEAL
        ax.plot([lo, hi], [y, y], color=col, lw=1.6, solid_capstyle='butt', zorder=2)
        ax.plot(rr, y, 's', ms=6.5, color=col, zorder=3)
        ax.text(260, y, f'{rr:g} ({lo:g} to {hi:g})', va='center', ha='left', fontsize=8, color=INK)
    ax.axvline(1, color=GREY, lw=0.8, ls=(0, (1, 2)))
    ax.set_xscale('log')
    ax.set_xlim(0.7, 250)
    ax.set_xticks([1, 3, 10, 30, 100], ['1', '3', '10', '30', '100'])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_yticks(ys, [r[0] for r in rows], fontsize=8)
    ax.set_ylim(-0.6, 2.9)
    ax.text(260, 2.62, 'RR (95% CI)', ha='left', va='center', fontsize=7.5, color=GREY, fontweight='bold')
    ax.set_xlabel('Relative risk of death among patients given both drugs (log scale)', fontsize=8)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75, top=0.86)
    fig.text(0.02, 0.955, 'Deaths: 9 of 88 (10.2%) with concomitant use; 1 of 28 (3.6%) with sequential use',
             ha='left', va='center', fontsize=7.5, color=GREY, style='italic')
    save(fig, 'fig02_3')


if __name__ == '__main__':
    fig02_1(); fig02_2(); fig02_3(); fig02_4(); fig02_5()
