# Figures for Chapter 20.
import datetime as dt
from figlib import *


def fig20_1():
    """Signal management stages (GVP Module IX) and the decision each one makes."""
    stages = [
        ('Detection', 'Statistical screens and case review. For interaction signals, clinical review of the cases carries much of the weight.'),
        ('Validation', 'Enough evidence of a new association, or a new aspect of a known one, to justify further analysis? '
                       'Outcome: validated; not validated, with the reason; or monitoring.'),
        ('Analysis and prioritization', 'How urgently, and with what resources? A profile across six criteria, not a score.'),
        ('Assessment', 'What does all the evidence show? Is a change to benefit–risk, labeling, or risk minimization needed?'),
        ('Recommendation for action', 'What action, by whom, and by when?'),
        ('Exchange of information', 'Who must be told, and how? Regulatory notification; periodic report signal sections.'),
    ]
    h = 3.85
    fig, ax = diagram(h)
    sx, sw = 0.42, 1.55
    qx = sx + sw + 0.22
    qw = TEXT_W - 0.1 - qx
    bh, gap = 0.5, 0.12
    top = h - 0.1
    ys = [top - bh - k * (bh + gap) for k in range(len(stages))]
    for k, ((name, q), y) in enumerate(zip(stages, ys)):
        box(ax, sx, y, sw, bh, name, style='teal', size=8.5, wrapw=20)
        box(ax, qx, y, qw, bh, q, style='sand', size=7.5, align='left', wrapw=66)
        arrow(ax, (sx + sw + 0.02, y + bh / 2), (qx - 0.02, y + bh / 2), color=SAND_DARK, lw=0.8, head=5)
        if k < len(stages) - 1:
            arrow(ax, (sx + sw / 2, y - 0.01), (sx + sw / 2, y - gap + 0.01), head=5)
    # monitoring loop: validation back to detection
    xl = sx - 0.16
    yv, yd = ys[1] + bh / 2, ys[0] + bh / 2
    ax.plot([sx - 0.01, xl, xl], [yv, yv, yd], color=RUST, lw=1.0, ls=(0, (3, 2)), zorder=1)
    arrow(ax, (xl, yd), (sx - 0.01, yd), color=RUST, lw=1.0, head=6)
    text(ax, xl - 0.1, (yv + yd) / 2, 'monitoring', size=6.5, color=RUST, italic=True, rotation=90)
    save(fig, 'fig20_1')


def fig20_3():
    """Reporting rates with and without an inhibitor across assumed shares of exposure (Calculation 20.1)."""
    shares = [s / 1000 for s in range(10, 201)]
    w = [21 / (180 * s) for s in shares]          # per 1,000 patient-years
    wo = [26 / (180 * (1 - s)) for s in shares]
    fig, ax = chart(2.8)
    x = [s * 100 for s in shares]
    ax.plot(x, w, color=RUST, lw=1.8)
    ax.plot(x, wo, color=TEAL, lw=1.8)
    ax.axhline(0.26, color=GREY, lw=0.8, ls=(0, (4, 2)))
    ax.set_yscale('log')
    ax.set_ylim(0.08, 30)
    ax.set_xlim(0, 21)
    ax.set_yticks([0.1, 0.3, 1, 3, 10, 30])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'))
    ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xticks([0, 2, 5, 10, 15, 20])
    ax.set_xlabel('Assumed share of ravolixan patient-years with a CYP3A4 inhibitor (%), hypothetical', fontsize=8)
    ax.set_ylabel('Reports per 1,000 patient-years', fontsize=8)
    # marked assumptions from Calculation 20.1
    for s, a, b, r in [(2, 5.8, 0.15, 'ratio about 40'), (10, 1.2, 0.16, 'ratio about 7')]:
        ax.plot([s, s], [b, a], color=GREY, lw=0.8, zorder=1)
        ax.plot([s], [a], 'o', color=RUST, ms=5, zorder=3)
        ax.plot([s], [b], 'o', color=TEAL, ms=5, zorder=3)
        ax.text(s + 0.35, a, f'{a:g}', ha='left', va='bottom', fontsize=8, color=RUST, fontweight='bold')
        ax.text(s + 0.35, b * 0.88, f'{b:g}', ha='left', va='top', fontsize=8, color=TEAL, fontweight='bold')
        ax.text(s + 0.35, (a * b) ** 0.5, r, ha='left', va='center', fontsize=7.5, color=INK, style='italic')
    ax.text(20.8, 21 / (180 * 0.2) * 1.15, 'With an inhibitor', ha='right', va='bottom', fontsize=8, color=RUST)
    ax.text(20.8, 0.185, 'Without an inhibitor', ha='right', va='bottom', fontsize=8, color=TEAL)
    ax.text(20.8, 0.27, 'Overall 0.26', ha='right', va='bottom', fontsize=7.5, color=GREY)
    fig.tight_layout()
    save(fig, 'fig20_3')


def fig20_5():
    """Timeline of signal RVX-SIG-2026-004 (fictional dates from Worked Case 20.1)."""
    fig, ax = diagram(3.1)
    d0, d1 = dt.date(2026, 6, 20), dt.date(2026, 12, 25)
    x0, x1 = 0.3, TEXT_W - 0.3
    def X(d):
        return x0 + (d - d0).days / (d1 - d0).days * (x1 - x0)
    yl = 1.62
    ax.plot([x0, x1], [yl, yl], color=GREY, lw=1.2, zorder=1)
    for m in range(7, 13):
        d = dt.date(2026, m, 1)
        ax.plot([X(d), X(d)], [yl - 0.04, yl + 0.04], color=GREY, lw=0.8)
        text(ax, X(d) + 0.03, yl - 0.1, d.strftime('%b'), size=7, color=GREY, ha='left')
    step = 0.42
    # done (above the line): label to the right of the stem, at staggered levels
    done = [(dt.date(2026, 6, 30), 'Data lock point', '30 Jun', 3),
            (dt.date(2026, 7, 14), 'Detected in cumulative review', '14 Jul', 2),
            (dt.date(2026, 7, 28), 'Validated as a new aspect of a known risk', '28 Jul', 1),
            (dt.date(2026, 9, 15), 'Signal assessment report v1.0', '15 Sep', 2)]
    for d, lab, ds, lev in done:
        x = X(d)
        top = yl + 0.12 + (lev - 1) * step + 0.3
        ax.plot([x, x], [yl, top], color=TEAL, lw=0.8, zorder=1)
        ax.plot([x], [yl], 'o', color=TEAL, ms=5.5, zorder=3)
        text(ax, x + 0.05, top, ds, size=7.5, color=TEAL, bold=True, ha='left', va='top')
        text(ax, x + 0.05, top - 0.14, lab, size=7, color=INK, ha='left', va='top', wrapw=26)
    # due (below the line): label to the left of the stem, at staggered levels
    due = [(dt.date(2026, 10, 30), 'Targeted follow-up of 4 reduced-dose and 9 indeterminate reports', '30 Oct', 1),
           (dt.date(2026, 11, 30), 'PBPK simulations and concentration–QTc prediction', '30 Nov', 2),
           (dt.date(2026, 12, 15), 'Drug utilization feasibility; next review', '15 Dec', 3)]
    for d, lab, ds, lev in due:
        x = X(d)
        bot = yl - 0.25 - (lev - 1) * step
        ax.plot([x, x], [yl, bot - 0.3], color=SAND_DARK, lw=0.8, zorder=1, ls=(0, (2, 1.5)))
        ax.plot([x], [yl], 'o', mfc='white', mec=SAND_DARK, mew=1.3, ms=5.5, zorder=3)
        text(ax, x - 0.05, bot, ds, size=7.5, color=SAND_DARK, bold=True, ha='right', va='top')
        text(ax, x - 0.05, bot - 0.14, lab, size=7, color=INK, ha='right', va='top', wrapw=30)
    text(ax, x0, 0.12, 'Filled: done. Open: recommendation due.', size=7, color=GREY, italic=True, ha='left')
    save(fig, 'fig20_5')




def fig20_2():
    """Escalation of a validated, high-priority signal, with the ravolixan decisions."""
    fig, ax = diagram(3.45)
    h = 3.45
    # left: the signal and the committee
    box(ax, 0.1, 2.35, 1.35, 0.75, 'Validated signal, high priority', style='teal', size=8.5, wrapw=16)
    box(ax, 0.1, 0.85, 1.35, 1.15, 'Authority over labeling and risk minimization proposals. '
        'Records what is decided, by when, on what evidence.', style='light', size=7, title='Safety review committee',
        align='left', wrapw=24)
    arrow(ax, (0.775, 2.34), (0.775, 2.02))
    # right: three outputs
    rx, rw, bh = 1.85, TEXT_W - 0.1 - 1.85, 0.92
    outs = [('Better information first', 'Targeted follow-up, a drug utilization study, or new modeling.',
             'RVX-SIG-2026-004: follow-up, PBPK and concentration–QTc work, utilization feasibility.'),
            ('Labeling and risk minimization', 'Options evaluated (Chapter 23).',
             'RVX-SIG-2026-004: evaluation after follow-up and PBPK report.'),
            ('Regulatory communication', 'Validated-signal notification or emerging safety issue (EU); '
             'periodic report signal sections; FDA expectations (US).',
             'RVX-SIG-2026-004: not an emerging safety issue for now; next PBRER signal section.')]
    ys = [2.4, 1.33, 0.26]
    for (t, s, case), y in zip(outs, ys):
        box(ax, rx, y, rw, bh, '', style='white')
        text(ax, rx + 0.1, y + bh - 0.12, t, size=8.5, bold=True, color=TEAL, ha='left', va='top')
        text(ax, rx + 0.1, y + bh - 0.33, s, size=7.5, ha='left', va='top', wrapw=64)
        text(ax, rx + 0.1, y + 0.08, case, size=7, color=RUST, italic=True, ha='left', va='bottom', wrapw=74)
        arrow(ax, (1.47, 1.375), (rx - 0.02, y + bh / 2), color=GREY, lw=0.9, head=6)
    text(ax, 0.1, 0.42, 'Escalation is not\nthe same as action.', size=7.5, color=GREY, italic=True, ha='left',
         va='center')
    save(fig, 'fig20_2')


def fig20_4():
    """Previous awareness, part by part, for the two ravolixan signals."""
    fig, ax = diagram(3.95)
    lx, lw = 0.1, 1.45
    cx = [1.65, 3.45]
    cw = 1.75
    rows = ['Interaction already described?', 'Event already described?',
            'Link at this severity, with this precipitant?', 'Labeled advice followed and sufficient?']
    A = [('Yes: avoid strong, reduce dose with moderate inhibitors', 0),
         ('QT prolongation, yes. Torsade de pointes and death: not seen in development', 1),
         ('Inhibitors that prolong QT themselves: combined effect not addressed', 1),
         ('8 used contrary to labeling; 4 events after dose reduction', 1)]
    B = [('Yes: avoid strong inducers', 0), ('Yes: reduced efficacy', 0),
         ('Yes: rifampin AUC ratio 0.18 quantifies it; all 11 non-serious', 0),
         ('St John’s wort not named: clarity of wording, not a new risk', 0)]
    top = 3.5
    rh, gap = 0.56, 0.07
    text(ax, cx[0] + cw / 2, top + 0.22, 'Signal A: QT events with inhibitors', size=8, bold=True, color=RUST)
    text(ax, cx[1] + cw / 2, top + 0.22, 'Signal B: loss of efficacy with inducers', size=8, bold=True, color=TEAL)
    for i, r in enumerate(rows):
        y = top - (i + 1) * rh - i * gap
        text(ax, lx, y + rh / 2, r, size=7.5, ha='left', wrapw=24, bold=False)
        for j, (cells, x) in enumerate(zip((A, B), cx)):
            s, new = cells[i]
            box(ax, x, y, cw, rh, s, style='rust' if new else 'grey', size=7, wrapw=34)
    yb = top - 4 * rh - 3 * gap - 0.62
    box(ax, cx[0], yb, cw, 0.48, 'Validated: new aspect of a known risk', style='accent', size=8, wrapw=26)
    box(ax, cx[1], yb, cw, 0.48, 'Not validated: monitoring, with reopening criteria', style='sand', size=7.5,
        wrapw=30)
    text(ax, lx, yb + 0.24, 'Outcome', size=7.5, bold=True, ha='left')
    for x in cx:
        arrow(ax, (x + cw / 2, yb + 0.48 + 0.12), (x + cw / 2, yb + 0.48 + 0.01), head=5)
    text(ax, lx, 0.1, 'Shaded rust: something new. Any new part, or advice that fails, is enough to validate.',
         size=7, color=GREY, italic=True, ha='left')
    save(fig, 'fig20_4')


if __name__ == '__main__':
    fig20_1(); fig20_2(); fig20_3(); fig20_4(); fig20_5()
