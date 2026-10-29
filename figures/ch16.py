# Figures for Chapter 16.
from figlib import *


def fig16_1():
    """Seriousness versus severity: two separate axes, with examples from the chapter."""
    H = 2.55
    fig, ax = diagram(H)
    x0, y0 = 0.72, 0.42
    cw, ch, g = 2.2, 0.86, 0.1
    cells = {  # (col, row): (title, text, style)
        (0, 1): ('Serious, not severe', 'Acute kidney injury in Worked Case 16.1: led to admission; creatinine about '
                 '1.8 times baseline (KDIGO stage 1)', 'rust'),
        (1, 1): ('Serious and severe', 'Torsade de pointes in Worked Case 16.2: life-threatening, admitted; '
                 'graded severe by the investigator', 'light'),
        (0, 0): ('Neither', 'A mild event with no seriousness criterion', 'white'),
        (1, 0): ('Severe, not serious', 'Severe headache for two days in Exercise 16.1: stayed at home and '
                 'recovered', 'rust'),
    }
    for (c, r), (t, s, st) in cells.items():
        box(ax, x0 + c * (cw + g), y0 + r * (ch + g), cw, ch, s, style=st, size=7.5, title=t, align='left', wrapw=44)
    # axes
    xa0, xa1 = x0, x0 + 2 * cw + g
    ya = y0 - 0.12
    arrow(ax, (xa0, ya), (xa1, ya), color=GREY)
    text(ax, (xa0 + xa1) / 2, ya - 0.14, 'Severity: intensity of the event (mild, moderate, severe; or a grade)',
         size=7.5, color=GREY, italic=True)
    xb = x0 - 0.12
    arrow(ax, (xb, y0), (xb, y0 + 2 * ch + g), color=GREY)
    text(ax, xb - 0.15, y0 + ch + g / 2, 'Seriousness: outcome (ICH E2A)', size=7.5, color=GREY,
         italic=True, rotation=90)
    for r, lab in [(0, 'Non-serious'), (1, 'Serious')]:
        text(ax, xb - 0.38, y0 + r * (ch + g) + ch / 2, lab, size=7, color=INK, rotation=90, bold=True)
    text(ax, x0, y0 + 2 * ch + g + 0.12, 'Rust cells: where the two are most often confused', size=7,
         color=RUST, italic=True, ha='left')
    save(fig, 'fig16_1')


def fig16_3():
    """Reporting logic when an interaction is involved: common steps, then the three settings."""
    H = 4.38
    fig, ax = diagram(H)
    mx, mw, mh, gy = 0.1, 3.1, 0.5, 0.15
    steps = [
        ('Valid case, Day 0', 'Identifiable patient, reporter, suspected product, and event.\nDay 0 is first '
         'receipt anywhere in the organization.', 'teal', 0.62),
        ('Our product suspect or interacting?', 'Interacting drugs are treated as suspected for reporting.', 'light', mh),
        ('Seriousness, per event', 'ICH E2A criteria; taken from the reporter or investigator.', 'light', mh),
        ('Expectedness, per event', 'Against our own document and its version (RSI, USPI, SmPC).', 'light', mh),
    ]
    ys = []
    y = H - 0.08
    for k, (t, s, st, h) in enumerate(steps):
        y -= h
        box(ax, mx, y, mw, h, s, style=st, size=7.2, title=t, align='left', wrapw=66)
        if k:
            arrow(ax, (mx + mw / 2, ys[k - 1] - 0.02), (mx + mw / 2, y + h + 0.02))
        ys.append(y)
        y -= gy
    # notes beside the steps
    nx, nw = 3.4, 1.78
    box(ax, nx, ys[1], nw, mh, 'Each company assesses against its own product\'s document.',
        style='sand', size=7, wrapw=34)
    box(ax, nx, ys[3], nw, mh, 'A described interaction does not make an unlisted event expected.',
        style='rust', size=7, wrapw=34)
    arrow(ax, (nx - 0.02, ys[3] + mh / 2), (mx + mw + 0.02, ys[3] + mh / 2), color=RUST)
    # branches
    bh, bw, bg = 0.8, 1.62, 0.12
    by = 0.62
    bx = [0.1 + k * (bw + bg) for k in range(3)]
    branches = [('EU postmarketing', 'Serious: 15 days, whether expected or not. Non-serious EU cases: 90 days.'),
                ('US postmarketing', 'Serious and unexpected: 15-day alert report. Otherwise: periodic report.'),
                ('Clinical trial (SUSAR)', 'Serious, unexpected per the RSI, suspected, on active drug after '
                 'unblinding: 7 days if fatal or life-threatening, otherwise 15.')]
    yb = ys[3] - 0.13
    ax.plot([mx + mw / 2, mx + mw / 2], [ys[3] - 0.02, yb], color=GREY, lw=1.1, zorder=1)
    ax.plot([bx[0] + bw / 2, bx[2] + bw / 2], [yb, yb], color=GREY, lw=1.1, zorder=1)
    for x, (t, s) in zip(bx, branches):
        arrow(ax, (x + bw / 2, yb), (x + bw / 2, by + bh + 0.02))
        box(ax, x, by, bw, bh, s, style='white', size=7, title=t, align='left', wrapw=33)
    box(ax, 0.1, 0.08, bx[2] + bw - 0.1, 0.42, 'In every setting: an expected event with an undescribed interaction '
        'still goes to signal management and aggregate review, and significant follow-up starts a new clock.',
        style='sand', size=7, wrapw=110)
    save(fig, 'fig16_3')


def fig16_2():
    """Expectedness: within the listed term versus more specific or more severe (ref [1])."""
    H = 2.6
    fig, ax = diagram(H)
    cols = [('More specific', 'Acute renal failure', ('Acute renal failure', 'expected'), ('Interstitial nephritis', 'unexpected')),
            ('More specific and more severe', 'Electrocardiogram QT prolonged',
             ('QTcF 541 ms', 'expected'), ('Torsade de pointes', 'unexpected')),
            ('More severe', 'Reversible forms only', ('A reversible case', 'expected'), ('A fatal outcome', 'unexpected'))]
    cw, cg = 1.6, 0.12
    for i, (head, listed, inn, out) in enumerate(cols):
        x = 0.1 + i * (cw + cg)
        text(ax, x + cw / 2, 2.42, head, size=8, bold=True, color=TEAL)
        box(ax, x, 1.68, cw, 0.5, listed, style='light', size=7.3, title='Listed in the reference', wrapw=30)
        hw = (cw - 0.1) / 2
        for j, ((lab, verdict), st) in enumerate([(inn, 'white'), (out, 'rust')]):
            bx = x + j * (hw + 0.1)
            box(ax, bx, 0.62, hw, 0.62, lab, style=st, size=7.2, wrapw=14)
            text(ax, bx + hw / 2, 0.47, verdict, size=7, bold=True, color=TEAL if j == 0 else RUST)
            arrow(ax, (x + cw / 2, 1.66), (bx + hw / 2, 1.26), color=GREY, lw=0.9)
    text(ax, TEXT_W / 2, 0.14, 'A reaction described only as a class ADR should not automatically be considered expected for the product.',
         size=6.8, color=GREY, italic=True)
    save(fig, 'fig16_2')


def fig16_4():
    """Ravolixan (fictional): exposure with diltiazem against the thorough QT study (BRIEF Section 7)."""
    fig, a = chart(2.75)
    fig.subplots_adjust(left=0.1, right=0.97, top=0.96, bottom=0.3)
    pts = [(1, 6, 9, 'therapeutic dose: 6 ms (upper 90% CI 9)', 'left'),
           (4, 18, 22, 'supratherapeutic dose: 18 ms (upper 90% CI 22)', 'right')]
    for x, m, u, lab, side in pts:
        a.plot([x, x], [m, u], color=TEAL, lw=1.2)
        a.plot([x - 0.06, x + 0.06], [u, u], color=TEAL, lw=1.2)
        a.plot([x], [m], 'o', color=TEAL, ms=6, zorder=3)
        dx = 0.12 if side == 'left' else -0.12
        a.text(x + dx, m, lab, fontsize=7, va='center', ha=side, color=TEAL)
    a.plot([1.5], [0.9], '^', color=RUST, ms=8, zorder=3, clip_on=False)
    a.text(1.62, 1.6, 'with diltiazem: Cmax ratio 1.5 (AUC ratio 2.0)', fontsize=7, color=RUST, va='center')
    a.set_xlim(0, 5.2); a.set_ylim(0, 25)
    a.set_xticks([0, 1, 2, 3, 4, 5])
    a.set_xlabel('Ravolixan Cmax relative to 40 mg', fontsize=7.5)
    a.set_ylabel('Placebo-corrected ΔQTcF (ms)', fontsize=7.5)
    fig.text(0.1, 0.03, 'Thorough QT study: mean with upper 90% CI. Not on this axis: potassium 3.1 mmol/L and magnesium 0.68 mmol/L\nin Worked Case 16.2, strong independent risk factors.',
             fontsize=7, color=SAND_DARK, va='bottom', style='italic', linespacing=1.3)
    save(fig, 'fig16_4')


def fig16_5():
    """Worked Case 16.2 (fictional): trial course and the reporting clock."""
    H = 2.62
    fig, ax = diagram(H)
    ax.set_ylim(0.3, 0.3 + H)
    # top: trial course, not to scale
    ev = [('2 June', 'randomized;\nQTcF 438 at screening'), ('14 August', 'diltiazem started by\nprimary-care physician;\nsite not told'),
          ('3 September', 'syncope; torsade de\npointes; QTcF 541'), ('5 September', 'QTcF 462'),
          ('7 September', 'discharged')]
    x0, x1 = 0.55, 4.85
    yt = 2.25
    text(ax, 0.1, 2.72, 'Trial course (not to scale)', size=8, bold=True, color=TEAL, ha='left')
    ax.plot([x0 - 0.2, x1 + 0.2], [yt, yt], color=GREY, lw=0.8)
    xs = [x0 + k * (x1 - x0) / 4 for k in range(5)]
    for k, ((d, s), x) in enumerate(zip(ev, xs)):
        col = RUST if k == 2 else (SAND_DARK if k == 1 else TEAL)
        ax.plot([x], [yt], 'o', color=col, ms=6, zorder=3)
        text(ax, x, yt + 0.17, d, size=7.3, bold=True, color=col)
        text(ax, x, yt - 0.14, s, size=6.8, color=INK, va='top')
    # bottom: reporting clock by day, 3 to 12 September
    text(ax, 0.1, 1.55, 'Reporting clock (days in September)', size=8, bold=True, color=TEAL, ha='left')
    d0, d1 = 3, 12
    cx0, cx1 = 0.55, 4.85
    def X(d):
        return cx0 + (d - d0) / (d1 - d0) * (cx1 - cx0)
    yc = 0.95
    ax.plot([X(d0), X(d1)], [yc, yc], color=GREY, lw=0.8)
    for d in range(d0, d1 + 1):
        ax.plot([X(d), X(d)], [yc - 0.04, yc + 0.04], color=GREY, lw=0.6)
        text(ax, X(d), yc - 0.14, str(d), size=6.8, color=GREY)
    ax.add_patch(matplotlib.patches.Rectangle((X(5), yc - 0.07), X(12) - X(5), 0.14, fc=RUST_LIGHT, ec='none', zorder=1))
    marks = [(3, 'event', GREY, 'c'), (4, 'site\ninformed', GREY, 'c'), (5, 'Day 0:\nsponsor receipt', TEAL, 'c'),
             (6, 'unblinded:\nravolixan', TEAL, 'l'), (12, 'due: 7-day\nSUSAR', RUST, 'c')]
    for d, lab, col, al in marks:
        ax.plot([X(d)], [yc], 'o', color=col, ms=5.5, zorder=3)
        if al == 'l':
            text(ax, X(d) - 0.03, yc + 0.3, lab, size=6.8, color=col, bold=True, ha='left')
        else:
            text(ax, X(d), yc + (0.3 if col != GREY else -0.4), lab, size=6.8, color=col, bold=col != GREY)
    text(ax, (X(5) + X(12)) / 2, yc - 0.42, 'life-threatening SUSAR: 7 days from Day 0', size=7, color=RUST, italic=True)
    save(fig, 'fig16_5')


if __name__ == '__main__':
    fig16_1(); fig16_2(); fig16_3(); fig16_4(); fig16_5()
