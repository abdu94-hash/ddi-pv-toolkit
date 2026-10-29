# Figures for Chapter 14.
from figlib import *


def fig14_1():
    """Selecting follow-up questions: three tests, then rank and check for a disconfirming question."""
    H = 3.86
    fig, ax = diagram(H)
    mx, mw, mh = 0.12, 2.75, 0.56
    nx, nw = 3.3, 1.88
    ys = [3.24, 2.5, 1.68, 0.86]
    box(ax, mx + 0.4, ys[0] + 0.08, mw - 0.8, mh - 0.16, 'Candidate question', style='teal', size=8.5)
    tests = [('Decision-critical?', 'Could a plausible answer change causality, seriousness, expectedness, or the next action?'),
             ('Discriminating?', 'Does the answer separate one hypothesis from another?'),
             ('Obtainable?', 'Can the reporter answer from records they hold?')]
    outs = [('Do not ask', 'e.g. a dose already in the report; the patient\'s occupation'),
            ('Low value', 'e.g. "Did the patient feel unwell?" separates nothing'),
            ('Rephrase', 'Ask for values and dates, not interpretations')]
    for k, ((t, s), (ot, os)) in enumerate(zip(tests, outs)):
        y = ys[k + 1]
        box(ax, mx, y, mw, mh, s, style='light', size=7.5, title=t, align='left', wrapw=52)
        arrow(ax, (mx + mw / 2, ys[k] + (0.08 if k == 0 else 0) - 0.02), (mx + mw / 2, y + mh + 0.02))
        text(ax, mx + mw / 2 + 0.08, (ys[k] + (0.08 if k == 0 else 0) + y + mh) / 2, 'yes' if k else '',
             size=7, color=TEAL, italic=True, ha='left')
        box(ax, nx, y, nw, mh, os, style='grey', size=7.3, title=ot, align='left', wrapw=36)
        arrow(ax, (mx + mw + 0.02, y + mh / 2), (nx - 0.02, y + mh / 2))
        text(ax, (mx + mw + nx) / 2, y + mh / 2 + 0.1, 'no', size=7, color=GREY, italic=True)
    # final step
    fy = 0.08
    arrow(ax, (mx + mw / 2, ys[3] - 0.02), (mx + mw / 2, fy + mh + 0.02))
    text(ax, mx + mw / 2 + 0.08, (ys[3] + fy + mh) / 2, 'yes', size=7, color=TEAL, italic=True, ha='left')
    box(ax, mx, fy, mw, mh, 'Send the top five to seven, most important first, each with its purpose',
        style='teal', size=7.5, title='Rank', align='left', wrapw=52)
    box(ax, nx, fy, nw, mh, 'Is one question able to prove the first explanation wrong?',
        style='rust', size=7.3, title='Before sending', align='left', wrapw=36)
    arrow(ax, (nx - 0.02, fy + mh / 2), (mx + mw + 0.02, fy + mh / 2), color=RUST)
    save(fig, 'fig14_1')


def fig14_5():
    """Worked Case 14.1 (fictional): each hypothesis on day 1 and at month 3, and what moved it."""
    H = 3.6
    fig, ax = diagram(H)
    lx, lw = 0.1, 1.3
    c1x, cw = 1.5, 0.92
    ex, ew = 2.52, 1.75
    c2x = 4.32
    rh, gap = 0.48, 0.09
    top = 3.22
    hy = top + 0.2
    text(ax, c1x + cw / 2, hy, 'Day 1', size=8, bold=True, color=TEAL)
    text(ax, ex + ew / 2, hy, 'What follow-up showed', size=8, bold=True, color=TEAL)
    text(ax, c2x + cw / 2, hy, 'Month 3', size=8, bold=True, color=TEAL)
    rows = [
        ('Atorvastatin–\nitraconazole interaction','Possible; not leading', 'sand',
         'CK 85 U/L: no sign of the expected exposure effect', 'Not supported', 'grey'),
        ('Atorvastatin alone', 'Open', 'white',
         'Tolerated for 2 years; restarted at the same dose without recurrence', 'Unlikely', 'grey'),
        ('Itraconazole alone', 'Open; could explain alone', 'white',
         'Timing compatible, but an alternative is confirmed; never re-exposed', 'Unlikely; not excluded', 'grey'),
        ('Hepatitis E', 'Open; serology pending', 'white',
         'IgM positive and HEV RNA detected; undercooked pork; improving', 'Best supported', 'teal'),
        ('Alcohol, acetaminophen, biliary', 'Open; unknown', 'white',
         'About 8 units a week; 2 g/day for 3 days; ultrasound normal', 'Unlikely', 'grey'),
    ]
    for k, (lab, s1, st1, ev, s2, st2) in enumerate(rows):
        y = top - (k + 1) * rh - k * gap
        text(ax, lx, y + rh / 2, lab, size=7.8, ha='left', wrapw=24, bold=k == 0, color=RUST if k == 0 else INK)
        box(ax, c1x, y, cw, rh, s1, style=st1, size=7.2, wrapw=16)
        text(ax, ex + ew / 2, y + rh / 2, ev, size=7, color=INK, wrapw=38)
        arrow(ax, (c1x + cw + 0.03, y + 0.07), (c2x - 0.03, y + 0.07), color=RULE, lw=0.9)
        box(ax, c2x, y, cw, rh, s2, style=st2, size=7.2, wrapw=16, bold=st2 == 'teal')
    text(ax, lx, 0.2, 'The interaction was the first explanation offered: the reporter, the system flag, and a familiar mechanism all pointed to it.',
         size=6.8, color=RUST, italic=True, ha='left')
    save(fig, 'fig14_5')


def fig14_2():
    """Two routes to a liver signal: the interaction raises statin exposure (ref [5]); itraconazole alone injures the liver (ref [7])."""
    fig, (a, b) = chart(2.45, ncols=2, gridspec_kw={'width_ratios': [1.25, 1]})
    labs = ['Atorvastatin acid', 'Atorvastatin lactone', 'Active HMG-CoA\nreductase inhibitors']
    vals = [3, 4, 1.6]
    txt = ['about 3-fold', 'about 4-fold', '1.6-fold']
    y = [2, 1, 0]
    a.barh(y, vals, 0.55, color=[TEAL, TEAL, TEAL_MID])
    for yi, v, t in zip(y, vals, txt):
        a.text(v + 0.08, yi, t, va='center', fontsize=7.5, color=INK)
    a.axvline(1, color=GREY, lw=0.8, ls=(0, (2, 2)), zorder=0)
    a.set_yticks(y, labs, fontsize=7.5)
    a.tick_params(axis='y', length=0); a.spines['left'].set_visible(False)
    a.set_xlim(0, 5.6); a.set_xticks([0, 1, 2, 3, 4, 5])
    a.set_xlabel('AUC ratio with itraconazole', fontsize=7.5)
    a.set_title('Interaction: statin exposure rises', fontsize=8, color=TEAL, loc='left', pad=6)
    # itraconazole DILI incidence
    bv = [3.6, 62.5]
    b.bar([0, 1], bv, 0.55, color=[RUST_LIGHT, RUST], ec=RUST, lw=0.8)
    for xi, v in zip([0, 1], bv):
        b.text(xi, v + 2, f'{v}', ha='center', fontsize=7.5, color=RUST, fontweight='bold')
    b.set_xticks([0, 1], ['All users', '60 or more\nDDDs'], fontsize=7.5)
    b.set_ylim(0, 75); b.set_yticks([0, 25, 50, 75])
    b.set_ylabel('DILI per 10,000 persons', fontsize=7.5)
    b.set_title('Itraconazole alone: liver injury', fontsize=8, color=RUST, loc='left', pad=6)
    fig.tight_layout(w_pad=2.0)
    save(fig, 'fig14_2')


def fig14_3():
    """Worked Case 14.1: the R ratio calculation and where the result falls (ref [2])."""
    H = 2.0
    fig, ax = diagram(H)
    steps = [('ALT ÷ ULN', '1,240 ÷ 40 = 31'), ('ALP ÷ ULN', '180 ÷ 130 = 1.38'), ('R', '31 ÷ 1.38 ≈ 22')]
    bw, g = 1.5, 0.22
    x0 = (TEXT_W - (3 * bw + 2 * g)) / 2
    for k, (t, s) in enumerate(steps):
        x = x0 + k * (bw + g)
        box(ax, x, 1.2, bw, 0.6, s, style='teal' if k == 2 else 'light', size=8, title=t)
        if k:
            arrow(ax, (x - g + 0.02, 1.5), (x - 0.02, 1.5))
    # scale: log R from 0.5 to 40
    import math
    sx0, sx1 = 0.35, 4.95
    def X(r):
        return sx0 + (math.log10(r) - math.log10(0.5)) / (math.log10(40) - math.log10(0.5)) * (sx1 - sx0)
    sy, sh = 0.62, 0.3
    zones = [(0.5, 2, 'Cholestatic (R ≤ 2)', SAND, SAND_DARK), (2, 5, 'Mixed', '#EEF1F2', GREY),
             (5, 40, 'Hepatocellular (R ≥ 5)', TEAL_LIGHT, TEAL)]
    for lo, hi, lab, fc, tc in zones:
        ax.add_patch(matplotlib.patches.Rectangle((X(lo), sy), X(hi) - X(lo), sh, fc=fc, ec='white', lw=1.5, zorder=1))
        text(ax, (X(lo) + X(min(hi, 15))) / 2, sy + sh / 2, lab, size=7.2, color=tc, bold=True)
    for r in (2, 5):
        text(ax, X(r), sy - 0.12, str(r), size=7, color=GREY)
    xr = X(22)
    ax.plot([xr, xr], [sy - 0.04, sy + sh + 0.04], color=RUST, lw=1.8, zorder=3)
    arrow(ax, (x0 + 2 * (bw + g) + bw / 2, 1.18), (xr, sy + sh + 0.06), color=RUST, lw=1.0)
    text(ax, xr, sy - 0.14, 'this case: 22', size=7.2, color=RUST, bold=True)
    text(ax, sx0, 0.14, 'R on a log scale. Bilirubin 92 µmol/L, about 4.4 times ULN: hepatocellular injury with jaundice.',
         size=6.8, color=GREY, italic=True, ha='left')
    save(fig, 'fig14_3')


def fig14_4():
    """Chronology of Worked Case 14.1 (fictional), stages 1 to 3."""
    H = 3.05
    fig, ax = diagram(H)
    cols = ['2 years\nbefore', '6 months\nbefore', '5 weeks\nbefore', '3 weeks\nbefore', 'Admission', 'Day 12',
            'Day 14', 'Week 8', 'Week 10', 'Week 14']
    x0, dx = 1.25, 0.41
    def X(k):
        return x0 + k * dx
    ytop, ybot = 2.62, 0.62
    for k, c in enumerate(cols):
        text(ax, X(k), ybot - 0.2, c, size=6.8, color=GREY, va='top')
        ax.plot([X(k), X(k)], [ybot - 0.05, ybot], color=GREY, lw=0.6)
    ax.plot([X(-0.3), X(9.25)], [ybot, ybot], color=GREY, lw=0.6)
    for k in (0.5, 1.5, 2.5, 3.5, 4.5, 6.5, 7.5, 8.5):
        xk = X(k)
        ax.plot([xk - 0.04, xk - 0.01], [ybot - 0.045, ybot + 0.045], color=GREY, lw=0.6)
        ax.plot([xk + 0.01, xk + 0.04], [ybot - 0.045, ybot + 0.045], color=GREY, lw=0.6)
    adm = X(4)
    ax.plot([adm, adm], [1.42, ytop], color=RUST, lw=0.8, ls=(0, (2, 2)), zorder=1)
    text(ax, adm, ytop + 0.13, 'jaundice: both drugs stopped', size=7, color=RUST, bold=True)
    rows = {'Atorvastatin': 2.38, 'Itraconazole': 2.02, 'Findings': 1.62, 'ALT (U/L)': 1.22, 'Bilirubin\n(µmol/L)': 0.88}
    for lab, y in rows.items():
        text(ax, 0.08, y, lab, size=7.8, ha='left')
    bar = 0.16
    def seg(a, b, y, color, label='', tc='white'):
        ax.add_patch(matplotlib.patches.Rectangle((a, y - bar / 2), b - a, bar, fc=color, ec='none', zorder=2))
        if label:
            text(ax, (a + b) / 2, y, label, size=6.8, color=tc, bold=True)
    y = rows['Atorvastatin']
    seg(X(-0.2), adm, y, TEAL, '40 mg daily for two years')
    seg(X(8), X(9.25), y, TEAL, 'restarted')
    y = rows['Itraconazole']
    seg(X(2), adm, y, TEAL_MID, '200 mg', tc=INK)
    text(ax, X(5.2), y, 'not restarted', size=6.8, color=GREY, italic=True, ha='left')
    y = rows['Findings']
    text(ax, X(3), y, 'undercooked\npork', size=6.8, color=RUST)
    text(ax, X(5.35), y, 'HEV IgM+, RNA\ndetected; CK normal', size=6.8, color=RUST)
    y = rows['ALT (U/L)']
    for k, v, c in [(1, 'normal', GREY), (4, '1,240', RUST), (6, '310', INK), (7, 'normal', GREY), (9, 'normal', GREY)]:
        text(ax, X(k), y, v, size=7, color=c, bold=c == RUST, italic=c == GREY)
    y = rows['Bilirubin\n(µmol/L)']
    for k, v, c in [(4, '92', RUST), (6, '38', INK)]:
        text(ax, X(k), y, v, size=7, color=c, bold=c == RUST)
    text(ax, X(4.5), 0.08, 'Time axis not to scale.', size=6.8, color=GREY, italic=True)
    save(fig, 'fig14_4')


if __name__ == '__main__':
    fig14_1(); fig14_2(); fig14_3(); fig14_4(); fig14_5()
