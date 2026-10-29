# Figures for Chapter 5.
import numpy as np
from figlib import *


def _course(t, on, off, k_on, k_off, level):
    """First-order approach to `level` after `on`, first-order return to 1 after `off`."""
    y = np.ones_like(t)
    a = (t >= on) & (t < off)
    y[a] = 1 + (level - 1) * (1 - np.exp(-(t[a] - on) / k_on))
    y_off = 1 + (level - 1) * (1 - np.exp(-(off - on) / k_on))
    b = t >= off
    y[b] = 1 + (y_off - 1) * np.exp(-(t[b] - off) / k_off)
    return y


def fig05_1():
    """Schematic onset and offset of reversible inhibition, time-dependent inhibition, and induction."""
    fig, axes = chart(3.6, nrows=3, sharex=True)
    t = np.linspace(0, 20, 800)
    on, off = 3, 10
    panels = [
        ('Reversible inhibition', _course(t, on, off, 0.25, 0.45, 2.2),
         [(3.4, 1.55, 'starts within one or two doses', 'left'), (11.0, 1.9, 'ends as the inhibitor is cleared', 'left')]),
        ('Time-dependent inhibition', _course(t, on, off, 1.6, 2.6, 2.2),
         [(4.9, 1.45, 'onset delayed', 'left'), (13.0, 1.75, 'outlasts the inhibitor: offset\nneeds new enzyme', 'left')]),
        ('Induction', _course(t, on, off, 1.4, 3.6, 0.4),
         [(4.6, 1.22, 'needs new protein: full effect\nin about a week (rifampin)', 'left'),
          (13.4, 0.42, 'de-induction over about two\nweeks after the inducer stops', 'left')]),
    ]
    for ax, (name, y, notes) in zip(axes, panels):
        ax.axvspan(on, off, color=SAND, zorder=0, lw=0)
        ax.axhline(1, color=GREY, lw=0.7, ls=(0, (1, 2)), zorder=1)
        col = RUST if name == 'Induction' else TEAL
        ax.plot(t, y, color=col, lw=1.8, zorder=3)
        ax.text(0.2, 2.65 if name != 'Induction' else 1.55, name, fontsize=8.5, fontweight='bold', color=col,
                va='top', ha='left')
        for x, yy, s, ha in notes:
            ax.text(x, yy, s, fontsize=7, color=INK, va='center', ha=ha, linespacing=1.1, style='italic')
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        if name == 'Induction':
            ax.set_ylim(0.15, 1.6)
        else:
            ax.set_ylim(0.6, 2.75)
    axes[0].text((on + off) / 2, 0.66, 'perpetrator taken', ha='center', va='bottom', fontsize=7, color=SAND_DARK)
    axes[-1].set_xticks([on, off], ['perpetrator\nstarted', 'perpetrator\nstopped'], fontsize=7.5)
    axes[-1].set_xlim(0, 20)
    axes[-1].set_xlabel('Time (schematic)', fontsize=8)
    fig.text(0.012, 0.55, 'Object-drug exposure (relative to baseline, dotted)', rotation=90, va='center',
             ha='left', fontsize=8)
    fig.tight_layout(h_pad=0.4)
    fig.subplots_adjust(left=0.06)
    save(fig, 'fig05_1')


def fig05_3():
    """Static model: AUC ratio against fm for several degrees of pathway inhibition."""
    fig, ax = chart(3.0)
    fm = np.linspace(0, 0.97, 400)
    cases = [(None, 'complete blockade', RUST), (9, '[I]/Ki = 9 (90% blocked)', TEAL),
             (3, '[I]/Ki = 3 (75% blocked)', TEAL_MID), (1, '[I]/Ki = 1 (50% blocked)', SAND_DARK)]
    for r, lab, col in cases:
        aucr = 1 / (1 - fm) if r is None else 1 / (fm / (1 + r) + (1 - fm))
        ax.plot(fm, aucr, color=col, lw=1.8, zorder=3)
    # direct labels
    ax.text(0.80, 6.6, 'complete\nblockade', color=RUST, fontsize=7.5, ha='right', va='center', linespacing=1.1)
    ax.text(0.985, 1 / (0.97 / 10 + 0.03) * 0.97, '[I]/Ki = 9\n(90% blocked)', color=TEAL, fontsize=7.5,
            ha='left', va='center', linespacing=1.1)
    ax.text(0.985, 1 / (0.97 / 4 + 0.03), '[I]/Ki = 3\n(75%)', color=TEAL_MID, fontsize=7.5, ha='left',
            va='center', linespacing=1.1)
    ax.text(0.985, 1 / (0.97 / 2 + 0.03), '[I]/Ki = 1\n(50%)', color=SAND_DARK, fontsize=7.5, ha='left',
            va='center', linespacing=1.1)
    # M12 boundaries (index-substrate definitions)
    for v, s_ in ((1.25, 'weak'), (2, 'moderate'), (5, 'strong')):
        ax.axhline(v, color=GREY, lw=0.6, ls=(0, (1, 2)), zorder=1, xmax=0.97)
    ax.text(0.01, 5 * 1.03, '5-fold: strong', fontsize=7, color=GREY, va='bottom')
    ax.text(0.01, 2 * 1.03, '2-fold: moderate', fontsize=7, color=GREY, va='bottom')
    ax.text(0.95, 1.25 / 1.03, '1.25-fold: weak', fontsize=7, color=GREY, va='top', ha='right')
    # points from Calculation 5.1
    for x, y in ((0.9, 10), (0.5, 2), (0.2, 1.25), (0.9, 1.82)):
        ax.plot(x, y, 'o', ms=4.5, color=INK, zorder=4)
    ax.text(0.88, 10, 'fm 0.90, complete: 10', fontsize=7, ha='right', va='center', color=INK)
    ax.text(0.48, 2.1, 'fm 0.50: 2.0', fontsize=7, ha='right', va='bottom', color=INK)
    ax.text(0.18, 1.36, 'fm 0.20: 1.25', fontsize=7, ha='right', va='bottom', color=INK)
    ax.annotate('fm 0.90,\n[I]/Ki = 1: 1.8', (0.9, 1.82), xytext=(1.0, 1.42), fontsize=7, ha='left', va='center',
                color=INK, annotation_clip=False, linespacing=1.1,
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.6, shrinkA=1, shrinkB=3))
    ax.set_yscale('log')
    ax.set_ylim(0.95, 13); ax.set_xlim(0, 1.0)
    ax.set_yticks([1, 1.25, 2, 5, 10], ['1', '1.25', '2', '5', '10'])
    ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.spines['bottom'].set_bounds(0, 1.0)
    ax.set_xlabel('fm: fraction of object-drug clearance through the inhibited pathway', fontsize=8.5)
    ax.set_ylabel('Predicted AUC ratio (model)', fontsize=8.5)
    fig.tight_layout()
    fig.subplots_adjust(right=0.86)
    save(fig, 'fig05_3')


def fig05_2():
    """Which species carries the activity decides the direction of the consequence."""
    fig, ax = diagram(2.75)
    rows = [(1.55, 'Activity in the parent drug', True,
             ('Active exposure rises: toxicity', 'Active exposure falls: therapeutic failure')),
            (0.15, 'Activity in a metabolite (prodrug)', False,
             ('Active exposure falls: therapeutic failure', 'Active exposure rises: more effect, or toxicity if the metabolite is toxic'))]
    for y, title, parent_active, (inh, ind) in rows:
        text(ax, 0.08, y + 1.0, title, size=8.5, bold=True, color=TEAL, ha='left')
        h = 0.5
        box(ax, 0.08, y + 0.2, 0.75, h, 'Parent' if parent_active else 'Parent\n(prodrug)',
            style='teal' if parent_active else 'grey', size=8)
        box(ax, 1.13, y + 0.2, 0.7, h, 'Enzyme', style='white', size=8)
        text(ax, 1.48, y + 0.08, 'inhibited or induced', size=6.5, color=GREY, italic=True)
        box(ax, 2.13, y + 0.2, 0.9, h, 'Metabolite\n(inactive)' if parent_active else 'Active\nmetabolite',
            style='grey' if parent_active else 'teal', size=8)
        arrow(ax, (0.85, y + 0.45), (1.11, y + 0.45), color=GREY)
        arrow(ax, (1.85, y + 0.45), (2.11, y + 0.45), color=GREY)
        bw = 1.66
        box(ax, 3.56, y + 0.5, bw, 0.42, inh, style='rust' if 'toxicity' in inh else 'sand', size=7, align='left',
            wrapw=40)
        box(ax, 3.56, y + 0.02, bw, 0.42, ind, style='rust' if 'toxicity' in ind else 'sand', size=7, align='left',
            wrapw=40)
        text(ax, 3.48, y + 0.71, 'Inhibitor', size=7, color=GREY, ha='right', italic=True)
        text(ax, 3.48, y + 0.23, 'Inducer', size=7, color=GREY, ha='right', italic=True)
    ax.plot([0.08, TEXT_W - 0.08], [1.43, 1.43], color=RULE, lw=0.6)
    save(fig, 'fig05_2')


def fig05_4():
    """Calculation 5.2: recovery of excess enzyme activity after an inducer stops (8-day half-life)."""
    fig, ax = chart(2.5)
    t = np.linspace(0, 35, 400)
    excess = 100 * 0.5 ** (t / 8)
    ax.axvspan(14, 28, color=RUST_LIGHT, lw=0, zorder=0)
    ax.text(21, 92, 'two to four weeks: exposure climbs and peaks\nif the dose was raised during induction',
            ha='center', va='top', fontsize=7, color=RUST, linespacing=1.1)
    ax.plot(t, excess, color=TEAL, lw=1.9, zorder=3)
    for d, v, lab in ((8, 50, 'day 8: half gone'), (16, 25, 'day 16: three-quarters gone'),
                      (27, 100 * 0.5 ** (27 / 8), 'day 27: about 90% gone')):
        ax.plot(d, v, 'o', ms=5, color=INK, zorder=4)
        ax.text(d + 0.8, v + 3, lab, ha='left', va='bottom', fontsize=7.5, color=INK)
    ax.set_xlim(0, 35); ax.set_ylim(0, 105)
    ax.set_xticks([0, 7, 14, 21, 28, 35])
    ax.set_yticks([0, 25, 50, 75, 100], ['0%', '25%', '50%', '75%', '100%'])
    ax.set_xlabel('Days after the inducer stops', fontsize=8.5)
    ax.set_ylabel('Excess enzyme activity\nremaining (model)', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig05_4')


def fig05_5():
    """Rifampin with apixaban and rivaroxaban: AUC falls more than peak concentration."""
    fig, ax = chart(2.45)
    rows = [('Apixaban, observed,\noral dose', 3), ('Apixaban, observed,\nintravenous dose', 2),
            ('Apixaban, PBPK\nmodel', 1), ('Rivaroxaban, PBPK\nmodel', 0)]
    ax.axvline(1, color=GREY, lw=0.8, ls=(0, (1, 2)))
    ax.text(0.985, 3.55, 'no change', ha='right', va='center', fontsize=7, color=GREY)

    def auc(y, lo, hi=None, lab=''):
        if hi:
            ax.plot([lo, hi], [y, y], color=RUST, lw=5, solid_capstyle='round', zorder=3)
        else:
            ax.plot(lo, y, 'o', ms=7, color=RUST, zorder=3)
        ax.text(lo - 0.02, y + 0.2, lab, ha='center', va='bottom', fontsize=7.5, color=RUST)

    def cmax(y, lo, hi=None, lab=''):
        if hi:
            ax.plot([lo, hi], [y, y], color=TEAL, lw=5, solid_capstyle='round', zorder=3)
            ax.plot([lo, hi], [y, y], color='white', lw=2.6, solid_capstyle='round', zorder=3)
        else:
            ax.plot(lo, y, 'o', ms=7, mfc='white', mec=TEAL, mew=1.6, zorder=3)
        ax.text((lo + (hi or lo)) / 2 + 0.02, y + 0.2, lab, ha='center', va='bottom', fontsize=7.5, color=TEAL)

    auc(3, 0.46, lab='AUC −54%')
    auc(2, 0.61, lab='AUC −39%')
    auc(1, 0.43, lab='AUC 0.43')
    cmax(1, 0.48, lab='     peak 0.48')
    auc(0, 0.50, 0.52, lab='AUC 0.50–0.52')
    cmax(0, 0.72, 0.73, lab='peak 0.72–0.73')
    ax.set_yticks([r[1] for r in rows], [r[0] for r in rows], fontsize=7.5)
    ax.set_xlim(0.3, 1.05); ax.set_ylim(-0.45, 3.8)
    ax.set_xticks([0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel('Ratio with rifampin to without (filled: AUC; open: peak concentration)', fontsize=8)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    save(fig, 'fig05_5')


def fig05_6():
    """Worked Case 5.1: chronology against the induction onset window."""
    fig, ax = chart(2.4)
    from matplotlib.patches import Rectangle
    # bars
    ax.add_patch(Rectangle((-6, 2.75), 34, 0.4, fc=TEAL_LIGHT, ec=TEAL_MID, lw=0.8))
    ax.text(-5.5, 2.95, 'apixaban 5 mg twice daily, dose unchanged', ha='left', va='center', fontsize=7.5, color=TEAL)
    ax.add_patch(Rectangle((1, 2.05), 27, 0.4, fc=RUST_LIGHT, ec=RUST, lw=0.8))
    ax.text(1.5, 2.25, 'rifampin 600 mg daily (with isoniazid, pyrazinamide, ethambutol)', ha='left',
            va='center', fontsize=7.5, color=RUST)
    # induction schematic
    t = np.linspace(1, 28, 300)
    ind = 1 - np.exp(-(t - 1) / 2.3)
    ax.fill_between(t, 0.3, 0.3 + 1.2 * ind, color=SAND, lw=0)
    ax.plot(t, 0.3 + 1.2 * ind, color=SAND_DARK, lw=1.4)
    ax.text(8.5, 0.85, 'induction (schematic): essentially\ncomplete within about a week', ha='center', linespacing=1.1,
            va='center', fontsize=7, color=SAND_DARK, style='italic')
    # window
    ax.annotate('', xy=(28, 1.72), xytext=(8, 1.72),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=0.9))
    ax.text(8, 1.82, 'onset window opens about a week after the start and stays open', ha='left', va='bottom',
            fontsize=7, color=GREY)
    # events
    ax.axvline(25, color=RUST, lw=1.2, ymin=0.05, ymax=0.48)
    ax.text(24.6, 0.42, 'day 25: ischemic stroke;\nanti-Xa 24 ng/mL, well\nbelow the quoted range',
            ha='right', va='bottom', fontsize=7, color=RUST, fontweight='bold', linespacing=1.1)
    ax.plot(2, 0.15, 'x', ms=6, color=GREY, mew=1.2)
    ax.text(2.7, 0.15, 'a stroke on day 2 would not fit', ha='left', va='center', fontsize=6.5, color=GREY,
            style='italic')
    ax.set_xlim(-6, 30); ax.set_ylim(-0.1, 3.35)
    ax.set_xticks([1, 8, 15, 22, 25], ['4 Sep\nday 1', 'day 8', 'day 15', 'day 22', '28 Sep\nday 25'], fontsize=7)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    fig.tight_layout()
    save(fig, 'fig05_6')


if __name__ == '__main__':
    fig05_1(); fig05_2(); fig05_3(); fig05_4(); fig05_5(); fig05_6()
