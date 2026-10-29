# Figures for Chapter 10.
import numpy as np
from figlib import *


def fig10_1():
    """Four routes by which therapeutic proteins take part in interactions (Section 10.1)."""
    fig, ax = diagram(3.22)
    cx = [1.5, 2.8, 4.1]
    cw = 1.08
    bh = 0.4
    rows = [
        ('Cytokine-mediated', 'protein acts on a small molecule',
         [('Anti-cytokine protein', 'teal'), ('Inflammation relieved; CYP activity recovers', 'white'),
          ('Exposure to CYP substrate changes', 'rust')]),
        ('Immunogenicity', 'small molecule acts on a protein',
         [('Methotrexate added to infliximab', 'light'), ('Fewer antibodies against the drug', 'white'),
          ('Protein exposure maintained [2]', 'teal')]),
        ('Pharmacodynamic', 'effects add',
         [('Two or more immunomodulators', 'teal'), ('Additive immuno-suppression', 'white'),
          ('Infection', 'rust')]),
        ('Conjugate payload', 'a small-molecule component',
         [('Antibody–drug conjugate releases payload', 'teal'), ('Payload is a CYP3A substrate', 'white'),
          ('Inhibitor or inducer changes payload exposure', 'rust')]),
    ]
    y0, step = 2.62, 0.8
    for k, (t, s, chain) in enumerate(rows):
        y = y0 - k * step
        text(ax, 0.1, y + bh / 2 + 0.08, t, size=8.5, bold=True, color=TEAL, ha='left')
        text(ax, 0.1, y + bh / 2 - 0.12, s, size=7, color=GREY, ha='left', italic=True)
        for j, (lab, st) in enumerate(chain):
            box(ax, cx[j], y, cw, bh + 0.08, lab, style=st, size=7)
            if j < 2:
                arrow(ax, (cx[j] + cw + 0.03, y + (bh + 0.08) / 2), (cx[j + 1] - 0.03, y + (bh + 0.08) / 2), lw=1.1)
        if k < 3:
            ax.plot([0.1, TEXT_W - 0.1], [y - 0.16, y - 0.16], color=RULE, lw=0.6)
    save(fig, 'fig10_1')


def fig10_2():
    """Disease-drug-drug interaction: inflammation, CYP activity and substrate exposure over time. Schematic."""
    fig, axes = chart(3.2, nrows=3, sharex=True, gridspec_kw={'hspace': 0.3})
    fig.subplots_adjust(left=0.27, right=0.97, top=0.89, bottom=0.1)
    t = np.linspace(0, 10, 800)
    t_on, t_off = 2.0, 6.5

    def step(t, a, b, k_dn, k_up, lag=0.0):
        """Level a before t_on, moves to b after t_on (rate k_dn), back to a after t_off+lag (rate k_up)."""
        y = np.full_like(t, a)
        m = (t >= t_on) & (t < t_off + lag)
        y[m] = b + (a - b) * np.exp(-k_dn * (t[m] - t_on))
        y_end = b + (a - b) * np.exp(-k_dn * (t_off + lag - t_on))
        m2 = t >= t_off + lag
        y[m2] = a + (y_end - a) * np.exp(-k_up * (t[m2] - t_off - lag))
        return y
    infl = step(t, 1.0, 0.12, 3.0, 0.9, lag=0.9)
    cyp = step(t, 0.35, 0.95, 2.4, 0.8, lag=1.1)
    expo = step(t, 0.95, 0.4, 2.4, 0.8, lag=1.1)
    rows = [(infl, 'Inflammation\n(IL-6, CRP)', RUST, 'controlled within days'),
            (cyp, 'CYP3A4\nactivity', TEAL, 'suppression relieved'),
            (expo, 'Substrate exposure\nat unchanged dose', SAND_DARK, 'falls within a week [8]')]
    for a, (y, lab, c, ann), ypos in zip(axes, rows, [0.45, 0.62, 0.72]):
        a.axvspan(t_on, t_off, color=TEAL_LIGHT, lw=0, zorder=0)
        a.plot(t, y, color=c, lw=1.8)
        a.set_ylim(0, 1.15)
        a.set_yticks([])
        a.set_xlim(0, 10)
        a.spines['left'].set_color(RULE)
        a.text(-0.03, 0.5, lab, transform=a.transAxes, ha='right', va='center', fontsize=8, color=INK)
        a.text(t_on + 1.7, ypos, ann, fontsize=6.8, color=GREY, style='italic', va='center')
    axes[0].text((t_on + t_off) / 2, 1.22, 'IL-6 receptor antagonist given', fontsize=7.5, color=TEAL,
                 ha='center', va='bottom')
    axes[0].text(t_off + 0.1, 1.22, 'stopped, or disease flares', fontsize=7.5, color=GREY, ha='left', va='bottom')
    axes[2].text(t_off + 0.25, 0.2, 'effect may persist for\nweeks after stopping [10]', fontsize=6.8,
                 color=GREY, style='italic', va='center')
    axes[-1].set_xticks([])
    axes[-1].set_xlabel('Time', fontsize=8)
    save(fig, 'fig10_2')


def fig10_5():
    """Worked Case 10.1: tocilizumab, CRP, cyclosporine trough and creatinine (fictional)."""
    fig = plt.figure(figsize=(TEXT_W, 3.6))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.62, 1.25, 1.0], hspace=0.2,
                          left=0.16, right=0.96, top=0.95, bottom=0.11)
    axe, axc, axr = (fig.add_subplot(gs[i]) for i in range(3))
    xl = (-45, 66)
    for a in (axe, axc, axr):
        a.set_xlim(*xl)
        a.spines[['top', 'right']].set_visible(False)
        a.tick_params(length=3, width=0.6)
        a.axvspan(-20, 35, color=RUST_LIGHT, alpha=0.55, lw=0, zorder=0)
    # events
    axe.axis('off')
    axe.set_ylim(0, 1)
    for d in (1, 29):
        axe.plot(d, 0.66, marker='v', color=TEAL, ms=7)
    axe.text(15, 0.42, 'tocilizumab, days 1 and 29', fontsize=7, color=TEAL, ha='center', va='center')
    axe.plot(38, 0.66, marker='D', color=RUST, ms=5)
    axe.text(40.5, 0.66, 'biopsy: rejection, day 38', fontsize=7, color=RUST, ha='left', va='center')
    axe.text(-44, 0.42, 'CRP 46 mg/L before', fontsize=7, color=GREY, ha='left', va='center')
    axe.text(38, 0.42, 'CRP 2 mg/L, day 35', fontsize=7, color=GREY, ha='left', va='center')
    axe.text(7.5, 1.02, 'no trough measured', fontsize=7, color=RUST, ha='center', va='center', style='italic')
    # cyclosporine trough
    axc.axhspan(75, 125, color=TEAL_LIGHT, lw=0, zorder=0.5)
    axc.text(65, 120, 'target 75–125', fontsize=6.8, color=TEAL, ha='right', va='top')
    axc.fill_between([-45, -22], 92, 110, color=TEAL_MID, alpha=0.6, lw=0, zorder=1)
    axc.text(-44, 88, 'previous year:\n92 to 110', fontsize=6.8, color=TEAL, ha='left', va='top')
    axc.plot(-20, 104, 'o', color=TEAL, ms=5, zorder=3)
    axc.plot(35, 52, 'o', color=RUST, ms=5, zorder=3)
    axc.text(-18, 108, '104', fontsize=7.5, color=INK, va='bottom')
    axc.text(37.5, 52, '52', fontsize=7.5, color=RUST, va='center', fontweight='bold')
    axc.text(7.5, 66, 'not measured: when it fell is unknown', fontsize=6.8, color=GREY, style='italic', ha='center', va='top')
    axc.set_ylim(30, 135)
    axc.set_yticks([50, 75, 100, 125])
    axc.set_ylabel('Cyclosporine\ntrough (ng/mL)', fontsize=8)
    axc.set_xticks([-20, 1, 29, 35, 60])
    axc.tick_params(labelbottom=False)
    # creatinine
    axr.fill_between([-45, -22], 118, 126, color=SAND_BORDER, alpha=0.8, lw=0)
    axr.plot([35, 60], [168, 134], color=SAND_DARK, lw=1.4, marker='o', ms=5)
    axr.text(-44, 132, 'previous year: 118 to 126', fontsize=6.8, color=SAND_DARK, ha='left', va='bottom')
    axr.text(33, 168, '168', fontsize=7.5, color=INK, ha='right', va='center')
    axr.text(58, 134, '134', fontsize=7.5, color=INK, ha='right', va='top')
    axr.set_ylim(105, 180)
    axr.set_yticks([120, 150, 180])
    axr.set_ylabel('Creatinine\n(µmol/L)', fontsize=8)
    axr.set_xticks([-20, 1, 29, 35, 60])
    axr.set_xlabel('Day', fontsize=8)
    save(fig, 'fig10_5')


def fig10_3():
    """Simvastatin AUC after a single dose of an IL-6 receptor antagonist (Section 10.2)."""
    rows = [('Tocilizumab, 1 week (12 patients) [8]', 43, 34, 55, '43% (34–55)'),
            ('Tocilizumab, 5 weeks [8]', 61, 47, 78, '61% (47–78)'),
            ('Sarilumab, 1 week (19 patients) [9]', 54.7, 47.2, 63.3, '54.7% (47.2–63.3)')]
    fig, ax = chart(1.9)
    fig.subplots_adjust(left=0.4, right=0.78, top=0.95, bottom=0.25)
    n = len(rows)
    for i, (lab, est, lo, hi, txt) in enumerate(rows):
        y = n - 1 - i
        ax.plot([lo, hi], [y, y], color=TEAL, lw=1.8)
        ax.plot(est, y, 's', color=TEAL, ms=5.5)
        ax.text(1.03, y, txt, transform=ax.get_yaxis_transform(), fontsize=7.5, va='center')
    ax.axvline(100, color=GREY, lw=0.8)
    ax.text(98, n - 0.55, 'no change', fontsize=6.8, color=GREY, ha='right', va='center', style='italic')
    ax.set_xlim(0, 110)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_ylim(-0.5, n - 0.3)
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=7.5)
    ax.tick_params(axis='y', length=0)
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Simvastatin AUC, % of value without the biologic (90% CI)', fontsize=7.5)
    save(fig, 'fig10_3')


def fig10_4():
    """Calculation 10.1 as bars: relief of CYP3A4 suppression raises clearance and lowers the trough."""
    fig, (a1, a2) = chart(2.6, ncols=2, gridspec_kw={'width_ratios': [1.25, 1], 'wspace': 0.45})
    fig.subplots_adjust(left=0.1, right=0.97, top=0.93, bottom=0.2)
    x = [0, 1]
    w = 0.55
    a1.bar(x, [0.90, 1.62], w, color=[TEAL_MID, TEAL])
    a1.bar(x, [0.10, 0.10], w, bottom=[0.90, 1.62], color=RULE)
    a1.text(0, 0.45, 'CYP3A4\n0.90', ha='center', va='center', fontsize=7.2, color='white', fontweight='bold')
    a1.text(1, 0.81, 'CYP3A4\n0.90 × 1.8', ha='center', va='center', fontsize=7.2, color='white', fontweight='bold')
    a1.text(0.36, 0.95, 'other 0.10', ha='left', va='center', fontsize=6.8, color=GREY)
    a1.text(0, 1.05, '1.00', ha='center', va='bottom', fontsize=8, fontweight='bold')
    a1.text(1, 1.77, '1.72', ha='center', va='bottom', fontsize=8, fontweight='bold')
    a1.set_xticks(x, ['Active\ninflammation', 'After the\nbiologic'])
    a1.set_ylim(0, 2.0)
    a1.set_yticks([0, 0.5, 1.0, 1.5])
    a1.set_ylabel('Clearance (relative units)', fontsize=8)
    a2.bar(x, [100, 58], w, color=[TEAL, RUST])
    a2.text(0, 102, '100', ha='center', va='bottom', fontsize=8, fontweight='bold')
    a2.text(1, 60, 'about 58', ha='center', va='bottom', fontsize=8, fontweight='bold', color=RUST)
    a2.set_xticks(x, ['Before', 'After,\nsame dose'])
    a2.set_ylim(0, 120)
    a2.set_ylabel('Trough (ng/mL)', fontsize=8)
    save(fig, 'fig10_4')


if __name__ == '__main__':
    fig10_1(); fig10_2(); fig10_3(); fig10_4(); fig10_5()
