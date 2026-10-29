# Figures for Chapter 22 (aggregate reports; ravolixan is fictional).
import numpy as np
from figlib import *


def fig22_1():
    """How interaction evidence moves through the PBRER sections (map in Section 22.2)."""
    fig, ax = diagram(3.45)
    # column headers
    for x, s in [(0.85, 'Data and inputs'), (2.7, 'Signal sections'), (4.47, 'Risk and balance')]:
        text(ax, x, 3.3, s, size=7.5, color=GREY, italic=True)
    # column 1: inputs
    c1, w1 = 0.1, 1.5
    box(ax, c1, 2.7, w1, 0.42, 'Cases in the safety database', style='light', size=8)
    others = ['5  Exposure and use', '7–9  Trials and studies', '11  Literature',
              '14  Late-breaking']
    ys = [1.85, 1.38, 0.91, 0.44]
    for s, y in zip(others, ys):
        box(ax, c1, y, w1, 0.36, s, style='white', size=7.5)
    # column 2
    c2, w2 = 1.95, 1.5
    box(ax, c2, 2.72, w2, 0.5, 'combination invisible', style='grey', size=7, title='6  Summary tabulations')
    box(ax, c2, 2.08, w2, 0.38, 'Co-reported drug search', style='teal', size=8)
    box(ax, c2, 1.38, w2, 0.46, 'source, dates, status', style='light', size=7, title='15  Signal overview')
    box(ax, c2, 0.44, w2, 0.66, 'closed signals; new information on known risks',
        style='light', size=7, title='16.2 / 16.3  Evaluation')
    # column 3
    c3, w3 = 3.75, 1.45
    col3 = [(2.6, '16.4  Characterization', 'frequency, severity, risk factors, interacting drug', 'light'),
            (1.88, '16.5  Risk minimization', 'was the advice on the combination followed?', 'rust'),
            (1.16, '18  Benefit–risk', 'risk conditional on the combination', 'light'),
            (0.44, '19  Conclusions', 'labeling, RMP, further studies', 'light')]
    for y, t, s, st in col3:
        box(ax, c3, y, w3, 0.56, s, style=st, size=7, title=t, align='left', wrapw=30)
    # arrows: database -> tabulations (dead end) and -> search
    arrow(ax, (c1 + w1 + 0.02, 2.96), (c2 - 0.02, 2.96), color=GREY, ls=(0, (3, 2)))
    ax.plot([c1 + w1 / 2, c1 + w1 / 2], [2.7, 2.6], color=TEAL, lw=1.1)
    ax.plot([c1 + w1 / 2, 1.78, 1.78], [2.6, 2.6, 2.27], color=TEAL, lw=1.1)
    arrow(ax, (1.78, 2.27), (c2 - 0.02, 2.27), color=TEAL)
    # search -> 15 -> 16.2/16.3
    arrow(ax, (c2 + w2 / 2, 2.06), (c2 + w2 / 2, 1.86), color=TEAL)
    arrow(ax, (c2 + w2 / 2, 1.36), (c2 + w2 / 2, 1.12), color=TEAL)
    # other inputs bracket -> 16.2/16.3
    xb = 1.78
    ax.plot([xb, xb], [ys[-1] + 0.18, ys[0] + 0.18], color=GREY, lw=1.0)
    for y in ys:
        ax.plot([c1 + w1 + 0.01, xb], [y + 0.18, y + 0.18], color=GREY, lw=1.0)
    arrow(ax, (xb, 0.77), (c2 - 0.02, 0.77), color=GREY)
    # 16.2/16.3 -> 16.4 via bus, then down column 3
    xbus = 3.6
    ax.plot([c2 + w2 + 0.01, xbus, xbus], [0.77, 0.77, 2.88], color=TEAL, lw=1.1)
    arrow(ax, (xbus, 2.88), (c3 - 0.02, 2.88), color=TEAL)
    xm = c3 + w3 / 2
    for ytop in (2.58, 1.86, 1.14):
        arrow(ax, (xm, ytop), (xm, ytop - 0.12), color=TEAL)
    note(ax, 'Grey dashed path: counts by MedDRA term alone never show the combination.', y=0.17, size=7)
    save(fig, 'fig22_1')


def fig22_2():
    """Reporting rates by period, and the co-exposure sensitivity analysis (Calculation 22.1)."""
    fig, (a1, a2) = chart(2.75, ncols=2, gridspec_kw={'width_ratios': [1, 1.15], 'wspace': 0.42})
    # left panel: reporting rates per 100,000 patient-years
    groups = ['All QT-related reports\n(cumulative 26.1)','With a CYP3A4\ninhibitor']
    before, interval = [19.3, 6.7], [39.3, 21.3]
    x = np.arange(2)
    bw = 0.34
    a1.bar(x - bw / 2 - 0.02, before, bw, color=TEAL_MID)
    a1.bar(x + bw / 2 + 0.02, interval, bw, color=TEAL)
    for xi, b, i in zip(x, before, interval):
        a1.text(xi - bw / 2 - 0.02, b + 1, f'{b}', ha='center', va='bottom', fontsize=7.5)
        a1.text(xi + bw / 2 + 0.02, i + 1, f'{i}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    for xi in x:
        a1.text(xi - bw / 2 - 0.02, 0.8, 'before', fontsize=6.5, color='white', ha='center', va='bottom', rotation=90)
        a1.text(xi + bw / 2 + 0.02, 0.8, 'interval', fontsize=6.5, color='white', ha='center', va='bottom', rotation=90)
    a1.set_xticks(x, groups, fontsize=7.5)
    a1.set_xlim(-0.55, 1.5)
    a1.set_ylim(0, 48)
    a1.set_ylabel('Reports per 100,000 patient-years', fontsize=7.5)
    a1.tick_params(axis='x', length=0)
    # right panel: ratio as a function of the unknown co-exposure fraction f
    f = np.linspace(0.015, 0.12, 200)
    ratio = (21 / 26) * (1 - f) / f
    a2.plot(f * 100, ratio, color=RUST, lw=1.6)
    for fp, lab in [(2, 'about 40'), (5, 'about 15'), (10, 'about 7')]:
        r = (21 / 26) * (1 - fp / 100) / (fp / 100)
        a2.plot(fp, r, 'o', color=RUST, ms=4.5, zorder=3)
        a2.text(fp + 0.45, r + 2.2, lab, fontsize=7.5, color=INK, va='bottom')
    a2.set_xlim(0, 12.5)
    a2.set_ylim(0, 58)
    a2.set_xticks([0, 2, 4, 6, 8, 10, 12])
    a2.set_xlabel('Assumed co-exposure, % of patient-years', fontsize=7.5)
    a2.set_ylabel('Ratio of reporting rates,\nwith vs without inhibitor', fontsize=7.5)
    a2.text(12.3, 52, 'Direction robust;\nsize depends on f.\nNot a relative risk.', fontsize=7, color=GREY,
            style='italic', ha='right', va='top', linespacing=1.25)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.2)
    save(fig, 'fig22_2')


def fig22_5():
    """What happened before and after the DLP, and where each item goes in the PBRER."""
    fig, ax = diagram(2.75)
    yl = 1.85  # timeline
    # shaded phases
    x_dlp, x_fin = 1.75, 4.15
    ax.add_patch(plt.Rectangle((x_dlp, 0.1), x_fin - x_dlp, 2.5, fc=TEAL_LIGHT, ec='none', alpha=0.55, zorder=0))
    ax.add_patch(plt.Rectangle((x_fin, 0.1), 5.2 - x_fin, 2.5, fc='#EEF1F2', ec='none', zorder=0))
    text(ax, (x_dlp + x_fin) / 2, 2.46, 'Report preparation', size=7.5, color=TEAL, italic=True)
    text(ax, (x_fin + 5.2) / 2, 2.46, 'After finalization', size=7.5, color=GREY, italic=True)
    # interval block
    box(ax, 0.1, yl - 0.24, 1.5, 0.48, 'PBRER interval\n1 Jul 2025 – 30 Jun 2026', style='teal', size=7.5, wrapw=40)
    ax.plot([1.6, 5.15], [yl, yl], color=GREY, lw=1.0, zorder=1)
    events = [(x_dlp, '30 Jun', 'DLP', RUST),
              (2.35, '14 Jul', 'signal\ndetected', TEAL),
              (2.95, '28 Jul', 'validated', TEAL),
              (3.55, '5 Sep', 'trial TdP\nreceived', TEAL),
              (x_fin, '8 Sep', 'PBRER\nfinalized', INK),
              (4.75, '15 Sep', 'assessment\ndue', GREY)]
    for x, d, s, c in events:
        ax.plot([x], [yl], 'o', ms=5, color=c, zorder=3)
        text(ax, x, yl + 0.2, d, size=7.5, bold=True, color=c)
        text(ax, x, yl - 0.27, s, size=7, color=INK, va='top')
    # destinations
    bh, by = 0.66, 0.2
    dest = [(0.1, 1.55, 'Cases received to the DLP', '16.3 preliminary findings; counts at the DLP', 'light'),
            (1.85, 1.15, 'Signal', '15: new, evaluation ongoing; 14: summary', 'light'),
            (3.08, 1.0, 'RVX-305 case', '14: late-breaking information', 'light'),
            (4.22, 0.98, 'Outcome', 'submitted as regions require; next PBRER', 'white')]
    for x, w, t, s, st in dest:
        box(ax, x, by, w, bh, s, style=st, size=6.8, title=t, align='left')
    # connectors from events to destinations
    for xe, xd in [(0.9, 0.9), (2.65, 2.42), (3.55, 3.58), (4.75, 4.71)]:
        ax.plot([xe, xd], [yl - (0.26 if xe < 1 else 0.6), by + bh + 0.02], color=RULE, lw=0.9, zorder=1)
    save(fig, 'fig22_5')


def fig22_3():
    """From search to comparison groups: the structure behind the signal and case tables."""
    fig, ax = diagram(3.3)
    cx = TEXT_W / 2
    box(ax, cx - 1.25, 2.85, 2.5, 0.34, '52 reports retrieved (SMQ, broad)', style='white', size=7.8)
    arrow(ax, (cx, 2.83), (cx, 2.65), color=GREY)
    box(ax, cx - 1.25, 2.27, 2.5, 0.36, '47 after deduplication (24 in the interval)', style='light', size=7.8)
    # split
    lx, lw = 0.1, 2.75
    rx, rw = 3.05, 2.15
    ax.plot([cx, cx], [2.25, 2.12], color=GREY, lw=1.1)
    ax.plot([lx + lw / 2, rx + rw / 2], [2.12, 2.12], color=GREY, lw=1.1)
    arrow(ax, (lx + lw / 2, 2.12), (lx + lw / 2, 1.97), color=TEAL)
    arrow(ax, (rx + rw / 2, 2.12), (rx + rw / 2, 1.97), color=GREY)
    box(ax, lx, 1.6, lw, 0.36, 'With a CYP3A4 inhibitor: 21 (13 in the interval)', style='teal', size=7.8, wrapw=60)
    box(ax, rx, 1.6, rw, 0.36, 'Without an inhibitor: 26', style='grey', size=7.8, bold=True)
    # drugs under the inhibitor group
    drugs = [('Clarithromycin', 9, RUST, 'strong'), ('Itraconazole', 2, RUST, 'strong'),
             ('Fluconazole', 7, TEAL, 'moderate'), ('Diltiazem', 3, TEAL, 'moderate')]
    dw, dg = 0.64, 0.063
    for k, (d, n, c, cls) in enumerate(drugs):
        x = lx + k * (dw + dg)
        box(ax, x, 1.0, dw, 0.48, '', style='rust' if cls == 'strong' else 'light', radius=0.04)
        text(ax, x + dw / 2, 1.34, d, size=6.8, color=INK)
        text(ax, x + dw / 2, 1.13, str(n), size=9, bold=True, color=c)
    text(ax, lx + dw + dg / 2, 0.9, 'strong', size=6.6, color=RUST, italic=True)
    text(ax, lx + 3 * dw + 2.5 * dg, 0.9, 'moderate', size=6.6, color=TEAL, italic=True)
    box(ax, lx, 0.25, lw, 0.5, 'Hypokalemia or hypomagnesemia 9; ECG-documented torsade 6; fatal 2',
        style='white', size=7, wrapw=52)
    box(ax, rx, 0.75, rw, 0.73, 'Another QT-prolonging drug 14; structural heart disease or electrolyte abnormality 12',
        style='white', size=7, wrapw=36)
    box(ax, rx, 0.25, rw, 0.4, 'Risk factors common in both groups', style='sand', size=7, wrapw=40)
    save(fig, 'fig22_3')


def fig22_4():
    """Benefit-risk integration of a conditional, preventable, poorly measured risk."""
    fig, ax = diagram(3.0)
    # nested populations
    box(ax, 0.1, 0.25, 2.85, 2.6, '', style='light', radius=0.12)
    text(ax, 0.22, 2.68, 'All patients treated for plaque psoriasis', size=7.8, bold=True, color=TEAL, ha='left')
    text(ax, 0.22, 2.46, 'Benefit established; balance positive when used as labeled', size=7, ha='left', wrapw=46)
    box(ax, 0.95, 0.4, 1.85, 1.7, '', style='rust', radius=0.1)
    text(ax, 1.07, 1.95, 'Taking a CYP3A4 inhibitor', size=7.5, bold=True, color=RUST, ha='left')
    text(ax, 1.07, 1.73, 'Risk concentrated here', size=7, ha='left')
    box(ax, 1.5, 0.55, 1.15, 0.95, 'plus hypokalemia, another QT drug, or heart disease', style='accent', size=6.8,
        wrapw=20, bold=False)
    # properties and consequences
    props = [('Conditional', 'The balance can be unfavorable for co-exposed patients while the indication stays positive'),
             ('Largely preventable', 'The main lever is risk minimization: avoid the combination or adjust the dose'),
             ('Poorly measured', 'Frequency is unknown, so no quantitative weighting')]
    y = 2.2
    for t, s in props:
        box(ax, 3.2, y, 2.0, 0.68, s, style='sand', size=6.8, title=t, align='left', wrapw=40, pad=0.05)
        y -= 0.8
    arrow(ax, (2.97, 1.5), (3.18, 1.5), color=SAND_DARK)
    note(ax, 'Region sizes are schematic, not proportional to exposure.', y=0.1, size=6.8)
    save(fig, 'fig22_4')


if __name__ == '__main__':
    fig22_1(); fig22_2(); fig22_3(); fig22_4(); fig22_5()
