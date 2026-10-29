# Figures for Chapter 8.
import numpy as np
from figlib import *


def _course(t, t_on, t_off, k_on, k_off):
    """First-order rise after t_on and first-order fall after t_off (relative units)."""
    y = np.zeros_like(t)
    on = (t >= t_on) & (t < t_off)
    y[on] = 1 - np.exp(-k_on * (t[on] - t_on))
    y_off = 1 - np.exp(-k_on * (t_off - t_on))
    after = t >= t_off
    y[after] = y_off * np.exp(-k_off * (t[after] - t_off))
    return y


def fig08_2():
    """Onset and offset clocks for reversible inhibition, induction and time-dependent inhibition. Schematic."""
    fig, axes = chart(3.15, nrows=3, sharex=True, gridspec_kw={'hspace': 0.28})
    fig.subplots_adjust(left=0.28, right=0.97, top=0.9, bottom=0.1)
    t = np.linspace(0, 10, 600)
    t_on, t_off = 1.0, 5.0
    rows = [
        ('Reversible inhibition', 'tracks the inhibitor', 'falls as the inhibitor\nis eliminated', 3.0, 3.0, TEAL),
        ('Induction', 'days to weeks:\nnew enzyme is made', 'wanes at the rate\nof enzyme turnover', 0.7, 0.7, SAND_DARK),
        ('Time-dependent\ninhibition', 'enzyme inactivated', 'outlasts the inhibitor:\nnew enzyme needed', 2.0, 0.55, RUST),
    ]
    for a, (lab, on_txt, off_txt, kon, koff, c) in zip(axes, rows):
        a.axvspan(t_on, t_off, color=TEAL_LIGHT, lw=0, zorder=0)
        y = _course(t, t_on, t_off, kon, koff)
        a.plot(t, y, color=c, lw=1.8)
        a.set_ylim(-0.05, 1.3)
        a.set_yticks([])
        a.set_xlim(0, 10)
        a.spines['left'].set_color(RULE)
        a.text(-0.035, 0.5, lab, transform=a.transAxes, ha='right', va='center', fontsize=8.5,
               fontweight='bold', color=TEAL)
        a.text(t_on + 0.1, 1.22, on_txt, fontsize=6.8, color=GREY, va='top', style='italic')
        a.text(t_off + 0.25, 1.22, off_txt, fontsize=6.8, color=GREY, va='top', style='italic')
    axes[0].text((t_on + t_off) / 2, 1.42, 'precipitant given', fontsize=7.5, color=TEAL, ha='center', va='bottom')
    axes[0].text(t_off, 1.42, 'stopped', fontsize=7.5, color=GREY, ha='center', va='bottom')
    axes[0].text(t_on, 1.42, 'started', fontsize=7.5, color=GREY, ha='center', va='bottom')
    axes[-1].set_xticks([])
    axes[-1].set_xlabel('Time', fontsize=8)
    fig.text(0.04, 0.5, 'Size of effect on\nthe object drug\'s\npathway (relative)', rotation=90, ha='center',
             va='center', fontsize=7.5, color=INK)
    save(fig, 'fig08_2')


def fig08_3():
    """Calculation 8.2 as a curve: inhibitor remaining versus pathway activity after stopping. Model prediction."""
    fig, ax = chart(2.75)
    fig.subplots_adjust(left=0.12, right=0.78, top=0.95, bottom=0.17)
    t = np.linspace(0, 150, 400)
    conc = 0.5 ** (t / 50)
    act = 1 / (1 + 4 * conc)
    act100 = 1 / (1 + 4 * 0.5 ** (t / 100))
    ax.plot(t, conc * 100, color=GREY, lw=1.6)
    ax.plot(t, act * 100, color=TEAL, lw=2.0)
    ax.plot(t, act100 * 100, color=TEAL_MID, lw=1.4, ls=(0, (4, 2)))
    ax.set_xlim(0, 150); ax.set_ylim(0, 105)
    ax.set_xticks([0, 14, 28, 60, 100, 150])
    ax.set_xlabel('Days after stopping the inhibitor')
    ax.set_ylabel('Percent')
    # labelled points from the calculation
    for x, v in [(28, 68), (100, 25)]:
        ax.plot(x, v, 'o', color=GREY, ms=4)
    for x, v in [(0, 20), (28, 27), (100, 50)]:
        ax.plot(x, v, 'o', color=TEAL, ms=4)
    ax.text(31, 70, '68%', fontsize=7.5, color=GREY, va='bottom')
    ax.text(102, 22, '25%', fontsize=7.5, color=GREY, va='top')
    ax.text(3, 18, '20%', fontsize=7.5, color=TEAL, va='top')
    ax.text(26, 29, '27%', fontsize=7.5, color=TEAL, va='bottom', ha='right')
    ax.text(100, 53, '50%', fontsize=7.5, color=TEAL, va='bottom', ha='right')
    # direct labels at right edge
    ax.text(152, conc[-1] * 100, 'Inhibitor remaining\n(% of level at stopping)', fontsize=7.5, color=GREY,
            va='center', clip_on=False)
    ax.text(152, act[-1] * 100 + 2, 'Pathway activity\n(% of normal),\ninhibitor half-life\n50 days', fontsize=7.5, color=TEAL,
            va='center', clip_on=False)
    ax.text(152, act100[-1] * 100 - 11, 'Pathway activity,\ninhibitor half-life\n100 days', fontsize=7.5, color=TEAL_MID,
            va='center', clip_on=False)
    ax.axvline(14, color=RUST, lw=0.9, ls=(0, (3, 2)), zorder=0)
    ax.text(15.5, 101, 'Worked Case 8.1:\nwarfarin dose restored', fontsize=6.8, color=RUST, va='top')
    save(fig, 'fig08_3')


def fig08_5():
    """Worked Case 8.1: amiodarone, warfarin dose and INR over 330 days (fictional)."""
    fig = plt.figure(figsize=(TEXT_W, 3.75))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.55, 1.0, 1.35], hspace=0.22,
                          left=0.15, right=0.97, top=0.9, bottom=0.11)
    axa, axw, axi = (fig.add_subplot(gs[i]) for i in range(3))
    xl = (-30, 340)
    for a in (axa, axw, axi):
        a.set_xlim(*xl)
        a.spines[['top', 'right']].set_visible(False)
        a.tick_params(length=3, width=0.6)
        for x0 in (0, 150):
            a.axvline(x0, color=GREY, lw=0.8, ls=(0, (3, 2)), zorder=0)
    axa.text(0, 1.08, 'time zero: onset', fontsize=7, color=GREY, ha='center', va='bottom',
             transform=axa.get_xaxis_transform())
    axa.text(150, 1.08, 'time zero: offset', fontsize=7, color=GREY, ha='center', va='bottom',
             transform=axa.get_xaxis_transform())
    # amiodarone track
    axa.axis('off')
    axa.set_ylim(0, 1)
    axa.barh(0.5, 14, left=0, height=0.55, color=TEAL, lw=0)
    axa.barh(0.5, 136, left=14, height=0.55, color=TEAL_MID, lw=0)
    # fading bar: residual inhibition, schematic
    from matplotlib.colors import LinearSegmentedColormap
    fade = LinearSegmentedColormap.from_list('fade', [TEAL_MID, 'white'])
    grad = np.linspace(0, 1, 256)[None, :] ** 0.6
    axa.imshow(grad, extent=[150, 330, 0.225, 0.775], aspect='auto', cmap=fade, vmin=0, vmax=1, zorder=1)
    axa.set_xlim(*xl); axa.set_ylim(0, 1)
    axa.text(-33, 0.5, 'Amiodarone', ha='right', va='center', fontsize=8)
    axa.text(80, 0.5, '200 mg daily', ha='center', va='center', fontsize=7, color='white')
    axa.text(225, 0.5, 'stopped; residual inhibition (schematic)', ha='center', va='center', fontsize=7,
             color=TEAL, style='italic')
    # warfarin dose
    xs = [-30, 38, 38, 41, 41, 164, 164, 178, 178]
    ys = [5, 5, 0, 0, 3, 3, 5, 5, 3]
    axw.plot(xs, ys, color=SAND_DARK, lw=1.6)
    axw.plot([178, 290, 330], [3, 4.5, 5], color=SAND_DARK, lw=1.4, ls=(0, (3, 2)))
    axw.set_ylim(-0.5, 6.4)
    axw.set_yticks([0, 3, 5])
    axw.set_ylabel('Warfarin\n(mg/day)', fontsize=8)
    axw.set_xticks([0, 38, 150, 178, 330])
    axw.tick_params(labelbottom=False)
    axw.text(182, 5.25, 'restored to 5 mg on day 164', fontsize=7, color=RUST, ha='left', va='bottom')
    axw.text(250, 3.0, 'raised in steps', fontsize=6.8, color=GREY, style='italic', ha='left', va='top')
    axw.text(46, 0.35, 'withheld', fontsize=6.8, color=GREY, style='italic', ha='left', va='bottom')
    # INR
    axi.axhspan(2.0, 3.0, color=TEAL_LIGHT, lw=0, zorder=0)
    for a0, a1, lo, hi in [(-30, -2, 2.2, 2.8), (41, 148, 2.1, 2.7), (190, 330, 2.0, 3.0)]:
        axi.fill_between([a0, a1], lo, hi, color=TEAL_MID, alpha=0.55, lw=0)
    pts = [(7, 2.9, '2.9'), (38, 6.8, '6.8  hematuria'), (178, 5.1, '5.1  epistaxis')]
    for x, v, lab in pts:
        axi.plot(x, v, 'o', color=RUST if v > 4 else TEAL, ms=5, zorder=4)
        axi.text(x + 6, v, lab, fontsize=7.5, color=RUST if v > 4 else INK, va='center')
    axi.text(95, 3.15, 'INR 2.1 to 2.7', fontsize=6.8, color=TEAL, ha='center', va='bottom')
    axi.text(260, 3.15, 'INR 2.0 to 3.0', fontsize=6.8, color=TEAL, ha='center', va='bottom')
    axi.plot(28, 1.3, 'o', mfc='white', mec=GREY, ms=5, zorder=4)
    axi.text(34, 1.3, 'day 28: INR missed', fontsize=6.8, color=GREY, ha='left', va='center', style='italic')
    axi.set_ylim(0.8, 7.6)
    axi.set_yticks([2, 4, 6])
    axi.set_ylabel('INR', fontsize=8)
    axi.set_xticks([0, 38, 150, 178, 330])
    axi.set_xlabel('Day', fontsize=8)
    save(fig, 'fig08_5')


def fig08_1():
    """Calculation 8.1 as curves: approach to the new steady state with the old and the new half-life."""
    t = np.linspace(0, 330, 400)
    old, new = 1 - 0.5 ** (t / 40), 1 - 0.5 ** (t / 67)
    fig, ax = chart(2.6)
    fig.subplots_adjust(left=0.12, right=0.78, top=0.95, bottom=0.17)
    ax.plot(t, old * 100, color=GREY, lw=1.6, ls=(0, (4, 2)))
    ax.plot(t, new * 100, color=TEAL, lw=2.0)
    ax.axhline(94, color=RULE, lw=0.8, zorder=0)
    ax.text(3, 95.5, 'about 94% of the rise', fontsize=7, color=GREY, va='bottom')
    for x, c, lab in [(160, GREY, '160 h\n(under 7 days)'), (267, TEAL, '267 h\n(about 11 days)')]:
        ax.plot([x, x], [0, 94], color=c, lw=0.8, ls=(0, (2, 2)))
        ax.plot(x, 94, 'o', color=c, ms=4.5, zorder=3)
        ax.text(x + 4, 40, lab, fontsize=7, color=c, va='center')
    ax.text(334, 101.5, 'Old half-life\n40 h (wrong)', fontsize=7.5, color=GREY, va='bottom')
    ax.text(334, 94, 'New half-life\n67 h', fontsize=7.5, color=TEAL, va='top')
    ax.set_xlim(0, 330)
    ax.set_ylim(0, 116)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_xticks([0, 40, 67, 160, 267])
    ax.set_xlabel('Hours after the inhibitor is started')
    ax.set_ylabel('Rise completed (%)')
    save(fig, 'fig08_1')


def fig08_4():
    """Calculation 8.3 as bars: induced excess remaining after stopping, under two turnover estimates."""
    days = ['7 days', '14 days', '28 days']
    fast, slow = [0.19, 0.04, 0.005], [0.55, 0.30, 0.09]
    fast_lab = ['0.19', '0.04', 'under 0.01']
    fig, ax = chart(2.4)
    fig.subplots_adjust(left=0.13, right=0.97, top=0.95, bottom=0.2)
    x = np.arange(3)
    w = 0.34
    ax.bar(x - w / 2 - 0.02, fast, w, color=TEAL_MID)
    ax.bar(x + w / 2 + 0.02, slow, w, color=TEAL)
    for xi, v, lab in zip(x, fast, fast_lab):
        ax.text(xi - w / 2 - 0.02, v + 0.015, lab, ha='center', va='bottom', fontsize=7.5, color=INK)
    for xi, v in zip(x, slow):
        ax.text(xi + w / 2 + 0.02, v + 0.015, f'{v:.2f}', ha='center', va='bottom', fontsize=7.5, color=INK,
                fontweight='bold')
    ax.set_xticks(x, days)
    ax.set_xlabel('Time after the inducer is stopped', fontsize=8)
    ax.set_ylabel('Fraction of induced\nexcess remaining', fontsize=8)
    ax.set_ylim(0, 0.62)
    ax.set_yticks([0, 0.2, 0.4, 0.6])
    ax.text(-w / 2 - 0.02, 0.095, 'half-life' + chr(10) + '70 h [4]', ha='center', va='center', fontsize=6.8, color='white', fontweight='bold')
    ax.text(w / 2 + 0.02, 0.3, 'half-life' + chr(10) + '8 days [5]', ha='center', va='center', fontsize=6.8, color='white', fontweight='bold')
    save(fig, 'fig08_4')


if __name__ == '__main__':
    fig08_1(); fig08_2(); fig08_3(); fig08_4(); fig08_5()
