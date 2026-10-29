# Figures for Chapter 23 (labeling and risk minimization; ravolixan is fictional).
from figlib import *


def fig23_1():
    """Where one interaction is written in the US PI and the EU SmPC (Section 23.2)."""
    rows = [('4', 'Contraindications', 'Contraindicated combinations', '4.3', 'Contraindications'),
            ('2', 'Dosage and Administration', 'The dose modification itself', '4.2', 'Posology'),
            ('5', 'Warnings and Precautions', 'The clinical risk (e.g., QT) and its risk factors', '4.4', 'Special warnings'),
            ('7', 'Drug Interactions', 'Each drug or class: clinical impact, action, examples', '4.5', 'Interactions'),
            ('12.3', 'Pharmacokinetics', 'Study results: AUC and Cmax ratios', '5.2', 'Pharmacokinetics'),
            ('H, 17', 'Highlights; patient counseling', 'Summary and instructions a patient can act on', '', 'Package leaflet')]
    fig, ax = diagram(3.45)
    xl, wl = 0.32, 1.43
    xm, wm = 1.93, 1.72
    xr, wr = 3.83, 1.4
    text(ax, xl + wl / 2, 3.3, 'US prescribing information', size=8, bold=True, color=TEAL)
    text(ax, xm + wm / 2, 3.3, 'What is written there', size=8, bold=True, color=GREY)
    text(ax, xr + wr / 2, 3.3, 'EU SmPC', size=8, bold=True, color=TEAL)
    rh, gap, y0 = 0.4, 0.09, 2.75
    ys = [y0 - k * (rh + gap) for k in range(len(rows))]
    for (us, usn, what, eu, eun), y in zip(rows, ys):
        hub = us == '7'
        st = 'teal' if hub else 'light'
        tc = 'white' if hub else INK
        nc = 'white' if hub else TEAL
        box(ax, xl, y, wl, rh, '', style=st)
        text(ax, xl + 0.08, y + rh / 2, us, size=8.5, bold=True, color=nc, ha='left')
        text(ax, xl + 0.46, y + rh / 2, usn, size=7.5, color=tc, ha='left', wrapw=17)
        box(ax, xm, y, wm, rh, what, style='white', size=7.3, wrapw=32)
        box(ax, xr, y, wr, rh, '', style=st)
        if eu:
            text(ax, xr + 0.08, y + rh / 2, eu, size=8.5, bold=True, color=nc, ha='left')
            text(ax, xr + 0.42, y + rh / 2, eun, size=7.5, color=tc, ha='left')
        else:
            text(ax, xr + 0.08, y + rh / 2, eun, size=7.5, color=tc, ha='left')
        ax.plot([xl + wl + 0.01, xm - 0.01], [y + rh / 2] * 2, color=RULE, lw=0.9, zorder=1)
        ax.plot([xm + wm + 0.01, xr - 0.01], [y + rh / 2] * 2, color=RULE, lw=0.9, zorder=1)
    # US cross-reference: section 4 points to section 7
    y4, y7 = ys[0] + rh / 2, ys[3] + rh / 2
    arrow(ax, (xl - 0.01, y4), (xl - 0.01, y7), color=RUST, lw=0.9, rad=0.22, ls=(0, (3, 2)))
    note(ax, 'Dashed arrow: section 4 cross-refers to section 7. Dark boxes: the main home of the interaction.',
         y=0.12, size=6.8)
    save(fig, 'fig23_1')


def fig23_2():
    """From labeled action to additional risk minimization: a ladder of increasing burden."""
    fig, ax = diagram(3.2)
    steps = [('Monitor', 'what, when, what to do'),
             ('Adjust the dose', 'dose, start, stop'),
             ('Avoid', 'alternative; what if unavoidable'),
             ('Contra-\nindicate', 'named drugs; practical alternative'),
             ('Educational materials', 'professionals or patients'),
             ('Patient alert card', ''),
             ('Controlled access', '')]
    n = len(steps)
    x0, sw, gap = 0.1, 0.7, 0.03
    base = 0.78
    for k, (t, s) in enumerate(steps):
        x = x0 + k * (sw + gap)
        h = 0.72 + k * 0.22
        routine = k < 4
        box(ax, x, base, sw, h, '', style='light' if routine else 'rust', radius=0.04)
        text(ax, x + sw / 2, base + h - 0.08, t, size=7.3, bold=True, color=TEAL if routine else RUST,
             wrapw=12, va='top')
        if s:
            text(ax, x + sw / 2, base + 0.07, s, size=6.5, color=INK, wrapw=14, va='bottom')

    def bracket(xa, xb, y, label, color):
        ax.plot([xa, xa, xb, xb], [y + 0.06, y, y, y + 0.06], color=color, lw=0.9)
        text(ax, (xa + xb) / 2, y - 0.12, label, size=7.5, color=color, bold=True)
    bracket(x0, x0 + 4 * (sw + gap) - gap, 0.7, 'Routine: wording in the label and leaflet', TEAL)
    bracket(x0 + 4 * (sw + gap), x0 + n * (sw + gap) - gap, 0.7, 'Additional measures', RUST)
    arrow(ax, (x0 + 0.05, 0.36), (x0 + n * (sw + gap) - 0.1, 0.36), color=GREY, lw=1.0)
    text(ax, x0 + 0.05, 0.2, 'More burden on prescribers and patients; less clinical discretion',
         size=7, color=GREY, italic=True, ha='left')
    box(ax, 0.1, 2.42, 2.1, 0.66,
        'Serious interaction; routine wording has not changed practice; a tool that can reach the '
        'decision; an effectiveness plan from the start',
        style='sand', size=6.8, title='Before adding a measure', align='left', wrapw=46)
    save(fig, 'fig23_2')


def fig23_4():
    """Calculation 23.1: exposure with each inhibitor at 40 mg and after halving to 20 mg."""
    data = [('Diltiazem (moderate)', 'moderate', 2.0, 1.0, 'measured'),
            ('Fluconazole (moderate)', 'moderate', 2.6, 1.3, 'PBPK'),
            ('Clarithromycin (strong)', 'strong', 3.9, 1.95, 'PBPK'),
            ('Itraconazole (strong)', 'strong', 4.2, 2.1, 'measured')]
    fig, ax = chart(2.45)
    ys = [3.6, 2.6, 1.2, 0.2]
    for (name, cls, r40, r20, src), y in zip(data, ys):
        c = RUST if cls == 'strong' else TEAL
        ax.annotate('', xy=(r20 + 0.06, y), xytext=(r40 - 0.06, y),
                    arrowprops=dict(arrowstyle='-|>', color=GREY, lw=1.0, mutation_scale=8))
        ax.plot(r40, y, 'o', ms=6.5, mfc='white', mec=c, mew=1.4, zorder=3)
        ax.plot(r20, y, 'o', ms=6.5, color=c, zorder=3)
        ax.text(r40 - (0.07 if r40 == 3.9 else 0), y + 0.3, f'{r40:.1f}', ha='center', fontsize=7.5, color=INK)
        lab20 = '≈2.0' if r20 == 1.95 else f'{r20:.1f}'
        ax.text(r20 - 0.09, y, lab20, ha='right', va='center', fontsize=7.5, color=INK, fontweight='bold')
        ax.text(4.75, y, src, va='center', fontsize=7, color=GREY, style='italic')
    ax.set_yticks(ys, [d[0] for d in data], fontsize=8)
    ax.axvline(1.0, color=TEAL, lw=0.9, ls=(0, (3, 2)), zorder=1)
    ax.axvline(4.0, color=GREY, lw=0.9, ls=(0, (3, 2)), zorder=1)
    ax.text(1.04, -0.25, 'usual exposure (40 mg alone)', fontsize=7, color=TEAL, va='bottom', ha='left')
    ax.text(3.96, 4.35, 'ceiling, complete\ninhibition (1/0.25)', fontsize=7, color=GREY, va='top', ha='right')
    ax.text(5.25, 4.35, 'open: 40 mg\nfilled: 20 mg', fontsize=7, color=GREY, ha='right', va='top')
    ax.axhline(1.9, color=RULE, lw=0.6)
    ax.set_xlim(0.5, 5.3)
    ax.set_ylim(-0.3, 4.4)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xlabel('Average ravolixan exposure relative to 40 mg alone (AUC ratio)', fontsize=8)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    fig.subplots_adjust(left=0.24, right=0.98, top=0.97, bottom=0.17)
    save(fig, 'fig23_4')


def fig23_3():
    """Ivabradine: the outcome data behind the contraindication, and the measured effect of the measures."""
    fig, (a1, a2) = chart(2.55, ncols=2, gridspec_kw={'width_ratios': [1, 1.1], 'wspace': 0.45})
    # left: SIGNIFY [14]
    x = [0, 1]
    iv, pl = [17.9, 5.3], [2.1, 3.8]
    bw = 0.34
    a1.bar([xi - bw / 2 - 0.02 for xi in x], iv, bw, color=RUST)
    a1.bar([xi + bw / 2 + 0.02 for xi in x], pl, bw, color=RULE)
    for xi, a, b in zip(x, iv, pl):
        a1.text(xi - bw / 2 - 0.02, a + 0.5, f'{a}%', ha='center', fontsize=7.5, fontweight='bold')
        a1.text(xi + bw / 2 + 0.02, b + 0.5, f'{b}%', ha='center', fontsize=7.5)
    a1.text(0.62, 15.5, 'ivabradine', color=RUST, fontsize=7.5, fontweight='bold', ha='left')
    a1.text(0.62, 13.6, 'placebo', color=GREY, fontsize=7.5, fontweight='bold', ha='left')
    a1.set_xticks(x, ['Bradycardia', 'Atrial\nfibrillation'], fontsize=7.5)
    a1.set_ylim(0, 20)
    a1.set_xlim(-0.55, 1.5)
    a1.set_ylabel('Patients with the event, %', fontsize=7.5)
    a1.tick_params(axis='x', length=0)
    a1.set_title('SIGNIFY outcome study [14]', fontsize=7.5, color=GREY, fontweight='normal', loc='left')
    # right: drug utilization study [15]
    items = [('Without concomitant\nverapamil or diltiazem', 96.1, 99.2), ('Compliant with all\nnew measures', 70.6, 78.4)]
    ys = [1, 0]
    for (lab, b, a), y in zip(items, ys):
        a2.annotate('', xy=(a - 0.4, y), xytext=(b + 0.4, y),
                    arrowprops=dict(arrowstyle='-|>', color=GREY, lw=1.0, mutation_scale=8))
        a2.plot(b, y, 'o', ms=6, mfc='white', mec=TEAL, mew=1.4, zorder=3)
        a2.plot(a, y, 'o', ms=6, color=TEAL)
        a2.text(b - 1.7, y, f'{b}%', ha='right', va='center', fontsize=7.5)
        a2.text(a, y + 0.2, f'{a}%', ha='center', fontsize=7.5, fontweight='bold')
    a2.set_yticks(ys, [i[0] for i in items], fontsize=7.5)
    a2.set_xlim(64, 102)
    a2.set_ylim(-0.5, 1.55)
    a2.set_xlabel('Patients starting ivabradine, %', fontsize=7.5)
    a2.spines['left'].set_visible(False); a2.tick_params(axis='y', length=0)
    a2.text(101.5, -0.42, 'open: before   filled: after', fontsize=6.8, color=GREY, ha='right')
    a2.set_title('Drug utilization study [15]', fontsize=7.5, color=GREY, fontweight='normal', loc='left')
    fig.subplots_adjust(left=0.09, right=0.98, top=0.9, bottom=0.18)
    save(fig, 'fig23_3')


def fig23_5():
    """The ravolixan label and communication, before and after the recommendation."""
    rows = [('Strong inhibitors', 'Avoid; examples ketoconazole and itraconazole',
             'Contraindicated; clarithromycin, itraconazole, ketoconazole, posaconazole, voriconazole named; interrupt ravolixan for a short course'),
            ('Moderate inhibitors', 'Reduce to 20 mg daily; no drugs named',
             'Keep 20 mg; name fluconazole and diltiazem'),
            ('Electrolytes and ECG', 'Correct potassium and magnesium before starting ravolixan',
             'Also before starting a moderate inhibitor; ECG when other QT risk factors are present'),
            ('Who hears about it', 'Readers of the ravolixan label',
             'DHPC to dermatology, primary care, pharmacists; tiered alerts via knowledge bases; reciprocal wording sought')]
    fig, ax = diagram(3.05)
    xl, wl = 0.1, 1.0
    xb, wb = 1.2, 1.55
    xa, wa = 2.97, 2.23
    text(ax, xb + wb / 2, 2.92, 'Current label', size=8, bold=True, color=GREY)
    text(ax, xa + wa / 2, 2.92, 'Recommended (Recommendation 23.1)', size=8, bold=True, color=TEAL)
    hs = [0.66, 0.42, 0.5, 0.58]
    y = 2.8
    for (lab, b, a), h in zip(rows, hs):
        y -= h
        text(ax, xl, y + h / 2, lab, size=7.5, bold=True, color=INK, ha='left', wrapw=14)
        box(ax, xb, y, wb, h, b, style='grey', size=6.8, wrapw=30, align='left')
        box(ax, xa, y, wa, h, a, style='light' if lab != 'Strong inhibitors' else 'rust', size=6.8,
            wrapw=44, align='left')
        arrow(ax, (xb + wb + 0.02, y + h / 2), (xa - 0.02, y + h / 2), color=TEAL)
        y -= 0.1
    note(ax, 'Patient alert card, education and restricted prescribing held in reserve.', y=0.12, size=6.8)
    save(fig, 'fig23_5')


if __name__ == '__main__':
    fig23_1(); fig23_2(); fig23_3(); fig23_4(); fig23_5()
