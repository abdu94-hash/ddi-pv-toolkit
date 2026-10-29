# Figures for Chapter 12.
from figlib import *
from matplotlib.patches import Rectangle
import numpy as np


def _blank(a):
    a.set_xticks([]); a.set_yticks([])


def fig12_1():
    """Schematic laboratory trends: one that fits an interaction and two that do not."""
    fig, axes = chart(2.35, ncols=3)
    t = np.linspace(0, 10, 300)
    t0 = 3.0
    # 1. fits: rise after a lag, in the expected direction (inhibitor of warfarin metabolism)
    a = axes[0]
    y = 1 + 0.9 * (1 - np.exp(-np.clip(t - t0 - 1.0, 0, None) / 1.6))
    a.plot(t, y, color=TEAL)
    a.set_title('Fits: expected direction,\nafter a plausible lag', fontsize=8, color=TEAL, pad=4)
    # 2. too early: drop on day 1 of an inducer, where a slow fall would be expected
    a = axes[1]
    exp_ = 1.9 - 0.8 * (1 - np.exp(-np.clip(t - t0, 0, None) / 3.0))
    obs = np.where(t < t0, 1.9, np.where(t < t0 + 0.4, 1.9 - 0.8 * (t - t0) / 0.4, 1.1))
    a.plot(t, exp_, color=GREY, ls=(0, (3, 2)), lw=1.3)
    a.plot(t, obs, color=RUST)
    a.text(7.2, 1.62, 'expected with\ninduction', fontsize=6.8, color=GREY, ha='center', style='italic')
    a.text(6.0, 0.88, 'observed', fontsize=6.8, color=RUST, ha='center', style='italic')
    a.set_title('Too early for the\nmechanism', fontsize=8, color=RUST, pad=4)
    # 3. explained by illness: postoperative rise and fall, values inside the expected course
    a = axes[2]
    s = 1 + 1.1 * np.clip(t - t0, 0, None) * np.exp(-np.clip(t - t0, 0, None) / 1.4) / 1.4
    a.fill_between(t, s - 0.18, s + 0.18, color=SAND, lw=0)
    a.plot(t, s, color=SAND_DARK, lw=1.0, ls=(0, (3, 2)))
    for xi in (4.0, 5.2, 7.5):
        a.plot([xi], [1 + 1.1 * (xi - t0) * np.exp(-(xi - t0) / 1.4) / 1.4], 'o', color=TEAL, ms=4.5, zorder=3)
    a.text(8.3, 1.62, 'expected\ncourse after\nsurgery', fontsize=6.8, color=SAND_DARK, ha='center', style='italic')
    a.set_title('Explained by the illness\nor procedure', fontsize=8, color=SAND_DARK, pad=4)
    for a, lab in zip(axes, ['precipitant\nstarted', 'inducer\nstarted', 'surgery']):
        a.axvline(t0, color=GREY, lw=0.7, ls=(0, (1, 2)))
        a.text(t0 - 0.2, 0.62, lab, fontsize=6.8, color=GREY, ha='right', va='bottom')
        a.set_ylim(0.55, 2.3); a.set_xlim(0, 10)
        _blank(a)
        a.set_xlabel('Time', fontsize=7.5)
    axes[0].set_ylabel('Laboratory value', fontsize=7.5)
    fig.tight_layout(w_pad=1.2)
    save(fig, 'fig12_1')


def fig12_2():
    """Schematic concentration-time course: peak versus trough, and the slow climb to a new steady state."""
    fig, a = chart(2.6)
    dt = 0.05
    tau, ka = 12.0, 1.2
    k1 = np.log(2) / 12
    k2 = k1 / 2.2
    t_inh = 48.0
    ts = np.arange(-240, 216, dt)
    agut, c = 0.0, 0.0
    out = []
    for ti in ts:
        if abs((ti % tau)) < dt / 2:
            agut += 1.0
        k = k2 if ti >= t_inh else k1
        agut, c = agut - ka * agut * dt, c + (ka * agut - k * c) * dt
        out.append(c)
    out = np.array(out)
    m = ts >= 0
    tt, cc = ts[m] / 24, out[m]
    cmax = cc.max()
    cc = cc / cc[tt < 2].max()
    a.plot(tt, cc, color=TEAL, lw=1.3)
    a.axvline(t_inh / 24, color=RUST, lw=0.8, ls=(0, (2, 2)))
    ymax = cc.max()
    a.text(t_inh / 24 + 0.08, ymax * 1.08, 'inhibitor started', fontsize=7, color=RUST, ha='left', va='top')
    # troughs and a peak before the inhibitor
    trough_t = [36 - dt]
    for tq in [36.0 - dt]:
        i = np.argmin(abs(tt * 24 - tq)); a.plot(tt[i], cc[i], 'o', color=TEAL, ms=4.5, zorder=3)
        a.annotate('trough', (tt[i], cc[i]), xytext=(tt[i] - 0.55, cc[i] - 0.38), fontsize=7, color=TEAL,
                   arrowprops=dict(arrowstyle='-', color=TEAL, lw=0.6))
    i = np.argmax(np.where((tt * 24 > 24) & (tt * 24 < 36), cc, 0)); a.plot(tt[i], cc[i], 'o', color=TEAL, ms=4.5, zorder=3)
    a.annotate('peak', (tt[i], cc[i]), xytext=(tt[i] - 0.75, cc[i] + 0.3), fontsize=7, color=TEAL, ha='center',
               arrowprops=dict(arrowstyle='-', color=TEAL, lw=0.6))
    # early sample after the inhibitor, and a later steady-state sample
    for tq, lab, col, dy in [(72.0 - dt, 'early level:\nunderestimates', RUST, 0.55), (204.0 - dt, 'new steady\nstate', TEAL, 0.5)]:
        i = np.argmin(abs(tt * 24 - tq)); a.plot(tt[i], cc[i], 'o', color=col, ms=4.5, zorder=3)
        a.annotate(lab, (tt[i], cc[i]), xytext=(tt[i] + 0.25, cc[i] - dy), fontsize=7, color=col, va='top',
                   arrowprops=dict(arrowstyle='-', color=col, lw=0.6))
    # 4-5 half-lives bracket
    y = ymax * 1.25
    a.annotate('', xy=(t_inh / 24, y), xytext=(t_inh / 24 + 4.5 * 12 * 2.2 / 24, y),
               arrowprops=dict(arrowstyle='<->', color=GREY, lw=0.8))
    a.text(t_inh / 24 + 2.25 * 12 * 2.2 / 24, y + 0.08, 'about 4 to 5 new half-lives to settle', fontsize=7,
           color=GREY, ha='center', va='bottom', style='italic')
    a.set_xlim(0, 9); a.set_ylim(0, ymax * 1.42)
    _blank(a)
    a.set_xlabel('Time (days)'); a.set_ylabel('Relative concentration')
    fig.tight_layout()
    save(fig, 'fig12_2')


def fig12_3():
    """Hunter decision rules and their performance against Sternbach's criteria (ref [10])."""
    H = 2.75
    fig, ax = diagram(H)
    box(ax, 0.1, 2.2, 3.05, 0.45, 'Serotonergic agent taken, plus any one of:', style='teal', size=8)
    rules = ['Spontaneous clonus', 'Inducible or ocular clonus with agitation or diaphoresis',
             'Tremor with hyperreflexia', 'Hypertonia, temperature above 38 °C, and ocular or inducible clonus']
    rh, g = 0.42, 0.07
    for k, r in enumerate(rules):
        y = 2.2 - 0.12 - (k + 1) * rh - k * g
        box(ax, 0.35, y, 2.8, rh, r, style='light', size=7.5, align='left', wrapw=52)
        ax.plot([0.22, 0.22, 0.35], [2.2, y + rh / 2, y + rh / 2], color=GREY, lw=0.9, zorder=1)
    text(ax, 0.1, 0.08, 'Clonus and lower-limb hyperreflexia are the most discriminating findings.',
         size=6.8, color=GREY, italic=True, ha='left')
    # performance chart
    b = fig.add_axes([3.75 / TEXT_W, 0.62 / H, 1.45 / TEXT_W, 1.85 / H])
    b.spines[['top', 'right']].set_visible(False); b.tick_params(length=3, width=0.6)
    x = np.arange(2)
    hv, sv = [84, 97], [75, 96]
    b.bar(x - 0.19, hv, 0.36, color=TEAL)
    b.bar(x + 0.19, sv, 0.36, color=RULE)
    for xi, v in zip(x - 0.19, hv):
        b.text(xi, v + 1.5, f'{v}%', ha='center', fontsize=7, color=TEAL, fontweight='bold')
    for xi, v in zip(x + 0.19, sv):
        b.text(xi, v + 1.5, f'{v}%', ha='center', fontsize=7, color=GREY)
    b.set_xticks(x, ['Sensitivity', 'Specificity'], fontsize=7.5)
    b.set_ylim(0, 122); b.set_yticks([0, 50, 100]); b.tick_params(axis='y', labelsize=7)
    b.text(0.3, 114, 'Sternbach', fontsize=6.8, color=GREY, ha='left')
    b.text(-0.4, 114, 'Hunter', fontsize=6.8, color=TEAL, ha='left', fontweight='bold')
    text(ax, 3.75 + 0.72, 0.2, 'Against a toxicologist\'s diagnosis;\noverdose populations', size=6.8, color=GREY, italic=True)
    save(fig, 'fig12_3')


def fig12_4():
    """Routes to serotonin excess with an SSRI plus tramadol or linezolid, and the PK twist (ref [5], [6])."""
    H = 3.55
    fig, ax = diagram(H)
    bh = 0.5
    rows = [2.95, 2.25, 1.55]
    drugs = ['SSRI', 'Linezolid', 'Tramadol']
    mechs = ['Blocks serotonin reuptake',
             'Weak, reversible MAO inhibition',
             'Blocks serotonin and norepinephrine\nreuptake (parent drug)']
    dx, dw = 0.1, 0.95
    mx, mw = 1.25, 1.85
    for y, d, m in zip(rows, drugs, mechs):
        box(ax, dx, y, dw, bh, d, style='teal', size=8.5)
        box(ax, mx, y, mw, bh, m, style='white', size=7.8, wrapw=40)
        arrow(ax, (dx + dw + 0.02, y + bh / 2), (mx - 0.02, y + bh / 2))
    # convergence on serotonin excess
    ex, ew, ey, eh = 3.45, 1.75, 2.48, 0.62
    box(ax, ex, ey, ew, eh, 'Excess serotonergic activity', style='accent', size=8.5)
    for y in rows:
        arrow(ax, (mx + mw + 0.02, y + bh / 2), (ex - 0.02, ey + eh / 2), color=RUST, lw=1.0)
    # clinical features
    fy, fh = 1.12, 1.12
    box(ax, ex, fy, ew, fh, 'Clonus and hyperreflexia, legs more than arms; tremor; agitation; '
        'diaphoresis; mydriasis; diarrhea. Hyperthermia and rigidity if severe.',
        style='rust', size=7.5, title='Serotonin toxicity', align='left', wrapw=33)
    arrow(ax, (ex + ew / 2, ey - 0.02), (ex + ew / 2, fy + fh + 0.02), color=RUST, lw=1.0)
    text(ax, ex + ew / 2, fy - 0.1, 'Onset usually rapid after an added drug or a dose increase',
         size=6.8, color=GREY, italic=True, wrapw=36, va='top')
    # PK twist with paroxetine
    px, py, pw, ph = 0.1, 0.1, 3.0, 1.08
    box(ax, px, py, pw, ph, '', style='sand')
    text(ax, px + 0.12, py + ph - 0.16, 'If the SSRI is paroxetine: CYP2D6 inhibition', size=8, bold=True,
         color=SAND_DARK, ha='left')
    steps = ['Parent tramadol\nAUC up about\na third', 'Active metabolite\nAUC down\n40% to 67%',
             'Less analgesia;\nPRN dose\nescalation']
    sw, sg = 0.86, 0.11
    for k, s in enumerate(steps):
        x = px + 0.12 + k * (sw + sg)
        box(ax, x, py + 0.1, sw, 0.62, s, style='white', size=7, wrapw=40)
        if k:
            arrow(ax, (x - sg + 0.01, py + 0.41), (x - 0.01, py + 0.41), color=GREY)
    # feedback: escalation means more serotonergic parent drug
    xr = px + 0.12 + 2 * (sw + sg) + sw / 2
    ax.plot([xr, xr], [py + 0.72, py + ph], color=RUST, lw=1.0, ls=(0, (3, 2)), zorder=3)
    arrow(ax, (xr, py + ph), (xr, rows[2] - 0.02), color=RUST, lw=1.0, ls=(0, (3, 2)))
    text(ax, xr - 0.08, (py + ph + rows[2]) / 2, 'more parent drug', size=6.8, color=RUST, italic=True, ha='right')
    save(fig, 'fig12_4')


def fig12_5():
    """Timeline of Worked Case 12.1 (fictional)."""
    H = 3.45
    fig, ax = diagram(H)
    x0, dx = 1.12, 0.505  # day d starts at x0 + d*dx; days 0..7
    def X(d):
        return x0 + d * dx
    ytop, ybot = 3.08, 0.42
    for d in range(8):
        if d % 2 == 0:
            ax.add_patch(Rectangle((X(d), ybot), dx, ytop - ybot, fc=TEAL_LIGHT, ec='none', alpha=0.7, zorder=0))
        text(ax, X(d) + dx / 2, ytop + 0.14, f'Day {d}', size=7.5, color=GREY)
    rows = {'Paroxetine': 2.72, 'Tramadol': 2.3, 'Ondansetron': 1.9, 'Haloperidol': 1.52,
            'Clinical course': 1.06, 'CK (U/L)': 0.6}
    for lab, y in rows.items():
        text(ax, 0.1, y, lab, size=8, ha='left', bold=lab in ('Tramadol', 'Paroxetine'))
    bar = 0.2
    def seg(d0, d1, y, color):
        ax.add_patch(Rectangle((X(d0), y - bar / 2), X(d1) - X(d0), bar, fc=color, ec='none', zorder=2))
    # paroxetine: long-term, omitted days 0-1, resumed morning day 2, held day 3, restarted at discharge
    y = rows['Paroxetine']
    ax.plot([X(0.05), X(2.3)], [y, y], color=GREY, lw=1, ls=(0, (2, 2)), zorder=1)
    text(ax, X(1), y + 0.15, 'omitted', size=6.8, color=GREY, italic=True)
    seg(2.3, 3.2, y, TEAL)
    text(ax, X(3.25), y, 'held', size=6.8, color=GREY, italic=True, ha='left')
    text(ax, X(7.5), y, 'restarted', size=6.8, color=GREY, italic=True)
    # tramadol PRN from evening day 0; 3 doses day 1; 4 doses day 2; stopped morning day 3
    y = rows['Tramadol']
    seg(0.8, 3.3, y, TEAL)
    for d, n in [(0.97, '3 doses'), (1.87, '4 doses')]:
        text(ax, X(d + 0.5), y, n, size=7, color='white', bold=True)
    text(ax, X(3.35), y, 'stopped', size=6.8, color=GREY, italic=True, ha='left')
    # ondansetron days 0 and 1
    y = rows['Ondansetron']
    for d in (0.5, 1.5):
        ax.plot([X(d)], [y], marker='o', ms=4.5, color=GREY, zorder=3)
    # haloperidol once at 22:00 day 2
    y = rows['Haloperidol']
    th = 2 + 22 / 24
    ax.plot([X(th)], [y], marker='D', ms=5, color=RUST, zorder=3)
    text(ax, X(th) + 0.1, y, '22:00, four hours after onset', size=6.8, color=RUST, italic=True, ha='left')
    # clinical course: onset day 2 18:00 to clonus resolved evening day 4
    y = rows['Clinical course']
    t_on, t_res = 2 + 18 / 24, 4 + 20 / 24
    seg(t_on, t_res, y, RUST)
    ax.plot([X(t_on), X(t_on)], [ybot, ytop], color=RUST, lw=0.8, ls=(0, (2, 2)), zorder=1)
    text(ax, X(t_on) - 0.06, y + 0.2, 'onset 18:00: agitation,\ntremor, sweating', size=6.8, color=RUST, ha='right')
    text(ax, X(t_on) + 0.06, y - 0.2, 'day 3, 02:00: 38.6 °C, clonus', size=6.8, color=RUST, ha='left')
    text(ax, X(t_res) + 0.06, y + 0.02, 'clonus\nresolved', size=6.8, color=GREY, ha='left', italic=True)
    text(ax, X(7.5), y, 'discharged', size=6.8, color=GREY, italic=True)
    # CK values days 1, 3, 5
    y = rows['CK (U/L)']
    for d, v in [(1, '610'), (3, '1,450'), (5, '520')]:
        text(ax, X(d + 0.5), y, v, size=7.5, bold=True, color=INK)
    text(ax, X(4), 0.25, 'Paroxetine: long-term 20 mg daily. Tramadol: 100 mg as needed, up to four times daily.',
         size=6.8, color=GREY, italic=True)
    save(fig, 'fig12_5')


if __name__ == '__main__':
    fig12_1(); fig12_2(); fig12_3(); fig12_4(); fig12_5()
