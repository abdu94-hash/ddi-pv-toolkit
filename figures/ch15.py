# Figures for Chapter 15.
from figlib import *
from matplotlib.patches import Rectangle


def fig15_3():
    """Three ways of coding the opening tacrolimus case and what later searches retrieve."""
    H = 3.15
    fig, ax = diagram(H)
    lx = 0.1
    cx = [1.75, 2.93, 4.11]
    cw = 1.1
    cards = [
        ('A. Interaction dropped', 'Posaconazole: concomitant. Tremor; AKI', 'grey'),
        ('B. Interaction only', 'Both drugs: interacting. Drug interaction', 'grey'),
        ('C. Worked Case 15.1', 'Both drugs: interacting. Drug interaction; Tremor; AKI; Headache; Nausea; '
         'Immunosuppressant drug level increased', 'light'),
    ]
    ct, ch = 2.05, 0.98
    for x, (t, s, st) in zip(cx, cards):
        box(ax, x, ct, cw, ch, s, style=st, size=6.8, title=t, align='left', wrapw=25)
    text(ax, lx, ct + ch - 0.06, 'How the case\nis coded', size=8, bold=True, ha='left', va='top', color=TEAL)
    text(ax, lx, ct + ch - 0.5, 'Drug roles and\nMedDRA terms (PTs)', size=7, ha='left', va='top', color=GREY, italic=True)
    searches = ['Interaction cases\n(PT Drug interaction)', 'Posaconazole as interacting\nor suspect drug',
                'Tacrolimus with tremor\nor kidney injury', 'Raised tacrolimus\nconcentration']
    found = [(0, 1, 1), (0, 1, 1), (1, 0, 1), (0, 0, 1)]
    rh = 0.42
    y0 = ct - 0.14
    text(ax, lx, y0 - 0.02, 'Later search', size=8, bold=True, ha='left', color=TEAL)
    for x in cx:
        text(ax, x + cw / 2, y0 - 0.02, 'found?', size=7, color=GREY, italic=True)
    for k, (s, f) in enumerate(zip(searches, found)):
        y = y0 - (k + 1) * rh + 0.08
        if k % 2 == 0:
            ax.add_patch(Rectangle((lx - 0.02, y - rh / 2 + 0.02), cx[-1] + cw - lx + 0.04, rh - 0.04,
                                   fc=TEAL_LIGHT, ec='none', alpha=0.7, zorder=0))
        text(ax, lx + 0.04, y, s, size=7.3, ha='left')
        for x, hit in zip(cx, f):
            if hit:
                ax.plot([x + cw / 2], [y], 'o', ms=8, color=TEAL, zorder=3)
            else:
                ax.plot([x + cw / 2], [y], 'o', ms=8, mfc='white', mec=RUST, mew=1.2, zorder=3)
                text(ax, x + cw / 2 + 0.12, y, 'missed', size=6.8, color=RUST, italic=True, ha='left')
    save(fig, 'fig15_3')


def fig15_5():
    """Worked Case 15.1 (fictional): chronology anchored to the precipitant's start (day 1)."""
    fig = plt.figure(figsize=(TEXT_W, 3.75))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.9, 1.55, 1.0], hspace=0.12,
                          left=0.2, right=0.97, top=0.97, bottom=0.12)
    axd, axt, axc = [fig.add_subplot(gs[i]) for i in range(3)]
    xb = -1.2  # baseline position (21 April, day -12), axis broken before day 1
    xlim = (-2.0, 10.8)
    # drug bands
    axd.set_xlim(*xlim); axd.set_ylim(0, 2); axd.axis('off')
    def band(a, b, y, color, label='', tc='white'):
        axd.add_patch(Rectangle((a, y - 0.32), b - a, 0.64, fc=color, ec='none'))
        if label:
            axd.text((a + b) / 2, y, label, ha='center', va='center', fontsize=7, color=tc, fontweight='bold')
    band(xb - 0.6, 5.5, 1.45, TEAL, '3 mg twice daily')
    axd.text(6.5, 1.45, 'withheld', ha='center', va='center', fontsize=6.8, color=GREY, style='italic')
    band(7.5, 10.6, 1.45, TEAL_MID, '1 mg twice daily', tc=INK)
    band(0.5, 10.6, 0.5, RUST, '300 mg twice on day 1, then once daily; continued')
    axd.text(-2.0, 1.45, 'Tacrolimus', ha='right', va='center', fontsize=8, transform=axd.transData)
    axd.text(-2.0, 0.5, 'Posaconazole', ha='right', va='center', fontsize=8, transform=axd.transData)
    # trough
    axt.axhspan(6, 10, color=TEAL_LIGHT, zorder=0)
    axt.text(2.5, 8, 'target 6–10', fontsize=6.8, color=TEAL, ha='center', va='center', style='italic')
    tx, ty = [xb, 6, 8, 10], [8.1, 22.4, 11.6, 8.4]
    axt.plot(tx, ty, 'o', color=TEAL, ms=5, zorder=3)
    for x, v in zip(tx, ty):
        c = RUST if v > 20 else INK
        axt.text(x + 0.25, v + 0.6, f'{v}', fontsize=7.5, color=c, fontweight='bold' if v > 20 else 'normal', va='bottom')
    axt.plot([6], [22.4], 'o', color=RUST, ms=5, zorder=4)
    axt.set_ylim(0, 31); axt.set_xlim(*xlim)
    axt.set_ylabel('Trough\n(ng/mL)', fontsize=8)
    # creatinine
    cx, cy = [xb, 6, 10], [104, 189, 121]
    axc.plot(cx, cy, 'o', color=TEAL, ms=5, zorder=3)
    axc.plot([6], [189], 'o', color=RUST, ms=5, zorder=4)
    for x, v in zip(cx, cy):
        c = RUST if v > 150 else INK
        axc.text(x + 0.25, v + 6, f'{v}', fontsize=7.5, color=c, fontweight='bold' if v > 150 else 'normal', va='bottom')
    axc.set_ylim(60, 240); axc.set_xlim(*xlim)
    axc.set_ylabel('Creatinine\n(µmol/L)', fontsize=8)
    for a in (axt, axc):
        a.spines[['top', 'right']].set_visible(False)
        a.tick_params(length=3, width=0.6)
        # events
        for d, col in [(4, GREY), (6, RUST)]:
            a.axvline(d, color=col, lw=0.7, ls=(0, (2, 2)), zorder=1)
    axt.text(4 - 0.12, 30.5, 'tremor', fontsize=6.8, color=GREY, ha='right', va='top', style='italic')
    axt.text(6 + 0.12, 30.5, 'admitted: AKI', fontsize=6.8, color=RUST, ha='left', va='top', style='italic')
    axt.set_xticks([]); axt.spines['bottom'].set_visible(False)
    ticks = [xb] + list(range(1, 11))
    labels = ['21 Apr'] + [str(d) for d in range(1, 11)]
    axc.set_xticks(ticks, labels)
    axc.set_xlabel('Day of posaconazole (day 1 = 4 May)', fontsize=8)
    # axis break marks between baseline and day 1
    for a in (axc,):
        for dx in (-0.06, 0.06):
            a.plot([-0.1 + dx - 0.08, -0.1 + dx + 0.08], [55, 65], color=GREY, lw=0.7, clip_on=False, zorder=5)
    fig.align_ylabels([axt, axc])
    save(fig, 'fig15_5')


LAYER = {'R': ('Reported', TEAL_LIGHT, TEAL), 'O': ('Opinion', SAND, SAND_DARK),
         'S': ('Sender', RUST_LIGHT, RUST)}
KEYT = {'R': 'Reported information', 'O': "Reporter's opinion", 'S': "Sender's assessment"}


def _tag(ax, x, y, key, w=None):
    lab, fc, ec = LAYER[key]
    w = w or (0.13 + len(lab) * 0.052)
    ax.add_patch(matplotlib.patches.FancyBboxPatch((x, y - 0.085), w, 0.17, boxstyle='round,pad=0,rounding_size=0.05',
                 fc=fc, ec=ec, lw=0.7, zorder=3))
    text(ax, x + w / 2, y, lab, size=6.6, color=ec, bold=True)
    return x + w + 0.05


def fig15_1():
    """Three layers of content and where each goes in the ICSR; who reads which part."""
    H = 3.34
    fig, ax = diagram(H)
    # layer key across the top
    descr = {'R': 'what the primary source said or documented', 'O': 'what the reporter believes about cause',
             'S': 'what the company or authority infers'}
    kx = 0.1
    for k in 'ROS':
        w = 1.62
        box(ax, kx, 2.72, w, 0.54, descr[k], style={'R': 'light', 'O': 'sand', 'S': 'rust'}[k], size=7, align='left',
            title=KEYT[k], wrapw=32)
        kx += w + 0.12
    # ICSR blocks
    bx, bw = 0.1, 3.78
    groups = [('Structured fields', 1.18, [('Drugs, doses, dates', 'R'), ('Drug roles: suspect, interacting, concomitant', 'O'),
                                           ('Event terms, incl. the PT Drug interaction', 'RO'), ('Test results', 'R')]),
              ('Free text', 0.08, [('Narrative: facts; opinion, attributed', 'RO'),
                                   ("Sender's comment and diagnosis (section H)", 'S')])]
    rh = 0.27
    for title, y0, items in groups:
        hgt = 0.3 + rh * len(items) + 0.06
        ax.add_patch(matplotlib.patches.FancyBboxPatch((bx, y0), bw, hgt, boxstyle='round,pad=0,rounding_size=0.06',
                     fc='white', ec=RULE, lw=0.9, zorder=1))
        text(ax, bx + 0.12, y0 + hgt - 0.16, title, size=8, bold=True, color=TEAL, ha='left')
        for i, (lab, keys) in enumerate(items):
            yy = y0 + hgt - 0.38 - i * rh
            text(ax, bx + 0.14, yy, lab, size=7.2, ha='left')
            tx = bx + bw - 0.08 - sum(0.13 + len(LAYER[k][0]) * 0.052 + 0.05 for k in keys) + 0.05
            for k in keys:
                tx = _tag(ax, tx, yy, k)
        # reader note
        rx = bx + bw + 0.22
        arrow(ax, (rx - 0.02, y0 + hgt / 2), (bx + bw + 0.02, y0 + hgt / 2), color=GREY, style='<|-')
        reader = ('Read by databases: signal detection, line listings, aggregate reports' if title.startswith('Struct')
                  else 'Read by a person reviewing the case')
        box(ax, rx, y0 + hgt / 2 - 0.36, 5.2 - rx, 0.72, reader, style='grey', size=7, wrapw=20)
    save(fig, 'fig15_1')


def fig15_2():
    """What the E2B(R3) role field records versus what the narrative and comment must state."""
    H = 2.45
    fig, ax = diagram(H)
    # left: role field
    lx, lw = 0.1, 2.0
    text(ax, lx + lw / 2, 2.28, 'What the role field records', size=8, bold=True, color=TEAL)
    for i, nm in enumerate(['Tacrolimus', 'Posaconazole']):
        y = 1.6 - i * 0.58
        box(ax, lx + 0.1, y, lw - 0.2, 0.42, '', style='light')
        text(ax, lx + 0.22, y + 0.21, nm, size=8, ha='left', bold=True)
        _tag(ax, lx + lw - 0.86, y + 0.21, 'R', w=0.66)
        ax.texts[-1].set_text('interacting')
    text(ax, lx + lw / 2, 0.7, 'symmetric: no direction,\nno combination', size=6.8, color=GREY, italic=True)
    # right: words
    rx = 2.45
    text(ax, rx + 1.37, 2.28, 'What the narrative and comment must add', size=8, bold=True, color=RUST)
    nodes = [('Posaconazole', 'precipitant', 'teal'), ('CYP3A4 inhibited', '', 'white'), ('Tacrolimus exposure up', 'object', 'teal')]
    nw, ng = 0.78, 0.18
    for i, (t, sub, st) in enumerate(nodes):
        x = rx + i * (nw + ng)
        box(ax, x, 1.45, nw, 0.52, t, style=st, size=7.2, wrapw=14)
        if sub:
            text(ax, x + nw * 0.35, 1.33, sub, size=6.8, color=GREY, italic=True)
        if i:
            arrow(ax, (x - ng + 0.02, 1.71), (x - 0.02, 1.71))
    box(ax, rx, 0.55, 2.74, 0.5, 'Tremor and AKI; the combination assessed as a plausible and important contributor',
        style='rust', size=7, wrapw=48)
    arrow(ax, (rx + 2 * (nw + ng) + nw * 0.8, 1.43), (rx + 2 * (nw + ng) + nw * 0.8, 1.07), color=RUST)
    text(ax, TEXT_W / 2, 0.18, 'E2B(R3) guide: select "interacting" for every drug the reporter suspects of interacting [5].',
         size=6.8, color=GREY, italic=True)
    save(fig, 'fig15_2')


def fig15_4():
    """Size of the posaconazole-tacrolimus interaction: volunteers, patients, and this case (refs [9], [10])."""
    import numpy as np
    rows = [('Healthy volunteers, single tacrolimus dose:', None),
            ('Cmax [9]', 2.21, None), ('AUC [9]', 4.58, None),
            ('Solid organ recipients, dose-corrected trough:', None),
            ('with posaconazole, mean [10]', 4.4, None), ('with voriconazole, mean [10]', 5.0, None),
            ('individual range, both azoles [10]', None, (1, 20)),
            ('Worked Case 15.1, trough on unchanged dose:', None),
            ('8.1 to 22.4 ng/mL', 2.8, None)]
    fig, a = chart(2.9)
    fig.subplots_adjust(left=0.44, right=0.95, top=0.97, bottom=0.17)
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - 1 - i
        if r[1] is None and (len(r) == 2 or r[2] is None):
            a.text(-0.02, y, r[0], transform=a.get_yaxis_transform(), ha='right', va='center', fontsize=7.3,
                   fontweight='bold', color=TEAL)
            continue
        lab, v, rng = r
        a.text(-0.02, y, lab, transform=a.get_yaxis_transform(), ha='right', va='center', fontsize=7.2)
        if rng:
            a.plot(rng, [y, y], color=TEAL_MID, lw=4, solid_capstyle='butt')
            a.text(4.5, y + 0.36, 'no change to about 20-fold', ha='center', va='center', fontsize=6.8, color=GREY, style='italic')
            continue
        col = RUST if 'Case' in rows[i - 1][0] else TEAL
        a.plot([v], [y], 'o', color=col, ms=6)
        lbl = {2.21: '+121%', 4.58: '+358%', 2.8: 'about 2.8-fold'}.get(v, f'{v}-fold')
        a.text(v * 1.14, y, lbl, va='center', fontsize=7, color=col, fontweight='bold' if col == RUST else 'normal')
    a.axvline(1, color=GREY, lw=0.8)
    a.set_xscale('log'); a.set_xlim(0.85, 60)
    a.set_xticks([1, 2, 5, 10, 20], ['1', '2', '5', '10', '20'])
    a.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    a.set_yticks([]); a.spines['left'].set_visible(False)
    a.set_ylim(-0.6, n - 0.4)
    a.set_xlabel('Fold increase with the azole (log scale; 1 = no change)', fontsize=7.5)
    save(fig, 'fig15_4')


if __name__ == '__main__':
    fig15_1(); fig15_2(); fig15_3(); fig15_4(); fig15_5()
