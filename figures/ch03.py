# Figures for Chapter 3.
import math
from figlib import *


def inhibit(ax, p, q, color=RUST, lw=1.2, ls='-', bar=0.09):
    """Line from p to q ending in a flat bar (inhibition)."""
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=1, solid_capstyle='butt')
    a = math.atan2(q[1] - p[1], q[0] - p[0]) + math.pi / 2
    dx, dy = bar * math.cos(a), bar * math.sin(a)
    ax.plot([q[0] - dx, q[0] + dx], [q[1] - dy, q[1] + dy], color=color, lw=lw + 0.6, zorder=1,
            solid_capstyle='butt')


def fig03_3():
    """Clopidogrel activation, where omeprazole and CYP2C19 genotype act."""
    fig, ax = diagram(2.55)
    y, h = 1.82, 0.62
    nodes = [(0.08, 1.0, 'Clopidogrel\n(prodrug)', 'light'),
             (1.33, 1.5, 'Oxidation by CYP enzymes;\nCYP2C19 important', 'light'),
             (3.08, 0.95, 'Active\nmetabolite', 'teal'),
             (4.28, 0.95, 'Antiplatelet\neffect', 'white')]
    for x, w, t, st in nodes:
        box(ax, x, y, w, h, t, style=st, size=8, wrapw=40)
    for (x1, w1, *_), (x2, *_) in zip(nodes, nodes[1:]):
        arrow(ax, (x1 + w1 + 0.03, y + h / 2), (x2 - 0.03, y + h / 2), color=TEAL)
    cx = 1.33 + 0.75
    # modifiers below the CYP2C19 step
    my, mh = 0.7, 0.72
    box(ax, 0.08, my, 2.3, mh, 'Inhibits CYP2C19. Active-metabolite AUC −40% with omeprazole 80 mg; '
        '−14% with pantoprazole 80 mg', style='rust', size=7.5, title='Omeprazole', align='left')
    box(ax, 2.62, my, 2.6, mh, 'Carriers of at least one reduced-function allele: active-metabolite '
        'exposure −32.4%', style='sand', size=7.5, title='Reduced-function CYP2C19 alleles', align='left')
    inhibit(ax, (1.23, my + mh + 0.02), (cx - 0.25, y - 0.05))
    inhibit(ax, (3.9, my + mh + 0.02), (cx + 0.25, y - 0.05), color=SAND_DARK)
    box(ax, 0.08, 0.08, 5.14, 0.44, 'Poor metabolizer (two loss-of-function alleles): the pathway is already largely '
        'absent, so an inhibitor of it has little left to inhibit.', style='grey', size=7.5)
    save(fig, 'fig03_3')


def fig03_4():
    """The exposure-effect-outcome chain for clopidogrel and omeprazole, and where it breaks."""
    fig, ax = diagram(3.55)
    cw, gap = 1.58, 0.2
    xs = [0.08 + k * (cw + gap) for k in range(3)]
    ty = 3.05
    heads = [('Exposure', 'Dedicated interaction studies'),
             ('Effect', 'Pharmacodynamic and biomarker studies'),
             ('Outcome', 'Observational studies and randomized trials')]
    for x, (hd, src) in zip(xs, heads):
        box(ax, x, ty, cw, 0.38, hd, style='teal', size=9)
        text(ax, x + cw / 2, ty - 0.06, src, size=7, color=GREY, italic=True, wrapw=30, va='top')
    # links between columns
    arrow(ax, (xs[0] + cw + 0.03, ty + 0.19), (xs[1] - 0.03, ty + 0.19), color=TEAL)
    arrow(ax, (xs[1] + cw + 0.03, ty + 0.19), (xs[2] - 0.03, ty + 0.19), color=RUST, ls=(0, (2, 2)))
    by = 0.5
    eh = 2.05
    box(ax, xs[0], by, cw, eh, 'Omeprazole 80 mg lowered active-metabolite AUC by 40% (taken together), '
        '47% (12 h apart), and 41% (clopidogrel dose doubled). Pantoprazole 80 mg: 14%.',
        style='white', size=7.5, align='left', title='Pharmacokinetic')
    box(ax, xs[1], by, cw, eh, 'Omeprazole 20 mg in stented patients: platelet reactivity index 51.4% vs 39.8% '
        'with placebo. Volunteers: index up 19.0 to 27.1 points with omeprazole, 3.9 with pantoprazole.',
        style='white', size=7.5, align='left', title='Pharmacodynamic')
    for x, s in ((xs[0], 'Cannot show: whether patients are harmed (healthy volunteers, high omeprazole dose)'),
                 (xs[1], 'Cannot show: more thrombotic events (biomarker endpoint)')):
        ax.plot([x + 0.1, x + cw - 0.1], [by + 0.62, by + 0.62], color=RULE, lw=0.6)
        text(ax, x + 0.1, by + 0.55, s, size=7, color=SAND_DARK, italic=True, ha='left', va='top', wrapw=34)
    oh = (eh - 0.1) / 2
    box(ax, xs[2], by + oh + 0.1, cw, oh, 'PPI users had more events: OR 1.27 and 1.25. Danish cohort: '
        'HR 1.29 with clopidogrel and 1.29 without.', style='sand', size=7.5, align='left', title='Observational')
    box(ax, xs[2], by, cw, oh, 'COGENT: cardiovascular events 4.9% vs 5.7%, HR 0.99 (0.68 to 1.44). '
        'A meaningful difference not ruled out.', style='light', size=7.5, align='left', title='Randomized')
    # verdicts
    vy = 0.33
    text(ax, xs[0] + cw / 2, vy, 'Consistent', size=8.5, bold=True, color=TEAL)
    text(ax, xs[1] + cw / 2, vy, 'Consistent', size=8.5, bold=True, color=TEAL)
    text(ax, xs[2] + cw / 2, vy, 'Conflicting', size=8.5, bold=True, color=RUST)
    text(ax, TEXT_W / 2, 0.07, 'Each link can break: here the chain holds from exposure to effect, but not to outcome.',
         size=7, color=GREY, italic=True)
    save(fig, 'fig03_4')


def fig03_1():
    """Where interaction information sits in US and EU labeling: the advice and its basis."""
    fig, ax = diagram(2.7)
    lx, cw, gap = 1.12, 1.97, 0.08
    xu, xe = lx, lx + cw + gap
    text(ax, xu + cw / 2, 2.52, 'US prescribing information', size=8.5, bold=True, color=TEAL)
    text(ax, xe + cw / 2, 2.52, 'EU SmPC', size=8.5, bold=True, color=TEAL)
    rows = [
        (1.42, 0.86, 'What prescribers\nwere told', 'light',
         ('Section 7, Drug Interactions', 'Recommendations, often as a table of drugs, effects and management. '
          'Also: boxed warning; sections 2, 4, 5'),
         ('Section 4.5', 'Consequence, mechanism, size of effect, recommendation. Also: 4.3 contraindicated '
          'combinations; 4.4 warnings; 4.2 dose adjustments')),
        (0.56, 0.74, 'Why: the\nbasis', 'white',
         ('Section 12.3, Pharmacokinetics', 'Studies done, doses, exposure changes, and in vitro findings never '
          'tested clinically'),
         ('Section 5.2', 'Metabolic pathways and transporters: where to check the mechanism')),
    ]
    for y, h, lab, st, us, eu in rows:
        text(ax, 0.08, y + h / 2, lab, size=8, bold=True, ha='left', color=INK)
        box(ax, xu, y, cw, h, us[1], style=st, size=7, title=us[0], align='left')
        box(ax, xe, y, cw, h, eu[1], style=st, size=7, title=eu[0], align='left')
    box(ax, 0.08, 0.06, 5.14, 0.38, 'For every label used, record document, region, product, revision date and section.',
        style='sand', size=7.5)
    save(fig, 'fig03_1')


def fig03_2():
    """How often interaction resources agree: three comparison studies."""
    fig, ax = chart(2.5)
    ys = [2, 1, 0]
    h = 0.42
    # 1. Abarca: 406 interactions rated major in at least one of four compendia
    ax.barh(ys[0], 100, height=h, color='#EEF1F2', ec=RULE, lw=0.6)
    ax.barh(ys[0], 71.7, left=100 - 71.7, height=h, color=RUST)
    ax.barh(ys[0], 2.2, height=h, color=TEAL)
    ax.text(100 - 71.7 / 2, ys[0], 'major in only one: 71.7%', ha='center', va='center', fontsize=7.5, color='white')
    ax.text(3.2, ys[0] + 0.33, 'major in all four: 2.2% (9 of 406)', ha='left', va='bottom', fontsize=7.5,
            color=TEAL, fontweight='bold')
    # 2. Wang: 59 boxed-warning contraindicated combinations, three screening programs
    ax.barh(ys[1], 100, height=h, color='#EEF1F2', ec=RULE, lw=0.6)
    ax.barh(ys[1], 68, height=h, color=TEAL_MID)
    ax.barh(ys[1], 3 / 59 * 100, height=h, color=TEAL)
    ax.text(34, ys[1], 'covered by any program: 68%', ha='center', va='center', fontsize=7.5, color=INK)
    ax.text(3.2, ys[1] + 0.33, 'detected and rated by all three: 3 of 59', ha='left', va='bottom', fontsize=7.5,
            color=TEAL, fontweight='bold')
    # 3. Vitry: major in one compendium but absent from the others
    ax.plot([0, 100], [ys[2], ys[2]], color=RULE, lw=0.6)
    ax.plot([14, 44], [ys[2], ys[2]], color=RUST, lw=7, solid_capstyle='butt')
    ax.text(46, ys[2], '14% to 44% not listed at all\nin the other compendia', ha='left', va='center', fontsize=7.5,
            color=RUST, linespacing=1.1)
    ax.set_yticks(ys, ['406 interactions rated\nmajor in any of four\nUS compendia',
                       '59 combinations\ncontraindicated in\nUS boxed warnings',
                       'Interactions rated\nmajor in one of four\ninternational compendia'], fontsize=7.5)
    ax.set_xlim(0, 100); ax.set_ylim(-0.5, 2.6)
    ax.set_xticks([0, 25, 50, 75, 100], ['0%', '25%', '50%', '75%', '100%'])
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    save(fig, 'fig03_2')


def fig03_5():
    """Worked Case 3.1 before and after follow-up."""
    fig, ax = diagram(3.0)
    c0, c1, c2 = 0.08, 1.5, 3.42
    w1, w2 = 1.7, 1.8
    text(ax, c1 + w1 / 2, 2.85, 'At intake', size=8.5, bold=True, color=GREY)
    text(ax, c2 + w2 / 2, 2.85, 'After follow-up', size=8.5, bold=True, color=TEAL)
    rows = [('Adherence', 'unknown', 'uninterrupted clopidogrel supply'),
            ('Procedure', 'unknown', 'well-expanded stent'),
            ('CYP2C19 genotype', 'unknown', 'poor-metabolizer genotype (two loss-of-function alleles)'),
            ('Reference disagreement', 'does not change the decision', 'does not change the decision')]
    rh, rg = 0.38, 0.08
    for k, (lab, a, b) in enumerate(rows):
        y = 2.3 - k * (rh + rg)
        text(ax, c0, y + rh / 2, lab, size=7.5, ha='left', bold=True)
        box(ax, c1, y, w1, rh, a, style='grey', size=7)
        box(ax, c2, y, w2, rh, b, style='light' if a == 'unknown' else 'grey', size=7, wrapw=34)
        arrow(ax, (c1 + w1 + 0.03, y + rh / 2), (c2 - 0.03, y + rh / 2), color=TEAL if a == 'unknown' else RULE)
    y = 0.1
    text(ax, c0, y + 0.3, 'Assessment', size=7.5, ha='left', bold=True)
    box(ax, c1, y, w1, 0.6, 'Interaction a possible contributor; adherence and genotype the key unknowns',
        style='sand', size=7)
    box(ax, c2, y, w2, 0.6, 'Interaction a weak explanation; genetically reduced activation the more likely '
        'contributor', style='accent', size=7, bold=False)
    arrow(ax, (c1 + w1 + 0.03, y + 0.3), (c2 - 0.03, y + 0.3), color=RUST)
    save(fig, 'fig03_5')


if __name__ == '__main__':
    fig03_1(); fig03_2(); fig03_3(); fig03_4(); fig03_5()
