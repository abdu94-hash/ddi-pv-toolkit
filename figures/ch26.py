# Figures for Chapter 26 (case series and committee; ravolixan is fictional).
from figlib import *


def fig26_1():
    """Chronology from the data lock point to the committee and the proposed steps after it."""
    fig, ax = diagram(3.1)
    yl = 2.05
    ev = [('30 Jun', 'DLP: 47 QT reports, 21 with an inhibitor', TEAL),
          ('28 Jul', 'signal validated', TEAL),
          ('3 Sep', 'first trial torsade (RVX-305)', TEAL),
          ('12 Sep', 'SUSAR reported by this date', TEAL),
          ('15 Sep', 'assessment report: high priority', TEAL),
          ('30 Oct', 'reduced-dose follow-up due; 2 of 4 answered', TEAL),
          ('Nov', 'Safety Review Committee', RUST),
          ('end Nov', 'fluconazole 400 mg simulations due', GREY)]
    x0, x1 = 0.6, 4.85
    xs = [x0 + k * (x1 - x0) / (len(ev) - 1) for k in range(len(ev))]
    ax.plot([0.2, 5.1], [yl, yl], color=GREY, lw=1.0, zorder=1)
    text(ax, 0.12, yl + 0.95, '2026', size=7.5, color=GREY, bold=True, ha='left')
    for k, ((d, s, c), x) in enumerate(zip(ev, xs)):
        up = k % 2 == 0
        ax.plot([x], [yl], 'o', ms=6 if c == RUST else 4.5, color=c, zorder=3)
        ax.plot([x, x], [yl + (0.06 if up else -0.06), yl + (0.2 if up else -0.2)], color=RULE, lw=0.8)
        text(ax, x, yl + (0.3 if up else -0.3), d, size=7.5, bold=True, color=c)
        text(ax, x, yl + (0.42 if up else -0.42), s, size=6.8, color=INK, wrapw=19, va='bottom' if up else 'top')
    # proposed steps after the committee
    by, bh = 0.32, 0.6
    steps = ['Labeling proposals submitted; effectiveness plan agreed', 'DHPC to dermatology, primary care, pharmacists',
             'Reassessment at 6 and 12 months', 'Cumulative review in the next PBRER']
    bw, gap = 1.12, 0.2
    bx0 = (TEXT_W - (4 * bw + 3 * gap)) / 2
    for k, s in enumerate(steps):
        bx = bx0 + k * (bw + gap)
        box(ax, bx, by, bw, bh, s, style='white', size=6.8, wrapw=24, lw=0.9)
        if k < 3:
            arrow(ax, (bx + bw + 0.02, by + bh / 2), (bx + bw + gap - 0.02, by + bh / 2), color=GREY)
    xc = xs[6]
    ax.plot([xc, xc], [yl - 0.08, 1.2], color=RUST, lw=0.9, ls=(0, (3, 2)))
    ax.plot([xc, bx0 + bw / 2], [1.2, 1.2], color=RUST, lw=0.9, ls=(0, (3, 2)))
    arrow(ax, (bx0 + bw / 2, 1.2), (bx0 + bw / 2, by + bh + 0.02), color=RUST, lw=0.9, ls=(0, (3, 2)))
    text(ax, 1.65, 1.12, 'if the committee approves the recommendation', size=6.8, color=RUST, italic=True,
         ha='left', va='top')
    save(fig, 'fig26_1')


def fig26_3():
    """The 21 inhibitor reports, one square each: overlap, information quality, electrolytes."""
    fig, ax = diagram(2.05)
    sq, g = 0.14, 0.025
    xs0 = 1.55
    rows = [(1.62, 'Overlap of the two drugs',
             [(11, TEAL, 'confirmed 11'), (5, TEAL_MID, 'probable 5'), (4, RULE, 'unknown 4'), (1, RUST, 'none 1')]),
            (1.0, 'Information quality',
             [(7, TEAL, 'grade A 7'), (9, TEAL_MID, 'grade B 9'), (5, RULE, 'grade C 5')]),
            (0.38, 'Hypokalemia or\nhypomagnesemia',
             [(9, SAND_DARK, 'documented in 9'), (12, '#EEF1F2', '')])]
    for y, lab, segs in rows:
        text(ax, 0.1, y + sq / 2, lab, size=7.8, ha='left', color=INK, bold=True)
        i = 0
        for n, c, slab in segs:
            xa = xs0 + i * (sq + g)
            for j in range(n):
                x = xs0 + (i + j) * (sq + g)
                ax.add_patch(plt.Rectangle((x, y), sq, sq, fc=c, ec='white' if c != '#EEF1F2' else RULE,
                                           lw=0.6, zorder=2))
            xb = xs0 + (i + n) * (sq + g) - g
            if slab:
                text(ax, (xa + xb) / 2, y - 0.1, slab, size=6.8, color=INK, va='top')
            i += n
    ax.plot([xs0 + 20 * (sq + g) + sq / 2], [1.62 + sq / 2], marker='x', color='white', ms=4, mew=1.2, zorder=3)
    text(ax, xs0, 1.98, '21 reports co-reporting a CYP3A4 inhibitor; one square per report', size=7, color=GREY,
         italic=True, ha='left')
    save(fig, 'fig26_3')


def fig26_5():
    """Every source bears on plausibility; none supplies the denominator needed for frequency."""
    fig, ax = diagram(3.45)
    src = [('Interaction studies and PBPK', 'AUC ratios 2.0 to 4.2'),
           ('Thorough QT study', '6 ms at usual dose; 18 ms at about 4-fold'),
           ('Development program', 'no torsade; strong inhibitors excluded'),
           ('RVX-305 trial case', 'diltiazem; potassium 3.1 mmol/L'),
           ('Spontaneous series', '21 reports; overlap confirmed in 11'),
           ('Literature', 'torsade is usually multifactorial')]
    xl, wl, bh, gap = 0.1, 1.95, 0.44, 0.06
    ytop = 2.9
    ys = [ytop - k * (bh + gap) for k in range(len(src))]
    for (t, s), y in zip(src, ys):
        box(ax, xl, y, wl, bh, s, style='light', size=6.6, title=t, align='left', wrapw=44, pad=0.04)
    xbus = 2.2
    for y in ys:
        ax.plot([xl + wl + 0.01, xbus], [y + bh / 2] * 2, color=TEAL, lw=1.0)
    ax.plot([xbus, xbus], [ys[-1] + bh / 2, ys[0] + bh / 2], color=TEAL, lw=1.0)
    xr, wr = 2.85, 2.35
    box(ax, xr, 2.3, wr, 0.88,
        'Strong inhibitors: supported, with additional risk factors in most cases. '
        'QT-prolonging moderate inhibitors: uncertain; dose reduction does not address their own QT effect.',
        style='light', size=6.9, title='Plausibility of a ravolixan contribution', align='left', wrapw=46)
    box(ax, xr, 0.72, wr, 0.92,
        'Cannot be estimated: no count of co-exposed users. The development bound (about 1 in 1,000) '
        'does not cover the combination. Needed: drug utilization data.',
        style='rust', size=6.9, title='Frequency in co-exposed patients', align='left', wrapw=46)
    arrow(ax, (xbus, 2.74), (xr - 0.02, 2.74), color=TEAL)
    arrow(ax, (xbus, 1.18), (xr - 0.02, 1.18), color=GREY, ls=(0, (3, 2)))
    text(ax, xbus + 0.08, 2.8, 'all sources', size=6.6, color=TEAL, ha='left', italic=True, va='bottom')
    text(ax, xbus + 0.08, 1.24, 'no\ndenominator', size=6.6, color=GREY, ha='left', italic=True, va='bottom')
    note(ax, 'The decision adds what the evidence does not settle: preventability, alternatives, and burden.',
         y=0.15, size=6.8)
    save(fig, 'fig26_5')


def fig26_2():
    """Rule of three: the upper 95% bound when no events are seen in n patients (3/n) [5]."""
    import numpy as np
    fig, ax = chart(2.45)
    n = np.logspace(np.log10(300), np.log10(30000), 300)
    ub = 3000 / n  # events per 1,000 patients
    ax.fill_between(n, 0, ub, color=RUST_LIGHT, lw=0)
    ax.plot(n, ub, color=RUST, lw=1.6)
    ax.set_xscale('log')
    ax.plot(2900, 3000 / 2900, 'o', color=TEAL, ms=6, zorder=3)
    ax.annotate('Ravolixan development: no torsade\nin about 2,900 patients; bound about\n1 in 1,000 (strong inhibitors excluded)',
                xy=(2900, 3000 / 2900), xytext=(4200, 4.4), fontsize=7.5, color=TEAL, va='center',
                arrowprops=dict(arrowstyle='-', color=TEAL, lw=0.8))
    ax.text(420, 1.4, 'Rates in the shaded area\ncannot be excluded', fontsize=7, color=RUST, style='italic')
    ax.set_xlim(300, 30000)
    ax.set_ylim(0, 10.5)
    ax.set_xticks([300, 1000, 3000, 10000, 30000])
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:,.0f}'))
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel('Patients observed with no event (n)', fontsize=8)
    ax.set_ylabel('Upper 95% bound,\nevents per 1,000 patients', fontsize=8)
    fig.subplots_adjust(left=0.13, right=0.97, top=0.96, bottom=0.18)
    save(fig, 'fig26_2')


def fig26_4():
    """Reconciling the fluconazole cases after dose reduction: three explanations and what follow-up showed."""
    fig, ax = diagram(3.3)
    box(ax, 0.1, 2.25, 1.75, 0.8,
        '3 fluconazole cases despite the 20 mg dose; 20 mg with fluconazole gives about 1.3 times usual exposure',
        style='rust', size=6.9, title='The inconsistency', align='left', wrapw=34)
    box(ax, 0.1, 0.55, 1.75, 1.4,
        'Answers for 2 of the 4 reduced-dose cases: ravolixan 20 mg with a single 150 mg fluconazole dose and '
        'hypokalemia; ravolixan 20 mg with fluconazole 200 mg daily for 10 days. Neither above 200 mg. '
        '2 responses outstanding.',
        style='white', size=6.9, title='Follow-up by 30 October', align='left', wrapw=34)
    expl = [('Fluconazole prolongs QT itself', 'QTc rose 10.7 ms (7.2 to 14.1) with ciprofloxacin [9]; '
             'dose reduction does not address it', 'gains weight', TEAL),
            ('Fluconazole dose above 200 mg', 'Would exceed the PBPK prediction; 400 mg simulations '
             'due end of November', 'weaker for the 2 answered', GREY),
            ('Circumstances of use', 'Ill or hospitalized patients with electrolyte disturbances or other QT drugs: '
             'cases possible without any interaction', 'open', SAND_DARK)]
    xe, we, he = 2.2, 2.0, 0.78
    ys = [2.27, 1.35, 0.43]
    for (t, s, verdict, c), y in zip(expl, ys):
        box(ax, xe, y, we, he, s, style='light', size=6.8, title=t, align='left', wrapw=40)
        text(ax, xe + we + 0.1, y + he / 2, verdict, size=7, color=c, bold=True, ha='left', wrapw=12)
        arrow(ax, (1.87, 2.65), (xe - 0.02, y + he / 2), color=GREY, lw=0.9)
    text(ax, xe + we + 0.1, 3.12, 'After follow-up', size=7, color=GREY, italic=True, ha='left')
    note(ax, 'Case counts by inhibitor also depend on unknown co-prescription: 7 versus 9 is not a difference in risk.',
         y=0.15, size=6.7)
    save(fig, 'fig26_4')


if __name__ == '__main__':
    fig26_1(); fig26_2(); fig26_3(); fig26_4(); fig26_5()
