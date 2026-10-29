# Figures for Chapter 4.
from figlib import *
from matplotlib.patches import Rectangle


def fig04_1():
    """How long each class of acid-reducing agent raises gastric pH, and what that means for timing."""
    import numpy as np
    from matplotlib.colors import to_rgb
    fig, ax = chart(2.75)
    x0, x1 = -3.5, 14.5
    hh = 0.36

    def band(y, a, b, fade):
        prof = np.linspace(1, 0, 200) ** 1.4 if fade else np.ones(200)
        img = np.zeros((1, 200, 4)); img[..., :3] = to_rgb(TEAL_MID); img[..., 3] = 0.55 * prof
        ax.imshow(img, extent=[a, b, y - hh / 2, y + hh / 2], aspect='auto', zorder=1, interpolation='bilinear')

    band(2, 0, 2.2, True)
    band(1, 0, 12.5, True)
    band(0, x0, x1, False)
    for y in (0, 1, 2):
        ax.plot([0, 0], [y - hh / 2 - 0.04, y + hh / 2 + 0.04], color=TEAL, lw=1.6, zorder=3)

    def dose(x, y, reduced):
        ax.plot(x, y, 'o', ms=7, mfc=RUST if reduced else 'white', mec=RUST if reduced else TEAL,
                mew=1.3, zorder=4)

    def lab(x, y, s, reduced, ha='center'):
        ax.text(x, y, s, ha=ha, va='center', fontsize=7.5, color=RUST if reduced else TEAL,
                fontweight='bold' if reduced else 'normal', zorder=4)

    dose(0, 2, True); lab(-0.3, 2.36, 'taken together: −55 to 58%', True, ha='left')
    dose(2, 2, False); lab(2.45, 2, '2 h later: unchanged', False, ha='left')
    dose(-2, 1, False); lab(-2.3, 1.36, '2 h before: no effect', False, ha='left')
    dose(10, 1, True); lab(10, 1.36, '10 h later: about −60%', True)
    dose(1, 0, True); dose(12, 0, True)
    lab(6.5, 0.36, 'effect similar 1 h and 12 h later', True)
    ax.text(6.5, 0, 'acid suppressed for most of the day', ha='center', va='center', fontsize=7, color=TEAL,
            style='italic', zorder=4)
    for y, cls, obj in ((2, 'Antacid', 'dasatinib'), (1, 'H2-receptor antagonist', 'dasatinib'),
                        (0, 'Proton pump inhibitor', 'atazanavir with ritonavir')):
        ax.text(x0 - 0.3, y + 0.1, cls, ha='right', va='center', fontsize=8, color=INK, wrap=False)
        ax.text(x0 - 0.3, y - 0.17, obj, ha='right', va='center', fontsize=7, color=GREY, style='italic')
    ax.set_yticks([])
    ax.set_ylim(-0.35, 2.6); ax.set_xlim(x0, x1)
    ax.set_xticks(range(-2, 15, 2))
    ax.set_xlabel('Hours after the acid-reducing agent', fontsize=8.5)
    ax.spines['left'].set_visible(False)
    fig.tight_layout()
    fig.subplots_adjust(left=0.27)
    save(fig, 'fig04_1')


def fig04_2():
    """Ciprofloxacin relative bioavailability by antacid timing (Nix et al.)."""
    fig, ax = chart(2.6)
    pos = [-6, -4, -2, -0.15, 2]
    labs = ['6 h\nbefore', '4 h\nbefore', '2 h\nbefore', '5–10 min\nbefore', '2 h\nafter']
    vals = [None, 70, 23.2, 15.1, None]
    for p, v in zip(pos, vals):
        if v is None:
            ax.bar(p, 100, width=1.0, color='white', ec=TEAL, lw=0.9, ls=(0, (3, 2)), zorder=2)
            ax.text(p, 50, 'no\neffect', ha='center', va='center', fontsize=8, color=TEAL, linespacing=1.1)
        else:
            ax.bar(p, v, width=1.0, color=RUST if v < 50 else SAND_DARK, zorder=2)
            ax.text(p, v + 3, f'{v:g}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=INK)
    ax.axhline(100, color=GREY, lw=0.8, ls=(0, (1, 2)), zorder=1)
    ax.text(-7.0, 103, 'ciprofloxacin alone = 100%', ha='left', va='bottom', fontsize=7, color=GREY)
    ax.axvline(0.55, color=RULE, lw=0.8, zorder=1)
    ax.text(0.75, 110, 'ciprofloxacin first', ha='left', va='center', fontsize=7, color=TEAL, style='italic')
    ax.text(0.35, 110, 'antacid first', ha='right', va='center', fontsize=7, color=GREY, style='italic')
    ax.set_xticks(pos, labs, fontsize=7.5)
    ax.set_xlim(-7.1, 3.1); ax.set_ylim(0, 118)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel('Relative bioavailability (%)', fontsize=8.5)
    ax.set_xlabel('Time of antacid dose relative to ciprofloxacin', fontsize=8.5)
    fig.tight_layout()
    save(fig, 'fig04_2')


def fig04_3():
    """Calculation 4.1: AUC/MIC with and without iron at three MICs, against an illustrative target."""
    fig, ax = chart(2.6)
    mics = ['MIC 0.03 mg/L', 'MIC 0.125 mg/L', 'MIC 0.5 mg/L']
    no_fe = [967, 232, 58]
    fe = [360, 86, 22]
    xs = [0, 1, 2]
    ax.axhline(125, color=SAND_DARK, lw=0.9, ls=(0, (4, 2)), zorder=1)
    ax.text(2.42, 125 * 1.08, 'illustrative\ntarget 125', ha='left', va='bottom', fontsize=7, color=SAND_DARK,
            linespacing=1.1)
    for x, a, b in zip(xs, no_fe, fe):
        ax.plot([x, x], [b, a], color=RULE, lw=2.2, zorder=2)
        ax.plot(x, a, 'o', ms=8, color=TEAL, zorder=3)
        ax.plot(x, b, 'o', ms=8, color=RUST, zorder=3)
        ax.text(x + 0.1, a, f'{a}', ha='left', va='center', fontsize=8, color=TEAL, fontweight='bold')
        ax.text(x + 0.1, b, f'{b}', ha='left', va='center', fontsize=8, color=RUST, fontweight='bold')
    ax.text(-0.12, 967, 'without iron', ha='right', va='center', fontsize=7.5, color=TEAL)
    ax.text(-0.12, 360, 'with iron at\nevery dose', ha='right', va='center', fontsize=7.5, color=RUST,
            linespacing=1.1)
    ax.text(1, 52, 'interaction moves exposure\nacross the target', ha='center', va='center', fontsize=7,
            color=INK, style='italic', linespacing=1.1)
    ax.text(2, 11, 'below target\nbefore any interaction', ha='center', va='center', fontsize=7, color=INK,
            style='italic', linespacing=1.1)
    ax.set_yscale('log')
    ax.set_ylim(7, 1500); ax.set_xlim(-0.75, 2.8)
    ax.set_yticks([10, 30, 100, 300, 1000], ['10', '30', '100', '300', '1000'])
    ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xticks(xs, mics, fontsize=8)
    ax.set_ylabel('24-hour AUC/MIC (log scale)', fontsize=8.5)
    fig.tight_layout()
    save(fig, 'fig04_3')


def fig04_4():
    """Decision path for a suspected absorption interaction: coprescription is not coadministration."""
    fig, ax = diagram(3.2)
    qx, qw, qh = 0.08, 2.3, 0.5
    ox, ow = 2.95, 2.27
    qs = [(2.55, 'Is the mechanism brief and local (chelation, antacid)?', 'No (e.g., PPI): separation does not '
           'protect, so timing cannot exclude the interaction', 'sand'),
          (1.8, 'Are the actual clock times known?', 'No: ask for times, food, missed or vomited doses',
           'white'),
          (1.05, 'Were the products taken together or too close?', 'No: record a negative finding', 'grey')]
    for y, q, out, st in qs:
        box(ax, qx, y, qw, qh, q, style='light', size=7.5)
        box(ax, ox, y, ow, qh, out, style=st, size=7)
        arrow(ax, (qx + qw + 0.03, y + qh / 2), (ox - 0.03, y + qh / 2), color=GREY)
        text(ax, (qx + qw + ox) / 2, y + qh / 2 + 0.1, 'no', size=6.5, color=GREY, italic=True)
    for y in (2.55, 1.8, 1.05):
        arrow(ax, (qx + qw / 2, y - 0.02), (qx + qw / 2, y - 0.23), color=TEAL)
        text(ax, qx + qw / 2 + 0.1, y - 0.12, 'yes', size=6.5, color=TEAL, italic=True, ha='left')
    box(ax, qx, 0.3, qw, qh, 'Relate the expected loss to the exposure margin', style='teal', size=7.5)
    box(ax, ox, 0.3, ow, qh, 'Weigh competing explanations; write the statement', style='teal', size=7.5)
    arrow(ax, (qx + qw + 0.03, 0.3 + qh / 2), (ox - 0.03, 0.3 + qh / 2), color=TEAL)
    text(ax, TEXT_W / 2, 0.11, 'A prescription list shows coprescription; only clock times show coadministration.',
         size=7, color=GREY, italic=True)
    save(fig, 'fig04_4')


def fig04_5():
    """Worked Case 4.1: course and the daily schedule after discharge."""
    fig = plt.figure(figsize=(TEXT_W, 2.55))
    # top: course
    ax1 = fig.add_axes([0.03, 0.55, 0.94, 0.42]); ax1.axis('off')
    ax1.set_xlim(-0.9, 8.6); ax1.set_ylim(-0.75, 1.15)
    ax1.plot([0, 8], [0, 0], color=GREY, lw=1.0, zorder=0)
    ax1.add_patch(Rectangle((0, -0.17), 3, 0.34, fc=TEAL_LIGHT, ec=TEAL_MID, lw=0.8))
    ax1.add_patch(Rectangle((3, -0.17), 4, 0.34, fc=RUST_LIGHT, ec=RUST, lw=0.8))
    ax1.text(1.5, 0, 'IV ciprofloxacin', ha='center', va='center', fontsize=7.5, color=TEAL)
    ax1.text(5, 0, 'oral ciprofloxacin 500 mg twice daily', ha='center', va='center', fontsize=7.5, color=RUST)
    for x, lab in ((0, 'admitted;\nE. coli, MIC 0.125'), (1.5, 'afebrile\nafter 36 h'), (3, 'discharged\nday 3'),
                   (7, 'readmitted, day 4 after\ndischarge; MIC 0.125')):
        ax1.plot([x, x], [0.2, 0.42], color=GREY, lw=0.8)
        ax1.text(x, 0.48, lab, ha='center', va='bottom', fontsize=7, color=INK, linespacing=1.1)
    ax1.plot(7, 0, 'v', ms=8, color=RUST, zorder=4)
    ax1.text(4.0, -0.45, 'Schematic; not to scale', ha='center', va='center', fontsize=6.5, color=GREY,
             style='italic')
    # bottom: one day at home
    ax2 = fig.add_axes([0.03, 0.02, 0.94, 0.5]); ax2.axis('off')
    ax2.set_xlim(-1.6, 25); ax2.set_ylim(-1.2, 1.4)
    ax2.plot([0, 24], [0, 0], color=GREY, lw=1.0)
    for h in (0, 6, 12, 18, 24):
        ax2.plot([h, h], [-0.08, 0.08], color=GREY, lw=0.8)
        ax2.text(h, -0.25, f'{h:02d}:00', ha='center', va='top', fontsize=7, color=GREY)
    ax2.text(-1.5, 0.75, 'One day\nafter\ndischarge', ha='left', va='center', fontsize=7.5, color=INK,
             fontweight='bold', linespacing=1.1)
    for h, items in ((8, ['ciprofloxacin', 'calcium carbonate', 'ferrous sulfate']),
                     (18, ['ciprofloxacin', 'calcium carbonate'])):
        for k, it in enumerate(items):
            y = 0.35 + k * 0.38
            col = TEAL if it == 'ciprofloxacin' else RUST
            ax2.plot(h, y, 'o', ms=6, color=col, zorder=3)
            ax2.text(h + 0.5, y, it, ha='left', va='center', fontsize=7.5, color=col)
        ax2.plot([h, h], [0.05, 0.3], color=GREY, lw=0.8)
    ax2.text(12, -0.9, 'Every ciprofloxacin dose was taken with a cation, the morning dose with two '
             '(confirmed by the carer).', ha='center', va='center', fontsize=7, color=GREY, style='italic')
    save(fig, 'fig04_5')


if __name__ == '__main__':
    fig04_1(); fig04_2(); fig04_3(); fig04_4(); fig04_5()
