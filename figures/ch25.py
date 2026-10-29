# Figures for Chapter 25 (case workshop; ravolixan and the case are fictional).
import numpy as np
from figlib import *


def exposure(t):
    """Calculation 25.1 model: relative average ravolixan exposure, t in hours from the start of Day 1.
    Inhibition fully established from the start of Day 3; bioavailability x1.5 at once; clearance
    component approaches 2.6-fold with the new half-life of about 36 h."""
    t = np.asarray(t, dtype=float)
    after = 1.5 * (1 + 1.6 * (1 - 0.5 ** ((t - 48) / 36)))
    return np.where(t < 48, 1.0, after)


def fig25_2():
    """Calculation 25.1: exposure rising by Day 5, and the QT effect it predicts versus the observed change."""
    fig, (a1, a2) = chart(2.7, ncols=2, gridspec_kw={'width_ratios': [1.55, 1], 'wspace': 0.32})
    t_ev = 4 * 24 + 10.5
    t1 = np.linspace(0, t_ev, 400)
    t2 = np.linspace(t_ev, 11 * 24, 300)
    day = lambda t: t / 24 + 1
    a1.plot(day(t1), exposure(t1), color=TEAL, lw=1.8)
    a1.plot(day(t2), exposure(t2), color=TEAL, lw=1.2, ls=(0, (3, 2)))
    a1.axhline(3.9, color=GREY, lw=0.8, ls=(0, (1, 2)))
    a1.text(1.1, 3.98, 'new steady state, PBPK 3.9', fontsize=7, color=GREY, va='bottom')
    e_ev = float(exposure(t_ev))
    a1.plot(day(t_ev), e_ev, 'o', color=RUST, ms=5.5, zorder=3)
    a1.annotate('Day 5, 10:30: torsade;\nabout 3.1-fold', xy=(day(t_ev), e_ev), xytext=(6.4, 1.75),
                fontsize=7.5, color=RUST, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color=RUST, lw=0.8))
    a1.text(9.0, 3.55, 'had clarithromycin\ncontinued', fontsize=7, color=TEAL, ha='center', va='top', style='italic')
    a1.text(3.4, 0.55, 'inhibition assumed\ncomplete from Day 3', fontsize=7, color=GREY, ha='left', va='bottom')
    a1.set_xlim(1, 11.2)
    a1.set_ylim(0, 4.5)
    a1.set_xticks(range(1, 12))
    a1.set_xlabel('Day of clarithromycin', fontsize=8)
    a1.set_ylabel('Ravolixan exposure, fold baseline', fontsize=8)
    # right panel: predicted vs observed QTcF increase
    a2.barh([1, 0], [14, 136], color=[TEAL, RUST], height=0.55)
    a2.text(14 + 4, 1, 'about 14 ms', va='center', fontsize=7.5)
    a2.text(136 - 4, 0, '136 ms', va='center', ha='right', fontsize=7.5, color='white', fontweight='bold')
    a2.set_yticks([1, 0], ['Predicted from\nthorough QT data', 'Observed\n(572 − 436 ms)'], fontsize=7.5)
    a2.set_xlim(0, 150)
    a2.set_ylim(-0.6, 1.6)
    a2.set_xticks([0, 50, 100, 150])
    a2.set_xlabel('Rise in QTcF, ms', fontsize=8)
    a2.spines['left'].set_visible(False); a2.tick_params(axis='y', length=0)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.96, bottom=0.17)
    save(fig, 'fig25_2')


def fig25_3():
    """How the information and the assessment changed across the three stages."""
    fig, ax = diagram(3.65)
    x0, cw, cg = 0.62, 1.44, 0.13
    xs = [x0 + k * (cw + cg) for k in range(3)]
    heads = ['Stage 1 · 12 March\ninitial report (Day 0)', 'Stage 2 · 18 March\nfollow-up 1', 'Stage 3 · 1 April\nfollow-up 2']
    src = ['Hospital pharmacist, by telephone', 'Treating cardiologist', 'GP record, two pharmacies, patient']
    info = ['Ravolixan; clarithromycin "a few days before"; collapse, "long QT", "twisting VT"; potassium "low"',
            'Clarithromycin from Day 1, event Day 5; QTcF 572 ms (436 before); K 2.8, Mg 0.62; thiazide; recurrent TdP',
            'Loperamide about 12 mg a day from Day 3; diarrhea; prodrome Day 4; K 3.3 in January; GP unaware of ravolixan']
    assess = ['Interaction plausible; its contribution cannot be assessed',
              'Event defined; timing fits; predicted QT effect far short: look for more',
              'Interaction one plausible, preventable contributor among several']
    clock = ['Initial report due 27 March', 'Included in the initial report', 'New clock: follow-up due 16 April']
    rows = [(3.0, 0.42, 'Stage', None), (2.58, 0.34, 'Source', src), (1.66, 0.84, 'New facts', info),
            (0.88, 0.7, 'Assessment', assess), (0.4, 0.4, 'Reporting', clock)]
    for k, x in enumerate(xs):
        box(ax, x, 3.04, cw, 0.48, heads[k], style='teal', size=7.3, wrapw=40)
        box(ax, x, 2.58, cw, 0.36, src[k], style='white', size=6.8, wrapw=32)
        box(ax, x, 1.62, cw, 0.88, info[k], style='light', size=6.8, wrapw=31, align='left')
        box(ax, x, 0.84, cw, 0.7, assess[k], style='sand', size=6.8, wrapw=31, align='left')
        box(ax, x, 0.38, cw, 0.38, clock[k], style='grey', size=6.8, wrapw=32)
        if k < 2:
            arrow(ax, (x + cw + 0.015, 3.28), (x + cw + cg - 0.015, 3.28), color=TEAL)
    for y, lab in [(3.28, 'Stage'), (2.76, 'Source'), (2.06, 'New\nfacts'), (1.19, 'Assess-\nment'), (0.57, 'Clock')]:
        text(ax, 0.33, y, lab, size=7, color=GREY, bold=True)
    note(ax, 'Each stage is written down before the next arrives; Stage 1 alone would have overstated the interaction.',
         y=0.15, size=6.8)
    save(fig, 'fig25_3')


def fig25_5():
    """Contributors to the event: clarithromycin acts by three routes; the interaction is one of several."""
    fig, ax = diagram(3.3)
    xl, wl = 0.1, 1.35
    xm, wm = 1.85, 1.5
    xr, wr = 3.85, 1.35
    box(ax, xl, 2.55, wl, 0.5, 'Ravolixan 40 mg, concentration-dependent QT effect', style='light', size=7, wrapw=26)
    box(ax, xl, 1.45, wl, 0.55, 'Clarithromycin 500 mg twice daily', style='teal', size=7.3, wrapw=22)
    text(ax, xl + wl / 2, 1.3, 'prescribed by a GP unaware\nof ravolixan', size=6.5, color=GREY, italic=True, va='top')
    box(ax, xl, 0.25, wl, 0.45, 'Hydrochlorothiazide 25 mg', style='light', size=7, wrapw=26)
    box(ax, xm, 2.5, wm, 0.6, 'Ravolixan exposure up, about 3-fold by Day 5', style='light', size=7, wrapw=28)
    box(ax, xm, 1.0, wm, 0.36, 'Diarrhea from Day 3', style='white', size=7)
    box(ax, xm, 0.2, wm, 0.55, 'K 2.8 mmol/L, Mg 0.62 mmol/L', style='rust', size=7, wrapw=28)
    box(ax, xr, 2.5, wr, 0.6, 'Female, 67 years, heart rate 58/min', style='sand', size=7, wrapw=24,
        title=None)
    box(ax, xr, 1.3, wr, 0.75, 'Torsade de pointes, Day 5; QTcF 572 ms', style='accent', size=7.5, wrapw=22)
    box(ax, xr, 0.2, wr, 0.6, 'Loperamide about 12 mg a day (OTC); own QT liability', style='light', size=7, wrapw=24)
    c = GREY
    # ravolixan -> exposure
    arrow(ax, (xl + wl + 0.02, 2.8), (xm - 0.02, 2.8), color=c)
    # clarithromycin routes
    arrow(ax, (xl + wl + 0.02, 1.95), (xm + 0.2, 2.48), color=TEAL)
    text(ax, 1.42, 2.27, 'CYP3A4 and\nP-gp inhibition', size=6.5, color=TEAL, ha='right', va='center')
    arrow(ax, (xl + wl + 0.02, 1.72), (xr - 0.02, 1.72), color=TEAL)
    text(ax, 2.6, 1.82, 'own QT effect', size=6.8, color=TEAL, va='bottom')
    arrow(ax, (xl + wl + 0.02, 1.5), (xm + 0.2, 1.38), color=TEAL)
    text(ax, 1.48, 1.33, 'adverse\neffect', size=6.5, color=TEAL, ha='left', va='top')
    # diarrhea and thiazide -> electrolytes
    arrow(ax, (xm + wm / 2, 0.98), (xm + wm / 2, 0.77), color=c)
    arrow(ax, (xl + wl + 0.02, 0.47), (xm - 0.02, 0.47), color=c)
    # to the event
    arrow(ax, (xm + wm + 0.02, 2.75), (xr + 0.25, 2.07), color=c)
    arrow(ax, (xm + wm + 0.02, 0.6), (xr + 0.25, 1.28), color=c)
    arrow(ax, (xr + wr / 2, 2.48), (xr + wr / 2, 2.07), color=SAND_DARK)
    arrow(ax, (xr + wr / 2, 0.82), (xr + wr / 2, 1.28), color=c, ls=(0, (3, 2)))
    save(fig, 'fig25_5')


def fig25_1():
    """Published evidence the reviewer brings to the case (refs 3-6), as small multiples."""
    fig, axes = chart(3.3, ncols=2, nrows=2, gridspec_kw={'wspace': 0.75, 'hspace': 0.95})
    (a, b), (c, d) = axes

    def hbars(ax, labels, vals, colors, fmt, xmax, xlabel, title):
        y = list(range(len(vals)))[::-1]
        ax.barh(y, vals, color=colors, height=0.55)
        for yi, v in zip(y, vals):
            ax.text(v + xmax * 0.03, yi, fmt(v), va='center', fontsize=7.5, fontweight='bold')
        ax.set_yticks(y, labels, fontsize=7.2)
        ax.set_xlim(0, xmax)
        ax.set_ylim(-0.6, len(vals) - 0.4)
        ax.set_xlabel(xlabel, fontsize=7)
        ax.tick_params(axis='y', length=0)
        ax.tick_params(axis='x', labelsize=7)
        ax.spines['left'].set_visible(False)
        ax.set_title(title, fontsize=7.3, color=GREY, fontweight='normal', loc='left')
    hbars(a, ['Women', 'Two or more\nrisk factors'], [71, 71], [RUST, RUST], lambda v: f'{v}%', 100,
          '% of 249 published cases', 'Torsade with non-cardiac drugs [3]')
    hbars(b, ['With another\nQT drug', 'Hypokalemia'], [38.7, 15.9], [TEAL, TEAL], lambda v: f'{v}%', 50,
          '% of courses or users', 'Macrolides and quinolones in hospital [4]')
    hbars(c, ['Abuse', 'Treating\ndiarrhea'], [22, 17], [SAND_DARK, SAND_DARK], lambda v: f'{v}', 30,
          'Cases (of 48 serious cardiac)', 'Loperamide cardiac reports [5]')
    hbars(d, ['AUC', 'Cmax'], [3.8, 2.9], [TEAL_MID, TEAL_MID], lambda v: f'{v}-fold', 5,
          'Ratio with itraconazole', 'Loperamide with itraconazole [6]')
    d.axvline(1, color=GREY, lw=0.8, ls=(0, (3, 2)))
    fig.subplots_adjust(left=0.15, right=0.96, top=0.92, bottom=0.12)
    save(fig, 'fig25_1')


def fig25_4():
    """QTcF and potassium over time: every contributor removed at once, so recovery does not discriminate."""
    fig, (a1, a2) = chart(3.0, nrows=2, sharex=True, gridspec_kw={'height_ratios': [1.6, 1], 'hspace': 0.12})
    # x positions: pre-treatment and January shown left of an axis break; days 1 to 29 to scale
    qx, qv = [5.44, 6, 8, 11, 29], [572, 528, 489, 462, 441]
    for a in (a1, a2):
        a.axvspan(1, 5.44, color=TEAL_LIGHT, zorder=0)
        a.axvline(5.44, color=RUST, lw=0.9, ls=(0, (3, 2)))
    a1.plot([-6], [436], 'o', color=GREY, ms=5)
    a1.text(-6, 448, '436', ha='center', fontsize=7.5, color=GREY)
    a1.plot(qx, qv, '-o', color=TEAL, ms=4.5)
    offs = {5.44: (-0.5, 0, 'right'), 6: (0.6, 4, 'left'), 8: (-0.5, -16, 'right'), 11: (0.3, 10, 'left'), 29: (0, 10, 'center')}
    for x, v in zip(qx, qv):
        dx, dy, ha = offs[x]
        a1.text(x + dx, v + dy, str(v), ha=ha, va='center' if dy == 0 else 'bottom', fontsize=7.5,
                fontweight='bold' if x == 5.44 else 'normal')
    a1.axhline(500, xmin=0.35, color=GREY, lw=0.7, ls=(0, (1, 2)))
    a1.text(29.5, 503, '500 ms', fontsize=6.8, color=GREY, ha='right', va='bottom')
    a1.text(3.2, 428, 'clarithromycin, Days 1–5', fontsize=6.8, color=TEAL, va='bottom', ha='center', rotation=90)
    a1.text(6.2, 590, 'Day 5: ravolixan, clarithromycin and thiazide\nstopped; potassium and magnesium replaced',
            fontsize=6.8, color=RUST, va='top')
    a1.set_ylim(420, 600)
    a1.set_ylabel('QTcF, ms', fontsize=7.5)
    kx, kv = [-6, -3, 5.44, 29], [3.6, 3.3, 2.8, 4.2]
    a2.plot(kx[:2], kv[:2], 'o', color=GREY, ms=5)
    a2.plot(kx[2:], kv[2:], 'o', color=SAND_DARK, ms=5)
    for x, v in zip(kx, kv):
        a2.text(x + 0.6, v + 0.1, f'{v}', fontsize=7.5, ha='left',
                color=GREY if x < 0 else SAND_DARK, fontweight='bold' if v == 2.8 else 'normal')
    a2.set_ylim(2.4, 4.7)
    a2.set_ylabel('K, mmol/L', fontsize=7.5)
    a2.set_xlim(-8, 31)
    a2.set_xticks([-6, -3, 1, 5, 11, 29], ['Jul\n2025', '9 Jan', 'Day 1', 'Day 5', 'Day 11', '30 Mar'], fontsize=7)
    for a in (a1, a2):
        a.plot([-1.2, -0.6], [a.get_ylim()[0]] * 2, color='white', lw=3, clip_on=False, zorder=5)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.97, bottom=0.14)
    save(fig, 'fig25_4')


if __name__ == '__main__':
    fig25_1(); fig25_2(); fig25_3(); fig25_4(); fig25_5()
