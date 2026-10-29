# Figures for Chapter 13.
from figlib import *
from matplotlib.patches import Rectangle


def fig13_3():
    """Chronology of Worked Case 13.1 (fictional): why now, and what changed at dechallenge and restart."""
    H = 3.32
    fig, ax = diagram(H)
    cols = ['3 years\nbefore', '14 months', '4 months', '3 months', '16 days', 'Admission', '+4 days', '6 weeks\nafter']
    x0, dx = 1.38, 0.53
    def X(k):
        return x0 + k * dx
    ytop, ybot = 3.0, 0.98
    adm = X(5)
    # light band marking the recent changes
    ax.add_patch(Rectangle((X(2.55), ybot), adm - X(2.55), ytop - ybot, fc=TEAL_LIGHT, ec='none', zorder=0))
    text(ax, adm - 0.1, ytop + 0.12, 'recent changes: why now?', size=7, color=TEAL, italic=True, ha='right')
    for k, c in enumerate(cols):
        text(ax, X(k), ybot - 0.2, c, size=7, color=GREY, va='top')
        ax.plot([X(k), X(k)], [ybot - 0.06, ybot], color=GREY, lw=0.6)
    ax.plot([X(-0.3), X(7.3)], [ybot, ybot], color=GREY, lw=0.6)
    for k in (0.5, 1.5, 2.5, 3.5, 4.5, 6.5):  # axis breaks: time not to scale
        xk = X(k)
        ax.plot([xk - 0.05, xk - 0.01], [ybot - 0.05, ybot + 0.05], color=GREY, lw=0.6)
        ax.plot([xk + 0.01, xk + 0.05], [ybot - 0.05, ybot + 0.05], color=GREY, lw=0.6)
    ax.plot([adm, adm], [ybot, ytop], color=RUST, lw=0.9, ls=(0, (2, 2)), zorder=1)
    text(ax, adm + 0.06, ytop + 0.12, 'bleed', size=7.5, color=RUST, bold=True, ha='left')
    rows = {'Apixaban': 2.7, 'Sertraline': 2.3, 'Naproxen': 1.9, 'Creatinine\n(µmol/L)': 1.5, 'Weight (kg)': 1.15}
    for lab, y in rows.items():
        text(ax, 0.1, y, lab, size=8, ha='left')
    bar = 0.17
    def seg(a, b, y, color, label='', tc='white'):
        ax.add_patch(Rectangle((a, y - bar / 2), b - a, bar, fc=color, ec='none', zorder=2))
        if label:
            text(ax, (a + b) / 2, y, label, size=6.8, color=tc, bold=True)
    y = rows['Apixaban']
    seg(X(0), adm, y, TEAL, '5 mg twice daily, never adjusted')
    ax.plot([adm, X(6)], [y, y], color=GREY, lw=1, ls=(0, (2, 2)), zorder=1)
    text(ax, (adm + X(6)) / 2, y + 0.16, 'held', size=6.8, color=GREY, italic=True)
    seg(X(6), X(7.25), y, TEAL_MID, '2.5 mg + PPI', tc=INK)
    y = rows['Sertraline']
    seg(X(2), X(7.25), y, TEAL, '50 mg daily, continued')
    y = rows['Naproxen']
    seg(X(4), adm, y, RUST)
    text(ax, X(4) - 0.06, y, '500 mg twice daily', size=6.8, color=RUST, ha='right')
    text(ax, adm + 0.08, y, 'stopped', size=6.8, color=GREY, italic=True, ha='left')
    y = rows['Creatinine\n(µmol/L)']
    pts = [(X(1), 92), (X(3), 121), (adm, 158)]
    ax.plot([p[0] for p in pts], [y - 0.06, y, y + 0.06], color=RULE, lw=0.8, zorder=1)
    for (xx, v), dy in zip(pts, (-0.06, 0, 0.06)):
        ax.plot([xx], [y + dy], 'o', ms=3.5, color=TEAL if v < 150 else RUST, zorder=3)
        text(ax, xx + (0.07 if v > 150 else 0), y + dy + (0.0 if v > 150 else 0.13), str(v), size=7, bold=v > 150, color=RUST if v > 150 else INK, ha='left' if v > 150 else 'center')
    text(ax, (X(6) + X(7)) / 2, y, '129 at discharge', size=6.8, color=GREY, italic=True)
    y = rows['Weight (kg)']
    text(ax, X(0), y, '63', size=7, bold=True)
    text(ax, adm + 0.06, y, '56', size=7, bold=True, color=RUST, ha='left')
    text(ax, (X(0) + adm) / 2, y, 'when weight fell to 60 kg or less: unknown', size=6.8, color=GREY, italic=True)
    # notes on what dechallenge and restart can show
    nw, nh, ny = 2.45, 0.42, 0.06
    box(ax, 0.1, ny, nw, nh, 'At admission: naproxen stopped, apixaban held, ulcer treated. All at once: '
        'uninformative between drugs.', style='sand', size=6.8, align='left', wrapw=60)
    box(ax, 0.1 + nw + 0.2, ny, nw, nh, 'Restart without rebleeding: lower apixaban dose, PPI added, no '
        'naproxen. Changed conditions, not exoneration.', style='sand', size=6.8, align='left', wrapw=60)
    save(fig, 'fig13_3')


def fig13_4():
    """Converging contributions to the bleed in Worked Case 13.1: PD routes and PK routes (refs [6], [8], [9])."""
    H = 3.55
    fig, ax = diagram(H)
    bw, gap = 0.98, 0.39
    xs = [0.12 + k * (bw + gap) for k in range(4)]
    dy, dh = 2.5, 0.5
    for x, t, st in zip(xs, ['Sertraline', 'Naproxen', 'Apixaban', 'Age 82, 56 kg;\nrenal function falling'],
                        ['teal', 'teal', 'teal', 'grey']):
        box(ax, x, dy, bw, dh, t, style=st, size=8.5 if st == 'teal' else 7, wrapw=30)
    # PK routes into apixaban exposure: arcs over the top
    top = dy + dh + 0.02
    arrow(ax, (xs[1] + bw * 0.7, top), (xs[2] + bw * 0.3, top), color=RUST, lw=1.0, ls=(0, (3, 2)), rad=-0.45)
    text(ax, (xs[1] + xs[2] + bw) / 2, 3.38, 'PK: apixaban AUC up 54%', size=6.8, color=RUST, italic=True)
    arrow(ax, (xs[3] + bw * 0.3, top), (xs[2] + bw * 0.7, top), color=RUST, lw=1.0, ls=(0, (3, 2)), rad=0.45)
    text(ax, xs[3] + 0.2, 3.38, 'PK: lower clearance;\ndose not reduced', size=6.8, color=RUST, italic=True)
    # mechanism row
    my, mh = 1.35, 0.62
    mech = [(xs[0], 'Platelet function impaired', 'white'), (xs[1], 'Mucosal injury: gastric ulcer', 'rust'),
            (xs[2], 'Coagulation impaired, exposure higher than intended', 'white')]
    for x, t, st in mech:
        box(ax, x, my, bw, mh, t, style=st, size=7.3, wrapw=20)
    for k in range(3):
        arrow(ax, (xs[k] + bw / 2, dy - 0.02), (xs[k] + bw / 2, my + mh + 0.02), color=TEAL, lw=1.0)
    arrow(ax, (xs[1] + 0.12, dy - 0.02), (xs[0] + bw - 0.12, my + mh + 0.02), color=TEAL, lw=1.0)
    text(ax, (xs[0] + xs[1] + bw) / 2 + 0.02, 2.13, 'PD', size=6.8, color=TEAL, italic=True)
    # outcome
    oy, oh = 0.25, 0.52
    ow = xs[2] + bw - xs[0]
    box(ax, xs[0], oy, ow, oh, 'Upper GI hemorrhage from the ulcer', style='accent', size=8.5)
    labels = ['bleeding risk', 'the lesion', 'bleeding risk']
    for k in range(3):
        xa = xs[k] + bw / 2
        arrow(ax, (xa, my - 0.02), (xa, oy + oh + 0.02), color=RUST, lw=1.0)
        text(ax, xa + 0.06, (my + oy + oh) / 2, labels[k], size=6.8, color=GREY, italic=True, ha='left')
    # notes on the right
    box(ax, xs[3], my, bw, mh, 'H. pylori: competing cause of the ulcer, not yet excluded',
        style='grey', size=6.8, wrapw=22)
    box(ax, xs[3], oy, bw, oh, 'Ranked in words, not split into percentages',
        style='sand', size=6.8, wrapw=22)
    save(fig, 'fig13_4')


def fig13_1():
    """What each instrument assesses in a three-drug case, and inter-rater agreement (refs [4], [5])."""
    H = 3.0
    fig, ax = diagram(H)
    pw = 1.62
    names = ['Apixaban', 'Naproxen', 'Sertraline']
    titles = [('WHO-UMC, Naranjo', 'one drug at a time'), ('DIPS', 'one object–precipitant pair'),
              ('The combination', 'no instrument assesses it')]
    for p in range(3):
        x0 = 0.12 + p * (pw + 0.17)
        cx = x0 + pw / 2
        pts = [(cx, 2.22), (cx - 0.5, 1.5), (cx + 0.5, 1.5)]
        if p == 2:
            ax.add_patch(matplotlib.patches.Polygon(pts, closed=True, fc=RUST_LIGHT, ec=RUST, lw=0.9, ls=(0, (3, 2)), zorder=1))
            text(ax, cx, 1.76, '?', size=13, color=RUST, bold=True)
        else:
            for i, j in [(0, 1), (0, 2), (1, 2)]:
                ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=RULE, lw=0.8, zorder=1)
        if p == 1:
            for j in (1, 2):
                ax.plot([pts[0][0], pts[j][0]], [pts[0][1], pts[j][1]], color=TEAL, lw=2.2, zorder=1)
            text(ax, cx, 1.84, 'one pair\nper scale', size=6.8, color=TEAL, italic=True)
        for k, ((px, py), nm) in enumerate(zip(pts, names)):
            hl = p == 0
            ax.add_patch(matplotlib.patches.Circle((px, py), 0.1, fc=TEAL if hl else 'white', ec=TEAL, lw=1.0, zorder=3))
            dy = 0.2 if k == 0 else -0.2
            text(ax, px, py + dy, nm, size=7, color=INK)
        text(ax, cx, 2.84, titles[p][0], size=8, bold=True, color=RUST if p == 2 else TEAL)
        text(ax, cx, 2.66, titles[p][1], size=7, color=GREY, italic=True)
    # agreement bars
    b = fig.add_axes([1.45 / TEXT_W, 0.32 / H, 3.6 / TEXT_W, 0.68 / H])
    b.spines[['top', 'right']].set_visible(False); b.tick_params(length=3, width=0.6)
    vals = [('Naranjo', 0.297, '0.297'), ('WHO-UMC', 0.20, '0.20')]
    for i, (n, v, vs) in enumerate(vals):
        b.barh(i, v, 0.55, color=TEAL)
        b.text(v + 0.015, i, 'κ ' + vs, va='center', fontsize=7.5, color=TEAL, fontweight='bold')
    b.set_yticks([0, 1], [v[0] for v in vals], fontsize=7.5)
    b.set_xlim(0, 1); b.set_xticks([0, 0.5, 1]); b.tick_params(axis='x', labelsize=7)
    b.text(1.0, 1.45, '1 = perfect agreement', fontsize=6.8, color=GREY, ha='right', style='italic')
    text(ax, 0.12, 0.83, 'Agreement among\nfive raters on\n100 reports', size=7, color=INK, ha='left', va='top')
    save(fig, 'fig13_1')


def fig13_2():
    """Forest-style plot of the outcome evidence in Section 13.5 (refs [9]-[12], [14])."""
    rows = [
        ('SSRI with an anticoagulant', None),
        ('SSRI + oral anticoagulant, major bleeding (IRR) [10]', (1.33, 1.24, 1.42)),
        ('SSRI + oral anticoagulant, first 30 days (IRR) [10]', (1.74, 1.37, 2.22)),
        ('SSRI + DOAC, major bleeding (IRR) [10]', (1.25, 1.12, 1.40)),
        ('SSRI or SNRI + NOAC, major or CRNM bleeding (aHR) [11]', (1.26, 1.17, 1.35)),
        ('SSRI + rivaroxaban, ROCKET AF (aHR) [12]', (1.11, 0.82, 1.51)),
        ('NSAID with an anticoagulant', None),
        ('NSAID + NOAC, major or CRNM bleeding (aHR) [11]', (1.10, 1.01, 1.21)),
        ('Incident NSAID use, ARISTOTLE, major bleeding (HR) [14]', (1.61, 1.11, 2.33)),
        ('Without an anticoagulant: upper GI bleeding', None),
        ('SSRI (OR) [9]', (1.66, 1.44, 1.92)),
        ('SSRI + NSAID (OR) [9]', (4.25, 2.82, 6.42)),
    ]
    fig, a = chart(3.5)
    fig.subplots_adjust(left=0.5, right=0.97, top=0.98, bottom=0.13)
    n = len(rows)
    for i, (lab, v) in enumerate(rows):
        y = n - 1 - i
        if v is None:
            hc = SAND_DARK if lab.startswith('NSAID') else (INK if lab.startswith('Without') else TEAL)
            a.text(-0.02, y, lab, transform=a.get_yaxis_transform(), ha='right', va='center', fontsize=7.5,
                   fontweight='bold', color=hc)
            continue
        est, lo, hi = v
        col = RUST if 'SSRI + NSAID' in lab else (SAND_DARK if 'NSAID' in lab else TEAL)
        a.plot([lo, hi], [y, y], color=col, lw=1.3)
        a.plot([est], [y], 's', color=col, ms=4.5)
        a.text(-0.02, y, lab, transform=a.get_yaxis_transform(), ha='right', va='center', fontsize=7)
        a.text(hi * 1.06, y, f'{est:.2f}', va='center', fontsize=6.8, color=col)
    a.axvline(1, color=GREY, lw=0.8)
    a.set_xscale('log')
    a.set_xlim(0.7, 9)
    a.set_xticks([0.75, 1, 1.5, 2, 3, 5], ['0.75', '1', '1.5', '2', '3', '5'])
    a.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    a.set_yticks([]); a.spines['left'].set_visible(False)
    a.set_ylim(-0.6, n - 0.4)
    a.set_xlabel('Ratio with 95% CI (log scale; 1 = no difference)', fontsize=7.5)
    save(fig, 'fig13_2')


def fig13_5():
    """Calculation 13.1 drawn: Naranjo item scores per drug (ref [3])."""
    drugs = [('Naproxen', [('Previous reports', 1), ('Timing', 2), ('Withdrawal', 1), ('Objective', 1)],
              [('Alternative causes', -1)], 4),
             ('Apixaban', [('Previous reports', 1), ('Timing', 2), ('Withdrawal', 1), ('Objective', 1)],
              [('Alternative causes', -1), ('Restart, no recurrence', -1)], 3),
             ('Sertraline', [('Previous reports', 1), ('Timing', 2), ('Objective', 1)],
              [('Alternative causes', -1)], 3)]
    shade = {'Previous reports': TEAL_MID, 'Timing': TEAL, 'Withdrawal': TEAL_MID, 'Objective': TEAL}
    short = {'Previous reports': 'reports', 'Timing': 'timing', 'Withdrawal': 'withdr.', 'Objective': 'endosc.'}
    fig, a = chart(2.35)
    fig.subplots_adjust(left=0.16, right=0.76, top=0.89, bottom=0.3)
    for i, (d, pos, neg, tot) in enumerate(drugs):
        y = len(drugs) - 1 - i
        x = 0
        for lab, v in pos:
            a.barh(y, v, 0.56, left=x, color=shade[lab], ec='white', lw=1.2)
            a.text(x + v / 2, y, f'+{v}', ha='center', va='center', fontsize=7, color='white', fontweight='bold')
            x += v
        x = 0
        for lab, v in neg:
            a.barh(y, v, 0.56, left=x, color=RUST, ec='white', lw=1.2)
            a.text(x + v / 2, y, f'{v}', ha='center', va='center', fontsize=7, color='white', fontweight='bold')
            x += v
        a.text(5.25, y, f'total {tot}: possible', va='center', fontsize=7.5, color=INK, fontweight='bold')
    a.axvline(0, color=GREY, lw=0.8)
    a.set_yticks(range(3), [d[0] for d in drugs][::-1], fontsize=8)
    a.tick_params(axis='y', length=0); a.spines['left'].set_visible(False)
    a.set_xlim(-2.4, 5.2); a.set_xticks(range(-2, 6))
    a.set_xlabel('Naranjo item scores (other items 0)', fontsize=7.5)
    a.text(-2.35, 2.55, 'subtracting', fontsize=6.8, color=RUST, style='italic')
    a.text(0.1, 2.55, 'adding: reports, timing, withdrawal, endoscopy', fontsize=6.8, color=TEAL, style='italic')
    fig.text(0.5, 0.03, 'Same category for all three: the scores cannot show which drug caused the ulcer, '
             'and the combination has no item.', fontsize=7, color=SAND_DARK, ha='center', va='bottom', style='italic')
    save(fig, 'fig13_5')


if __name__ == '__main__':
    fig13_1(); fig13_2(); fig13_3(); fig13_4(); fig13_5()
