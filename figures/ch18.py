# Figures for Chapter 18 (fictional ravolixan screening data, Section 18.7).
import math
from figlib import *


def fig18_4():
    """Four exposure strata: observed proportion for the combination against both expectations."""
    fig, ax = chart(2.9)
    cats = ['Neither', 'Ravolixan\nonly', 'Inhibitor\nonly', 'Ravolixan with\ninhibitor']
    vals = [0.200, 0.707, 0.700, 5.00]
    xs = [0, 1, 2, 3.25]
    cols = [RULE, TEAL_MID, TEAL_MID, RUST]
    ax.bar(xs, vals, width=0.6, color=cols)
    labs = ['0.200%', '0.707%', '0.700%', 'Observed 5.00%\n(21 of 420)']
    for x, v, l in zip(xs, vals, labs):
        ax.text(x, v + 0.12, l, ha='center', va='bottom', fontsize=8, color=INK,
                fontweight='bold' if x == 3.25 else 'normal')
    # expectations for the combination
    for v, lab in [(2.47, 'Multiplicative expectation 2.47%\n(10.4 reports expected)'),
                   (1.21, 'Additive expectation 1.21%\n(5.1 reports expected)')]:
        ax.plot([3.25 - 0.42, 3.25 + 0.42], [v, v], color=INK, lw=1.1, ls=(0, (3, 1.5)), zorder=3)
        ax.text(3.25 + 0.5, v, lab, ha='left', va='center', fontsize=7.5, color=INK, linespacing=1.2)
    ax.set_xticks(xs, cats, fontsize=8)
    ax.set_xlim(-0.5, 5.3)
    ax.set_ylim(0, 6.0)
    ax.set_ylabel('Reports describing a QT-related event (%)', fontsize=8)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}'))
    ax.text(1.0, 2.2, 'Each drug alone: about 3.5 times\nthe background proportion', ha='center', va='center',
            fontsize=7.5, color=GREY, style='italic')
    fig.tight_layout()
    save(fig, 'fig18_4')


def fig18_3():
    """Unshrunk and shrunk observed-to-expected ratios when 0.45 reports are expected."""
    E = 0.45
    ns = list(range(1, 9))
    raw = [math.log2(n / E) for n in ns]
    om = [math.log2((n + 0.5) / (E + 0.5)) for n in ns]
    lo = [o - 1.96 / (math.log(2) * math.sqrt(n)) for o, n in zip(om, ns)]
    fig, ax = chart(2.9)
    ax.axhline(0, color=GREY, lw=0.8, zorder=1)
    ax.plot(ns, raw, color=GREY, lw=1.2, marker='o', ms=3.5, mfc='white', zorder=2)
    ax.plot(ns, om, color=TEAL, lw=1.6, marker='o', ms=4, zorder=3)
    ax.plot(ns, lo, color=TEAL_MID, lw=1.2, ls=(0, (3, 1.5)), marker='o', ms=3.5, zorder=2)
    ax.fill_between([2.93, 3.07], -2.6, 4.6, color=RULE, alpha=0.45, lw=0, zorder=0)
    # direct labels at the right end
    ax.text(8.15, raw[-1], 'Unshrunk\nlog2(O/E)', ha='left', va='center', fontsize=7.5, color=GREY)
    ax.text(8.15, om[-1], 'Shrunk (Ω)', ha='left', va='center', fontsize=7.5, color=TEAL, fontweight='bold')
    ax.text(8.15, lo[-1], 'Lower limit\nΩ025', ha='left', va='center', fontsize=7.5, color=TEAL)
    # the observed diltiazem stratum, values as given in Calculation 18.4
    ax.text(2.9, 2.85, '2.73', ha='right', va='bottom', fontsize=7.5, color=GREY)
    ax.text(3.15, 1.88, '1.88', ha='left', va='top', fontsize=7.5, color=TEAL, fontweight='bold')
    ax.text(2.9, 0.42, '0.24', ha='right', va='bottom', fontsize=7.5, color=TEAL)
    ax.plot([3], [-0.17], marker='D', ms=4, mfc='white', mec=RUST, mew=1.1, zorder=4)
    ax.text(3.15, -0.25, '−0.17 (gamma posterior)', ha='left', va='top', fontsize=7.5, color=RUST)
    ax.text(3, 4.75, 'Observed: 3 reports', ha='center', va='bottom', fontsize=7.5, color=INK)
    ax.text(8.0, -0.15, 'screening threshold: Ω025 above 0', ha='right', va='top', fontsize=7, color=GREY,
            style='italic')
    ax.set_xticks(ns)
    ax.set_xlim(0.6, 9.3)
    ax.set_ylim(-2.6, 5.15)
    ax.spines['bottom'].set_bounds(1, 8)
    ax.set_xlabel('Observed reports with both drugs and the event (expected 0.45)', fontsize=8)
    ax.set_ylabel('log2 scale (0 = as expected)', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig18_3')




def fig18_1():
    """Four exposure strata and the two models of 'no interaction'."""
    fig, ax = diagram(3.05)
    # 2 x 2 grid of strata
    gx, gy, cw, ch = 0.45, 0.6, 1.0, 0.85
    cells = [((0, 1), 'Neither drug', 'f00', 'grey'), ((1, 1), 'Drug 1 only', 'f10', 'light'),
             ((0, 0), 'Drug 2 only', 'f01', 'light'), ((1, 0), 'Both drugs', 'f11', 'rust')]
    for (c, r), name, f, st in cells:
        x, y = gx + c * (cw + 0.08), gy + r * (ch + 0.08)
        box(ax, x, y, cw, ch, '', style=st)
        text(ax, x + cw / 2, y + ch - 0.22, name, size=8, color=INK)
        text(ax, x + cw / 2, y + 0.3, f, size=12, bold=True, color=RUST if st == 'rust' else TEAL)
    text(ax, gx + cw / 2, gy + 2 * ch + 0.08 + 0.14, 'Drug 1 absent', size=7.5, color=GREY)
    text(ax, gx + cw * 1.5 + 0.08, gy + 2 * ch + 0.08 + 0.14, 'Drug 1 present', size=7.5, color=GREY)
    text(ax, gx - 0.14, gy + ch * 1.5 + 0.08, 'Drug 2 absent', size=7.5, color=GREY, rotation=90)
    text(ax, gx - 0.14, gy + ch / 2, 'Drug 2 present', size=7.5, color=GREY, rotation=90)
    text(ax, gx + cw + 0.04, 0.3, 'f = proportion of reports in the stratum that describe the event',
         size=7, color=GREY, italic=True, wrapw=40)
    # the question and the two models
    rx, rw = 2.85, TEXT_W - 0.1 - 2.85
    text(ax, rx, 2.95, 'Does f11 exceed what the other three strata predict without an interaction?',
         size=8, bold=True, color=INK, ha='left', va='top', wrapw=40)
    box(ax, rx, 1.75, rw, 0.62, '', style='light')
    text(ax, rx + 0.1, 2.37 - 0.15, 'Multiplicative model', size=8, bold=True, color=TEAL, ha='left')
    text(ax, rx + 0.1, 1.91, 'expected f11 = f10 × f01 / f00', size=8.5, ha='left')
    box(ax, rx, 1.0, rw, 0.62, '', style='light')
    text(ax, rx + 0.1, 1.62 - 0.15, 'Additive model', size=8, bold=True, color=TEAL, ha='left')
    text(ax, rx + 0.1, 1.16, 'expected f11 = f10 + f01 − f00', size=8.5, ha='left')
    text(ax, rx, 0.85, 'If both drugs are associated with the event on their own, the multiplicative '
         'expectation is higher, so an interaction must be larger to stand out.', size=7, color=GREY,
         italic=True, ha='left', va='top', wrapw=50)
    save(fig, 'fig18_1')


def fig18_2():
    """From statistical interaction signals to communicated signals in a VigiBase feasibility study."""
    rows = [('Drug pairs assessed', 407, TEAL_MID), ('Already known to interact', 157, RULE),
            ('Signals eventually communicated', 3, RUST)]
    fig, ax = chart(1.9)
    y = [2, 1, 0]
    ax.barh(y, [r[1] for r in rows], color=[r[2] for r in rows], height=0.58)
    for yi, (lab, n, c) in zip(y, rows):
        ax.text(n + 6, yi, f'{n}', va='center', fontsize=8.5, fontweight='bold', color=RUST if n == 3 else INK)
    ax.set_yticks(y, [r[0] for r in rows], fontsize=8.5)
    ax.set_xlim(0, 450)
    ax.set_xlabel('Number', fontsize=8)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    ax.text(445, 0.95, 'Triage filters focused preliminary\nassessment on 14% of the\nstatistical signals',
            ha='right', va='center', fontsize=7, color=GREY, style='italic')
    fig.tight_layout()
    save(fig, 'fig18_2')


def fig18_5():
    """PRR and ROR with 95% CIs for the single-drug and within-drug comparisons (Calculations 18.1, 18.2)."""
    rows = [('PRR', 5.21, 3.92, 6.93, 0), ('ROR', 5.26, 3.94, 7.01, 0),
            ('PRR', 7.08, 4.02, 12.47, 1), ('ROR', 7.40, 4.12, 13.27, 1)]
    ys = [3.6, 3.0, 1.2, 0.6]
    fig, ax = chart(2.6)
    for y0, y1 in [(2.75, 3.85), (0.35, 1.45)]:
        ax.plot([1, 1], [y0, y1], color=GREY, lw=0.8)
    for (lab, est, lo, hi, g), y in zip(rows, ys):
        c = TEAL if g == 0 else RUST
        ax.plot([lo, hi], [y, y], color=c, lw=1.4)
        ax.plot([est], [y], 's', color=c, ms=5.5)
        ax.text(0.72, y, lab, ha='right', va='center', fontsize=8, color=INK)
        ax.text(16.5, y, f'{est:.2f} ({lo:.2f} to {hi:.2f})', ha='left', va='center', fontsize=7.5, color=INK)
    ax.text(0.55, 4.15, 'Ravolixan versus all other drugs (Calculation 18.1)', ha='left', va='center',
            fontsize=8, fontweight='bold', color=TEAL)
    ax.text(0.55, 1.75, 'Ravolixan with versus without an inhibitor (Calculation 18.2)', ha='left',
            va='center', fontsize=8, fontweight='bold', color=RUST)
    ax.text(0.55, 2.42, 'Answers: is the event over-represented with ravolixan? Says nothing about inhibitors.',
            ha='left', va='center', fontsize=7, color=GREY, style='italic')
    ax.text(0.55, 0.05, 'Answers: is it over-represented when an inhibitor is co-reported? Cannot separate the '
            'inhibitors’ own effect.', ha='left', va='center', fontsize=7, color=GREY, style='italic')
    ax.set_xscale('log')
    ax.set_xlim(0.55, 40)
    ax.set_ylim(-0.25, 4.45)
    ax.set_xticks([1, 2, 5, 10])
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'))
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.spines['left'].set_visible(False)
    ax.set_yticks([])
    ax.spines['bottom'].set_bounds(1, 20)
    ax.set_xlabel('Ratio, log scale (95% CI)', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig18_5')


if __name__ == '__main__':
    fig18_1(); fig18_2(); fig18_3(); fig18_4(); fig18_5()
