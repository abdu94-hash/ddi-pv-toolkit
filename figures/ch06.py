# Figures for Chapter 6.
from figlib import *
from matplotlib.patches import Circle


def _tp(ax, x, y, label, side, color=TEAL):
    """Transporter marker on a membrane at (x, y) with a label on `side`."""
    ax.add_patch(Circle((x, y), 0.075, fc='white', ec=color, lw=1.3, zorder=5))
    offs = {'left': (-0.11, 0, 'right', 'center'), 'right': (0.11, 0, 'left', 'center')}
    dx, dy, ha, va = offs[side]
    ax.text(x + dx, y + dy, label, ha=ha, va=va, fontsize=7, color=color, fontweight='bold', zorder=6,
            linespacing=1.05)


def fig06_1():
    """Where the main transporters sit in gut, liver and kidney, and which way they move drug."""
    fig, ax = diagram(3.3)
    pw, gap = 1.66, 0.08
    xs = [0.08 + k * (pw + gap) for k in range(3)]
    cy0, cy1 = 1.0, 2.35       # cell bottom (blood side) and top (lumen/bile/urine side)
    titles = ['Intestine', 'Liver', 'Kidney (proximal tubule)']
    tops = ['gut lumen', 'bile', 'urine']
    cells = [(0.18, 1.48), (0.18, 1.48), (0.34, 1.6)]
    notes = ['Inhibit efflux: more absorbed, plasma exposure up',
             'Inhibit uptake: plasma exposure up, liver exposure down',
             'Inhibit secretion: renal clearance down; filtration unchanged']
    for x, t, tp, (c0, c1), nt in zip(xs, titles, tops, cells, notes):
        text(ax, x + pw / 2, 3.15, t, size=8.5, bold=True, color=TEAL)
        text(ax, x + (c0 + c1) / 2, 2.8, tp, size=7.5, color=GREY, italic=True)
        text(ax, x + (c0 + c1) / 2, 0.6, 'blood', size=7.5, color=GREY, italic=True)
        ax.add_patch(FancyBboxPatch((x + c0, cy0), c1 - c0, cy1 - cy0, boxstyle='round,pad=0,rounding_size=0.08',
                                    fc=TEAL_LIGHT, ec=TEAL_MID, lw=0.9, zorder=2))
        box(ax, x + 0.02, 0.06, pw - 0.04, 0.44, nt, style='sand', size=7)

    def efflux(tx, lab):
        _tp(ax, tx, cy1, '', 'right')
        arrow(ax, (tx, cy1 + 0.08), (tx, 2.66), color=TEAL, lw=1.1)
        text(ax, tx, cy1 - 0.13, lab, size=7, bold=True, color=TEAL, va='top')

    def uptake(tx, lab):
        _tp(ax, tx, cy0, '', 'right')
        arrow(ax, (tx, 0.72), (tx, cy0 - 0.08), color=TEAL, lw=1.1)
        text(ax, tx, cy0 + 0.13, lab, size=7, bold=True, color=TEAL, va='bottom')

    # Intestine: drug absorbed downward, P-gp and BCRP pump back to lumen
    x = xs[0]
    arrow(ax, (x + 0.42, 2.68), (x + 0.42, 0.7), color=GREY, lw=1.0)
    text(ax, x + 0.31, 1.68, 'absorption', size=6.5, color=GREY, italic=True, rotation=90)
    efflux(x + 0.85, 'P-gp'); efflux(x + 1.25, 'BCRP')
    # Liver: OATP1B uptake from blood, P-gp/BCRP efflux into bile
    x = xs[1]
    uptake(x + 0.6, 'OATP1B1\nOATP1B3'); efflux(x + 1.1, 'P-gp\nBCRP')
    # Kidney: filtration bypasses the cell; OAT1/3 and OCT2 uptake, P-gp and MATE efflux to urine
    x = xs[2]
    ax.plot([x + 0.12, x + 0.12], [0.62, 2.62], color=SAND_DARK, lw=1.0, ls=(0, (3, 2)), zorder=1)
    arrow(ax, (x + 0.12, 2.55), (x + 0.12, 2.72), color=SAND_DARK, lw=1.0)
    text(ax, x + 0.23, 1.68, 'filtration (unbound drug)', size=6.5, color=SAND_DARK, italic=True, rotation=90)
    uptake(x + 0.68, 'OAT1\nOAT3'); uptake(x + 1.24, 'OCT2')
    efflux(x + 0.68, 'P-gp'); efflux(x + 1.24, 'MATE1\nMATE2-K')
    save(fig, 'fig06_1')


def fig06_3():
    """Calculation 6.1: displacement changes total, not unbound, steady-state concentration."""
    fig, ax = chart(2.55)
    groups = ['Baseline\nfu 0.40, CLu 100 L/day', 'Displacement alone\nfu 0.55, CLu 100 L/day',
              'Displacement plus\nCLu halved\nfu 0.55, CLu 50 L/day']
    tot = [10, 7.3, 14.5]
    unb = [4.0, 4.0, 8.0]
    xs = [0, 1.25, 2.5]
    w = 0.38
    for x, t_, u in zip(xs, tot, unb):
        ax.bar(x - w / 2 - 0.02, t_, width=w, color=TEAL_MID, zorder=2)
        ax.bar(x + w / 2 + 0.02, u, width=w, color=RUST if u > 4 else TEAL, zorder=2)
        ax.text(x - w / 2 - 0.02, t_ + 0.3, f'{t_:g}', ha='center', va='bottom', fontsize=8, color=INK)
        ax.text(x + w / 2 + 0.02, u + 0.3, f'{u:.1f}', ha='center', va='bottom', fontsize=8, color=INK,
                fontweight='bold')
    ax.text(xs[0] - w / 2 - 0.02, 0.4, 'total', ha='center', va='bottom', fontsize=7, color=INK, rotation=90)
    ax.text(xs[0] + w / 2 + 0.02, 0.4, 'unbound', ha='center', va='bottom', fontsize=7, color='white', rotation=90)
    ax.text(xs[1], 10.4, 'total −27%;\nunbound unchanged', ha='center', va='center', fontsize=7.5,
            color=TEAL, style='italic', linespacing=1.1)
    ax.text(xs[2] + 0.45, 8.0, 'unbound\ndoubled', ha='left', va='center', fontsize=7.5, color=RUST,
            style='italic', linespacing=1.1)
    ax.set_xticks(xs, groups, fontsize=7.5)
    ax.set_xlim(-0.55, 3.35); ax.set_ylim(0, 16.5)
    ax.set_ylabel('Average steady-state\nconcentration (mg/L)', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig06_3')


def fig06_5():
    """Methotrexate with trimethoprim-sulfamethoxazole: a kinetic and a dynamic route to the same harm."""
    fig, ax = diagram(3.55)
    # outcome
    box(ax, 4.12, 0.8, 1.1, 1.95, 'Marrow suppression and mucositis:\npancytopenia', style='accent', size=8, bold=True)
    # lane 1: kinetic
    ly, lh = 1.92, 0.83
    box(ax, 0.08, ly + 0.12, 0.95, lh - 0.24, 'TMP–SMX', style='rust', size=8.5, bold=True)
    box(ax, 1.25, ly, 1.55, lh, 'Competes for OAT-mediated secretion. Renal clearance of free methotrexate '
        '12.1 → 5.6 mL/kg/min', style='light', size=7, title='Tubular secretion', align='left')
    box(ax, 3.0, ly + 0.12, 0.92, lh - 0.24, 'Exposure up: mean 66%', style='white', size=7.5, bold=True)
    arrow(ax, (1.05, ly + lh / 2), (1.23, ly + lh / 2), color=RUST)
    arrow(ax, (2.82, ly + lh / 2), (2.98, ly + lh / 2), color=TEAL)
    arrow(ax, (3.94, ly + lh / 2), (4.1, ly + lh / 2), color=RUST)
    text(ax, 0.1, ly + lh + 0.08, 'pharmacokinetic', size=7, color=GREY, italic=True, ha='left', va='bottom')
    # amplifiers
    ay, ah = 2.98, 0.48
    box(ax, 1.25, ay, 1.55, ah, 'NSAIDs also compete at OAT', style='sand', size=7)
    box(ax, 3.0, ay, 2.22, ah, 'Reduced GFR: less filtration left to compensate', style='sand', size=7)
    arrow(ax, (2.02, ay - 0.02), (2.02, ly + lh + 0.02), color=SAND_DARK)
    arrow(ax, (3.46, ay - 0.02), (3.46, ly + lh - 0.1), color=SAND_DARK)
    # lane 2: dynamic
    dy, dh = 0.8, 0.6
    box(ax, 0.08, dy, 0.95, dh, 'Trimethoprim', style='rust', size=8.5, bold=True)
    box(ax, 1.25, dy, 2.67, dh, 'Itself an antifolate: adds to methotrexate at the target', style='light', size=7.5)
    arrow(ax, (1.05, dy + dh / 2), (1.23, dy + dh / 2), color=RUST)
    arrow(ax, (3.94, dy + dh / 2), (4.1, dy + dh / 2), color=RUST)
    text(ax, 0.1, dy + dh + 0.08, 'pharmacodynamic', size=7, color=GREY, italic=True, ha='left', va='bottom')
    # displacement: real but not the mechanism
    box(ax, 0.08, 0.08, 5.14, 0.5, 'Not the mechanism: sulfamethoxazole raises the free fraction (37.4% → 52.2%), but total '
        'clearance did not change significantly. Its main effect is to make a total concentration misleading.',
        style='grey', size=7)
    save(fig, 'fig06_5')


def fig06_2():
    """Berg et al.: creatinine-to-DTPA clearance ratio before and during trimethoprim."""
    fig, (ax, axn) = chart(2.4, ncols=2, gridspec_kw={'width_ratios': [1.25, 1]})
    for lab, a, b, col in (('cyclosporine', 1.21, 0.95, RUST), ('azathioprine', 1.05, 0.99, TEAL)):
        ax.plot([0, 1], [a, b], color=col, lw=1.8, marker='o', ms=6, zorder=3)
        ax.text(-0.08, a, f'{lab}  {a:.2f}', ha='right', va='center', fontsize=8, color=col, fontweight='bold')
        ax.text(1.08, b + (-0.016 if lab == 'azathioprine' else -0.014), f'{b:.2f}', ha='left', va='center',
                fontsize=8, color=col, fontweight='bold')
    ax.axhline(1.0, color=GREY, lw=0.7, ls=(0, (1, 2)))
    ax.text(1.4, 1.006, 'near 1: secretion\nblocked', ha='left', va='bottom', fontsize=7, color=GREY, linespacing=1.05)
    ax.set_xlim(-1.5, 2.0); ax.set_ylim(0.88, 1.27)
    ax.set_xticks([0, 1], ['before', 'trimethoprim\n7 days'], fontsize=8)
    ax.set_yticks([0.9, 1.0, 1.1, 1.2])
    ax.set_ylabel('Creatinine clearance /\nDTPA clearance', fontsize=8)
    axn.axis('off')
    axn.set_xlim(0, 1); axn.set_ylim(0, 1)
    notes = [('Filtration marker (DTPA)', 'unchanged', TEAL),
             ('Serum creatinine', 'rose in every patient', RUST),
             ('Creatinine clearance', 'fell in every patient', RUST)]
    for k, (a, b, col) in enumerate(notes):
        y = 0.86 - k * 0.26
        axn.text(0.02, y, a, ha='left', va='center', fontsize=8, color=INK, fontweight='bold')
        axn.text(0.02, y - 0.1, b, ha='left', va='center', fontsize=8, color=col)
    axn.text(0.02, 0.1, '16 stable renal transplant recipients;\ntrimethoprim 160 mg twice daily', ha='left',
             va='center', fontsize=7, color=GREY, style='italic', linespacing=1.1)
    fig.tight_layout(w_pad=0.5)
    save(fig, 'fig06_2')


def fig06_4():
    """Calculation 6.2: the relative ratio is the same; the absolute exposure is not."""
    fig, ax = chart(2.2)
    rows = [('Normal renal function', 1.0, 1.4, 2), ('Renal function at\n40% of normal', 2.2, 2.9, 1)]
    for lab, a, b, y in rows:
        ax.plot([a, b], [y, y], color=RULE, lw=3, zorder=2)
        ax.plot(a, y, 'o', ms=8, mfc='white', mec=TEAL, mew=1.6, zorder=3)
        ax.plot(b, y, 'o', ms=8, color=RUST, zorder=3)
        lo = '' if y == 2 else '\nwithout inhibitor'
        hi = '' if y == 2 else '\nwith inhibitor'
        ax.text(a, y - 0.26, f'{a:g}' + lo, ha='center', va='top', fontsize=8, color=TEAL, linespacing=1.1)
        ax.text(b, y - 0.26, f'{b:g}' + hi, ha='center', va='top', fontsize=8, color=RUST, fontweight='bold',
                linespacing=1.1)
        ax.text((a + b) / 2, y + 0.18, '×1.4', ha='center', va='bottom', fontsize=8, color=INK)
    ax.set_yticks([2, 1], [r[0] for r in rows], fontsize=8)
    ax.set_ylim(0.25, 2.55); ax.set_xlim(0.7, 3.2)
    ax.set_xticks([1, 1.5, 2, 2.5, 3])
    ax.set_xlabel('AUC relative to a person with normal kidneys taking the drug alone', fontsize=8)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    save(fig, 'fig06_4')


def fig06_6():
    """Worked Case 6.1: timeline of exposures, events and recovery."""
    from matplotlib.patches import Rectangle
    fig, ax = chart(2.6)
    bars = [(3.1, -3, 13, 'methotrexate 15 mg weekly (3 years); stopped on admission', TEAL_LIGHT, TEAL_MID, TEAL),
            (2.45, 1, 8, 'trimethoprim–sulfamethoxazole', RUST_LIGHT, RUST, RUST),
            (1.8, 1, 5, 'ibuprofen (OTC)', RUST_LIGHT, RUST, RUST)]
    for y, a, b, lab, fc, ec, tc in bars:
        ax.add_patch(Rectangle((a, y - 0.2), b - a, 0.4, fc=fc, ec=ec, lw=0.8))
        inside = b - a > 10
        ax.text(a + 0.3 if inside else b + 0.3, y, lab, ha='left', va='center', fontsize=7.5, color=tc)
    ev = [(10, 'day 10: mouth\nulcers, fever', 1.2, 0.0, 'right'),
          (12, 'day 12: admitted; WBC 1.1, neutrophils 0.3,\nplatelets 24 (× 10⁹/L); creatinine 210 µmol/L;\n'
               'methotrexate 0.04 µmol/L', 0.5, 0.0, 'left'),
          (22, 'day 22: counts\nrecovering', 1.2, 0.95, 'left')]
    for x, lab, y, y0, ha in ev:
        col = RUST if x < 20 else TEAL
        ax.plot([x, x], [y0, 1.55], color=col, lw=1.0)
        ax.text(x + (0.25 if ha == 'left' else -0.25), y, lab, ha=ha, va='center', fontsize=7, color=col,
                linespacing=1.1)
    ax.set_xlim(-3, 25.5); ax.set_ylim(0, 3.45)
    ax.set_xticks([1, 4, 8, 10, 12, 22])
    ax.set_xlabel('Day (day 1: antibiotic started)', fontsize=8)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    fig.tight_layout()
    save(fig, 'fig06_6')


if __name__ == '__main__':
    fig06_1(); fig06_2(); fig06_3(); fig06_4(); fig06_5(); fig06_6()
