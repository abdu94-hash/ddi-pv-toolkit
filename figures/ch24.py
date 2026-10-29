# Figures for Chapter 24 (alerts and effectiveness; ravolixan, Network A, Database B are fictional).
from figlib import *


def fig24_1():
    """Published override rates beside the share of overrides judged appropriate (refs 2-5)."""
    rows = [('Outpatient network,\nall medication alerts [2]', 52.6, None, 'about half'),
            ('Teaching hospital,\ninpatient DDI alerts [3]', 95.1, None, None),
            ('Intensive care units,\nmedication alerts [5]', None, 81.6, '81.6%'),
            ('New commercial system,\nhighest-severity DDI alerts [4]', 87.3, 0.5, '0.5%')]
    fig, (a1, a2) = chart(2.6, ncols=2, sharey=True, gridspec_kw={'wspace': 0.12})
    ys = [3, 2, 1, 0]
    for (lab, ov, ap, aplab), y in zip(rows, ys):
        if ov is not None:
            a1.plot([0, ov], [y, y], color=RULE, lw=1.0, zorder=1)
            a1.plot(ov, y, 'o', color=TEAL, ms=6, zorder=3)
            a1.text(ov - 3, y + 0.22, f'{ov}%', ha='center', fontsize=7.5)
        else:
            a1.text(3, y, 'not reported', fontsize=7, color=GREY, style='italic', va='center')
        if y == 3:
            a2.plot([0, 50], [y, y], color=RULE, lw=1.0, zorder=1)
            a2.plot(50, y, 'o', mfc='white', mec=SAND_DARK, mew=1.4, ms=6, zorder=3)
            a2.text(50, y + 0.22, 'about half', ha='center', fontsize=7.5)
        elif ap is not None:
            a2.plot([0, ap], [y, y], color=RULE, lw=1.0, zorder=1)
            a2.plot(ap, y, 'o', color=RUST if ap < 10 else SAND_DARK, ms=6, zorder=3)
            a2.text(ap + (3 if ap < 10 else 0), y + 0.22, aplab, ha='left' if ap < 10 else 'center', fontsize=7.5)
        else:
            a2.text(3, y, 'not reported', fontsize=7, color=GREY, style='italic', va='center')
    a1.set_yticks(ys, [r[0] for r in rows], fontsize=7.3)
    for a, xl in [(a1, 'Alerts overridden, %'), (a2, 'Overrides judged appropriate, %')]:
        a.set_xlim(-4, 105)
        a.set_ylim(-0.5, 3.55)
        a.set_xticks([0, 25, 50, 75, 100])
        a.set_xlabel(xl, fontsize=7.5)
        a.spines['left'].set_visible(False)
        a.tick_params(axis='y', length=0)
    fig.subplots_adjust(left=0.29, right=0.98, top=0.97, bottom=0.17)
    save(fig, 'fig24_1')


def fig24_2():
    """Implementation barriers along the path from the label to the patient (Section 24.2)."""
    fig, ax = diagram(2.95)
    stages = [('Label update', 'MAH'), ('Knowledge base', 'vendor'), ('Prescribing system', 'health system'),
              ('Second prescriber', 'primary or urgent care'), ('Dispensing', 'pharmacy'), ('Patient', '')]
    n = len(stages)
    sw, g = 0.72, 0.14
    x0 = 0.1
    ys, sh = 1.95, 0.5
    xs = [x0 + k * (sw + g) for k in range(n)]
    for k, ((t, owner), x) in enumerate(zip(stages, xs)):
        st = 'teal' if k in (0, n - 1) else 'light'
        box(ax, x, ys, sw, sh, t, style=st, size=7.2, wrapw=12)
        if owner:
            text(ax, x + sw / 2, ys + sh + 0.12, owner, size=6.6, color=GREY, italic=True)
        if k < n - 1:
            arrow(ax, (x + sw + 0.01, ys + sh / 2), (x + sw + g - 0.01, ys + sh / 2), color=TEAL)
    fails = [(1, 1, 'Update may take months; local settings can suppress or downgrade'),
             (2, 2, 'Object drug missing from the medication list; competing low-value alerts'),
             (3, 3, 'Unfamiliar with the object drug; instruction hard to follow'),
             (4, 4, 'Pharmacy and OTC supply outside the prescribing system')]
    for a, b, s in fails:
        xa, xb = xs[a], xs[b] + sw
        box(ax, xa - 0.04, 0.62, xb - xa + 0.08, 0.98, s, style='rust', size=6.5, wrapw=15, align='center')
        ax.plot([(xa + xb) / 2] * 2, [1.62, ys - 0.02], color=RUST, lw=0.9, ls=(0, (2, 2)))
    text(ax, xs[1] - 0.04, 0.45, 'Where the instruction can fail to reach the decision', size=7, color=RUST,
         italic=True, ha='left')
    text(ax, xs[0], 0.13, 'The MAH controls only the first step; it can inform the others, not configure them.',
         size=6.8, color=GREY, italic=True, ha='left')
    save(fig, 'fig24_2')


def fig24_3():
    """What happened after each type of alert in Network A, months 1-6 (Worked Case 24.1)."""
    fig, ax = chart(2.35)
    rows = [  # (y, segments [(n, colour, label, text colour)], total)
        (2, [(84, TEAL, '84 order cancelled\nor changed', 'white'),
             (31, TEAL_MID, '31 appropriate\noverride', 'white'),
             (33, RUST, '33 confirmed\noverlap', 'white')], 148),
        (1, [(118, TEAL, '118 dose cut to 20 mg', 'white'),
             (296 - 118, '#E3E8E9', '', INK)], 296),
        (0, [(31, TEAL, '', 'white'),
             (989, RULE, '989 overridden; appropriateness not reviewed', INK)], 1020),
    ]
    for y, segs, tot in rows:
        left = 0
        for n, c, lab, tc in segs:
            w = 100 * n / tot
            ax.barh(y, w, left=left, color=c, height=0.62, edgecolor='white', linewidth=0.8)
            if lab:
                ax.text(left + w / 2, y, lab, ha='center', va='center', fontsize=7, color=tc, linespacing=1.15)
            left += w
    ax.text(101.5, 2, '43%\noverridden', va='center', fontsize=7.5, color=INK, linespacing=1.15)
    ax.text(101.5, 1, 'potassium\ntested 26%', va='center', fontsize=7.5, color=INK, linespacing=1.15)
    ax.text(101.5, 0, '97%\noverridden', va='center', fontsize=7.5, color=INK, linespacing=1.15)
    ax.set_yticks([2, 1, 0], ['Strong inhibitor,\ninterruptive (148)', 'Moderate inhibitor,\nguidance only (296)',
                              'Legacy QT alert,\ngeneric (1,020)'], fontsize=8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.45, 2.45)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.set_xlabel('Share of alert displays (number of displays in brackets)', fontsize=8)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    fig.subplots_adjust(left=0.24, right=0.87, top=0.97, bottom=0.2)
    save(fig, 'fig24_3')


def fig24_4():
    """Database B: co-dispensing by period, and dose reduction with moderate inhibitors."""
    fig, (a1, a2) = chart(2.5, ncols=2, gridspec_kw={'width_ratios': [1.45, 1], 'wspace': 0.38})
    xs = [-3.5, 3.5, 9.5]
    strong = [1.90, 0.90, 0.8]
    a1.plot(xs, strong, '-o', color=RUST, ms=4.5)
    for x, v, lab in zip(xs, strong, ['1.90%', '0.90%', '0.8%']):
        a1.text(x, v + (0.12 if x < 0 else -0.25), lab, ha='center', fontsize=7.5, color=RUST)
    flu = [(xs[0], 1.4), (xs[2], 1.5)]
    a1.plot([p[0] for p in flu], [p[1] for p in flu], 'o', color=SAND_DARK, ms=4.5)
    a1.plot([p[0] for p in flu], [p[1] for p in flu], color=SAND_DARK, lw=1.2, ls=(0, (2, 2)))
    a1.text(xs[0], 1.4 - 0.2, '1.4%', ha='center', fontsize=7.5, color=SAND_DARK)
    a1.text(xs[2], 1.5 + 0.1, '1.5%', ha='center', fontsize=7.5, color=SAND_DARK)
    a1.text(2.5, 1.62, 'Fluconazole', fontsize=7.5, color=SAND_DARK, fontweight='bold', ha='center')
    a1.text(-6.8, 2.3, 'Strong inhibitors', fontsize=7.5, color=RUST, fontweight='bold', ha='left')
    a1.axvline(0, color=GREY, lw=0.9, ls=(0, (3, 2)))
    a1.text(0.3, 0.12, 'Month 0: label\nupdate and DHPC', fontsize=6.8, color=GREY, ha='left', va='bottom')
    a1.set_xlim(-7, 13)
    a1.set_ylim(0, 2.5)
    a1.set_xticks(xs, ['−6 to −1', '1 to 6', '7 to 12'], fontsize=7.5)
    a1.set_xlabel('Months relative to the measures', fontsize=7.5)
    a1.set_ylabel('Ravolixan users with overlap', fontsize=7.5)
    a1.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.1f}%'))
    # right panel: moderate-inhibitor overlap episodes still at 40 mg
    a2.bar([0, 1], [64, 45], width=0.55, color=[TEAL_MID, TEAL])
    for x, v in zip([0, 1], [64, 45]):
        a2.text(x, v + 2, f'{v}%', ha='center', fontsize=7.5, fontweight='bold' if x else 'normal')
    a2.axhline(30, color=RUST, lw=0.9, ls=(0, (3, 2)))
    a2.text(2.25, 31.5, 'rule at\nmonth 12:\n30% or less', fontsize=6.8, color=RUST, ha='right', va='bottom')
    a2.set_xticks([0, 1], ['−6 to −1', '1 to 6'], fontsize=7.5)
    a2.set_xlim(-0.5, 2.3)
    a2.set_ylim(0, 80)
    a2.set_xlabel('Months relative to the measures', fontsize=7.5)
    a2.set_ylabel('Moderate-inhibitor episodes at 40 mg', fontsize=7.5)
    a2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    fig.subplots_adjust(left=0.1, right=0.98, top=0.96, bottom=0.2)
    save(fig, 'fig24_4')


def fig24_5():
    """Effectiveness evaluation: process -> outcome -> reassessment, with the ravolixan results."""
    fig, ax = diagram(3.75)
    cols = [(0.1, 1.6, 'Process: was it delivered?'), (1.88, 1.6, 'Outcome: did practice change?'),
            (3.66, 1.54, 'Reassessment')]
    for x, w, t in cols:
        box(ax, x, 3.3, w, 0.34, t, style='teal', size=7.8)
    def item(x, w, y, h, title, body, style='light'):
        box(ax, x, y, w, h, body, style=style, size=6.8, title=title, align='left', wrapw=33)
    x, w = cols[0][0], cols[0][1]
    item(x, w, 2.5, 0.68, 'Reach (month 4)', '61% recalled receiving the DHPC')
    item(x, w, 1.45, 0.93, 'Knowledge (month 4)',
         'Named the contraindication: dermatology 88%, primary care 54%, pharmacists 71%; '
         'reminder if below 80% in any group', style='rust')
    item(x, w, 0.55, 0.78, 'Use (months 1–6)', '148 strong-inhibitor alerts; 33 with confirmed overlap, each reviewed')
    x, w = cols[1][0], cols[1][1]
    item(x, w, 2.5, 0.68, 'Behavior: strong', 'Co-dispensing 1.90% → 0.90% → 0.8% of users')
    item(x, w, 1.8, 0.58, 'Behavior: moderate', 'At 40 mg: 64% → 45% of episodes')
    item(x, w, 1.1, 0.58, 'Behavior: fluconazole', 'Overlap 1.4% → 1.5%: unchanged', style='rust')
    item(x, w, 0.3, 0.68, 'Health', 'Not estimable; 7 new reports (4 fluconazole) read as pointers')
    x, w = cols[2][0], cols[2][1]
    outcomes = [('Working: continue', 'white'), ('Working in one pathway only: targeted addition', 'accent'),
                ('Not working: a different measure', 'white'), ('Unintended effects: adjust or withdraw', 'white')]
    yy = 2.72
    for t, st in outcomes:
        box(ax, x, yy, w, 0.4, t, style=st, size=6.8, wrapw=30, bold=False)
        yy -= 0.46
    box(ax, x, 0.3, w, 0.88, 'PBPK for single-dose fluconazole; pharmacists and gynecology; '
        'pharmacy dispensing systems; results to the RMP and PBRER',
        style='sand', size=6.8, title='Ravolixan, month 12', align='left', wrapw=31)
    # arrows between columns
    for xa, xb in [(1.71, 1.87), (3.49, 3.65)]:
        arrow(ax, (xa, 3.47), (xb, 3.47), color=TEAL)
    note(ax, 'Each indicator has a decision rule written before launch (Section 24.4).', y=0.12, size=6.8)
    save(fig, 'fig24_5')


if __name__ == '__main__':
    fig24_1(); fig24_2(); fig24_3(); fig24_4(); fig24_5()
