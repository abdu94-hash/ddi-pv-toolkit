# Figures for Chapter 19.
from figlib import *


def fig19_1():
    """Chain of inference for a pharmacokinetic interaction and the sources that address each link."""
    fig, ax = diagram(3.1)
    links = ['Precipitant affects a pathway that matters for the object drug',
             'Exposure to the object drug changes by a known amount',
             'Changed exposure changes an effect or marker',
             'Marker change raises the risk of a clinical event',
             'It happens in real patients, often enough to matter']
    sources = ['Mechanistic and in vitro data',
               'Dedicated DDI study; PBPK model for untested combinations',
               'Exposure–response, e.g. concentration–QTc',
               'Case reports and series: that harm occurs, and in what circumstances',
               'Observational studies: how often; trials and disproportionality only in part']
    n = 5
    bw, gap = 0.9, 0.135
    x0 = (TEXT_W - (n * bw + (n - 1) * gap)) / 2
    ly, lh = 1.82, 1.0
    sy, sh = 0.6, 0.9
    for k in range(n):
        x = x0 + k * (bw + gap)
        box(ax, x, ly, bw, lh, '', style='light')
        text(ax, x + bw / 2, ly + lh - 0.13, f'LINK {k + 1}', size=7, bold=True, color=TEAL)
        text(ax, x + bw / 2, ly + 0.4, links[k], size=7.5, wrapw=17)
        if k < n - 1:
            arrow(ax, (x + bw + 0.01, ly + lh / 2), (x + bw + gap - 0.01, ly + lh / 2))
        box(ax, x, sy, bw, sh, '', style='sand')
        text(ax, x + bw / 2, sy + sh / 2, sources[k], size=7, wrapw=18)
        ax.plot([x + bw / 2, x + bw / 2], [sy + sh + 0.02, ly - 0.02], color=SAND_DARK, lw=0.9,
                ls=(0, (2, 1.5)), zorder=1)
    text(ax, x0, ly + lh + 0.15, 'The argument', size=7.5, bold=True, color=TEAL, ha='left')
    text(ax, x0, sy - 0.15, 'Evidence that addresses each link', size=7.5, bold=True, color=SAND_DARK, ha='left')
    note(ax, 'The conclusion is only as strong as the weakest link that matters for the decision.', y=0.12, size=7.5)
    save(fig, 'fig19_1')


def fig19_4():
    """Crude exposure-QTc line from the two thorough QT means, with inhibitor scenarios (Calculation 19.2)."""
    fig, ax = chart(3.0)
    # E14 upper-bound threshold
    ax.axhline(10, color=GREY, lw=0.8, ls=(0, (4, 2)), zorder=1)
    ax.text(4.95, 9.6, 'ICH E14: concern if the upper\nbound reaches about 10 ms', ha='right', va='top',
            fontsize=7, color=GREY, style='italic')
    # strong inhibitor bracket 2.1-4.2x
    ax.axvspan(2.1, 4.2, color=RUST_LIGHT, lw=0, zorder=0)
    ax.text(3.15, 0.8, 'Strong inhibitor at steady state,\nno dose change: about\n2.1 to 4.2 times Cmax',
            ha='center', va='bottom', fontsize=7.5, color=RUST)
    # crude line through the two means
    xs = [1, 4]
    ax.plot([1, 4], [6, 18], color=TEAL, lw=1.6, zorder=2)
    ax.plot([4, 4.2], [18, 18.8], color=TEAL, lw=1.6, ls=(0, (2, 1.5)), zorder=2)
    ax.plot([1.3, 1], [7.2, 6], color=TEAL, lw=1.6, zorder=2)
    ax.text(2.95, 15.3, 'ΔQTcF ≈ 2 + 4 × multiple', ha='center', va='center', fontsize=7.5, color=TEAL,
            rotation=22, rotation_mode='anchor')
    # thorough QT means with upper 90% bound
    for x, m, u in [(1, 6, 9), (4, 18, 22)]:
        ax.plot([x, x], [m, u], color=TEAL, lw=1.0, zorder=3)
        ax.plot([x - 0.06, x + 0.06], [u, u], color=TEAL, lw=1.0, zorder=3)
        ax.plot([x], [m], 'o', color=TEAL, ms=6, zorder=4)
    ax.text(0.9, 6, 'Therapeutic dose\n6 ms (upper 9)', ha='right', va='center', fontsize=7.5, color=INK)
    ax.text(3.9, 21.5, 'About 4× Cmax\n18 ms (upper 22)', ha='right', va='center', fontsize=7.5, color=INK)
    # scenario points from Calculation 19.2
    for x, y, lab, ha, dx, dy in [(2.1, 10, 'about 10 ms', 'left', 0.08, -1.3),
                                  (4.2, 19, 'about 19 ms', 'left', 0.1, -1.4)]:
        ax.plot([x], [y], 'o', mfc='white', mec=RUST, mew=1.4, ms=6, zorder=5)
        ax.text(x + dx, y + dy, lab, ha=ha, va='center', fontsize=7.5, color=RUST, fontweight='bold')
    ax.plot([1.3], [7], 'D', mfc='white', mec=SAND_DARK, mew=1.4, ms=5.5, zorder=5)
    ax.annotate('20 mg with fluconazole 200 mg:\nabout 1.3× → about 7 ms', xy=(1.28, 7.4), xytext=(0.2, 16.5),
                fontsize=7.5, color=SAND_DARK, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color=SAND_DARK, lw=0.8, shrinkA=0, shrinkB=3))
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 25)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xlabel('Ravolixan exposure, multiple of therapeutic Cmax', fontsize=8)
    ax.set_ylabel('Mean placebo-corrected ΔQTcF (ms)', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig19_4')




def fig19_2():
    """Tamoxifen and CYP2D6 inhibitors: consistent pharmacokinetics, discordant outcomes."""
    fig, (a1, a2) = chart(2.9, ncols=2, gridspec_kw={'width_ratios': [1, 2.6]})
    # left: endoxifen
    a1.bar([0, 1], [12.4, 5.5], color=[TEAL_MID, RUST], width=0.6)
    for x, v in [(0, 12.4), (1, 5.5)]:
        a1.text(x, v + 0.3, f'{v}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    a1.set_xticks([0, 1], ['Tamoxifen', '+ paroxetine'], fontsize=7.5)
    a1.set_ylim(0, 15.5)
    a1.set_ylabel('Mean endoxifen (ng/mL)', fontsize=8)
    a1.set_title('Exposure: consistent', fontsize=8, color=TEAL, loc='left')
    a1.text(0.5, 9.4, '[7]', ha='center', fontsize=7, color=GREY)
    # right: outcomes
    rows = [('Overlap +25%', 1.24, None, None, TEAL, '[9]'), ('Overlap +50%', 1.54, None, None, TEAL, ''),
            ('Overlap +75%', 1.91, None, None, TEAL, ''),
            ('Recurrence', 1.07, 0.88, 1.30, SAND_DARK, '[10]'),
            ('All-cause death', 0.96, 0.88, 1.06, GREY, '[12]')]
    ys = [4.4, 3.8, 3.2, 1.9, 0.9]
    a2.plot([1, 1], [0.55, 4.65], color=GREY, lw=0.8)
    for (lab, est, lo, hi, c, ref), y in zip(rows, ys):
        if lo is not None:
            a2.plot([lo, hi], [y, y], color=c, lw=1.4)
            val = f'{est:.2f} ({lo:.2f} to {hi:.2f}) {ref}'
        else:
            val = f'{est:.2f} {ref}'
        a2.plot([est], [y], 's', color=c, ms=5)
        a2.text(0.45, y, lab, ha='left', va='center', fontsize=7.5)
        a2.text(2.05, y, val, ha='left', va='center', fontsize=7.5)
    a2.text(0.45, 4.95, 'Breast cancer death, Ontario cohort (no intervals given)', ha='left', va='center',
            fontsize=7.5, color=TEAL, fontweight='bold')
    a2.text(0.45, 0.2, 'California cohort [11]: no statistically significant increase', ha='left',
            va='center', fontsize=7.5, color=GREY, style='italic')
    a2.set_title('Outcomes: discordant', fontsize=8, color=RUST, loc='left')
    a2.set_xscale('log')
    a2.set_xlim(0.43, 3.7)
    a2.set_ylim(-0.1, 5.3)
    a2.set_xticks([0.8, 1, 1.5, 2])
    a2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'))
    a2.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    a2.spines['bottom'].set_bounds(0.8, 2)
    a2.set_yticks([]); a2.spines['left'].set_visible(False)
    a2.set_xlabel('Risk ratio (paroxetine or CYP2D6 inhibitor)', fontsize=8)
    fig.tight_layout(w_pad=1.0)
    save(fig, 'fig19_2')


def fig19_3():
    """Ceiling on the AUC ratio from fm (Calculation 19.1) with the ravolixan studies and predictions."""
    fms = [i / 200 for i in range(0, 167)]
    fig, ax = chart(2.9)
    ax.plot(fms, [1 / (1 - f) for f in fms], color=TEAL, lw=1.8)
    ax.text(0.58, 2.75, 'Ceiling with complete inhibition:\nAUC ratio = 1 / (1 − fm)', ha='right',
            va='center', fontsize=7.5, color=TEAL)
    ax.axvline(0.75, color=RULE, lw=0.9, ls=(0, (4, 2)), zorder=0)
    ax.text(0.745, 6.3, 'Ravolixan\nfm ≈ 0.75', ha='right', va='top', fontsize=7.5, color=GREY)
    ax.plot([0.75], [4.0], 'o', mfc='white', mec=TEAL, mew=1.3, ms=6, zorder=4)
    pts = [(4.2, 'Itraconazole 4.2 (3.7 to 4.8), observed', RUST, True),
           (3.9, 'Clarithromycin 3.9, PBPK', RUST, False),
           (2.6, 'Fluconazole 200 mg 2.6, PBPK', SAND_DARK, False),
           (2.0, 'Diltiazem 2.0, observed', SAND_DARK, True)]
    x = 0.77
    ax.plot([x, x], [3.7, 4.8], color=RUST, lw=1.0, zorder=3)
    for v, lab, c, obs in pts:
        ax.plot([x], [v], 'o', color=c, mfc=c if obs else 'white', mec=c, mew=1.3, ms=5.5, zorder=5)
    lab_y = {4.2: 4.75, 3.9: 3.7, 2.6: 2.6, 2.0: 1.95}
    for v, lab, c, obs in pts:
        ax.annotate(lab, xy=(x + 0.008, v), xytext=(0.86, lab_y[v]), fontsize=7.5, color=c, ha='left',
                    va='center', arrowprops=dict(arrowstyle='-', color=c, lw=0.6, shrinkA=0, shrinkB=2))
    ax.text(0.725, 4.0, 'ceiling 4.0', ha='right', va='center', fontsize=7.5, color=TEAL)
    ax.set_xlim(0, 1.32)
    ax.set_ylim(0, 6.6)
    ax.set_xticks([0, 0.25, 0.5, 0.75])
    ax.spines['bottom'].set_bounds(0, 0.85)
    ax.set_xlabel('Fraction of clearance via CYP3A4 (fm)', fontsize=8)
    ax.set_ylabel('AUC ratio', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig19_3')




def fig19_5():
    """The ravolixan discordances sorted into apparent, possibly real, and gaps."""
    fig, ax = diagram(3.0)
    box(ax, 0.9, 2.48, TEXT_W - 1.8, 0.45, 'Do the sources answer the same question, in comparable populations, '
        'exposures, and outcomes?', style='white', size=8, wrapw=70)
    cw, gap = 1.62, 0.12
    x0 = (TEXT_W - (3 * cw + 2 * gap)) / 2
    cols = [('Apparent: explain it', 'light', TEAL,
             ['Small QT effect at the therapeutic dose, yet torsade de pointes: different exposure and population',
              'No torsade de pointes in about 2,900 trial patients, yet 6 post-marketing cases: upper 95% bound about 1 in 1,000; '
              'strong inhibitors excluded']),
            ('Possibly real: carry it forward', 'rust', RUST,
             ['4 events after a documented dose reduction to 20 mg: is the advice adequate when the moderate '
              'inhibitor prolongs QT itself? Highest-value follow-up']),
            ('A gap, not a conflict', 'sand', SAND_DARK,
             ['Clarithromycin prediction untested by a clinical study, but consistent with itraconazole',
              'No observational evidence: frequency and absolute risk unknown'])]
    for k, (head, st, hc, items) in enumerate(cols):
        x = x0 + k * (cw + gap)
        text(ax, x + cw / 2, 2.2, head, size=8, bold=True, color=hc)
        arrow(ax, (TEXT_W / 2 + (k - 1) * 0.6, 2.46), (x + cw / 2, 2.32), color=RULE, lw=0.9, head=5)
        y = 2.05
        for it in items:
            lines = wrap(it, 31).count('\n') + 1
            hh = 0.135 * lines + 0.12
            box(ax, x, y - hh, cw, hh, it, style=st, size=7, wrapw=31)
            y -= hh + 0.08
    note(ax, 'Apparent discordance is resolved by explaining it; real discordance only by better evidence.',
         y=0.12, size=7.5)
    save(fig, 'fig19_5')


if __name__ == '__main__':
    fig19_1(); fig19_2(); fig19_3(); fig19_4(); fig19_5()
