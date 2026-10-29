# Figures for Chapter 1.
from figlib import *


def fig01_1():
    """Funnel of the Italian spontaneous-report study (chapter ref [4])."""
    stages = [
        ('All reports in the database', 45315),
        ('At least two drugs listed', 17700),
        ('Contained a potential interaction', 5345),
        ('Reaction matched the expected interaction effect', 1159),
        ('Both interacting drugs recorded as suspect', 235),
    ]
    fig, ax = chart(2.5)
    y = list(range(len(stages)))[::-1]
    colors = [RULE, TEAL_MID, TEAL_MID, TEAL, RUST]
    ax.barh(y, [n for _, n in stages], color=colors, height=0.62)
    for yi, (lab, n) in zip(y, stages):
        ax.text(n + 600, yi, f'{n:,}', va='center', fontsize=8.5, color=INK, fontweight='bold')
    ax.set_yticks(y, [lab for lab, _ in stages], fontsize=8.5)
    ax.set_xlim(0, 52000)
    ax.set_xlabel('Number of spontaneous reports')
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    ax.text(1159 + 6600, y[3], '(21.7% of reports with a potential interaction)', fontsize=7.5, color=GREY, va='center', style='italic')
    ax.text(235 + 4400, y[4], '(20.3% of the matching reports)', fontsize=7.5, color=GREY, va='center', style='italic')
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:,.0f}'))
    fig.tight_layout()
    save(fig, 'fig01_1')


def fig01_3():
    """The eight-step framework, its feedback loop, and the two judgments from Step 7."""
    fig, ax = diagram(3.55)
    steps = ['Confirm exposure', 'Define the event', 'Map the mechanism', 'Test the timing',
             'Assess susceptibility', 'Examine alternatives', 'Integrate evidence', 'Decide and document']
    bw, bh, gap = 1.04, 0.62, 0.2
    x0 = (TEXT_W - (4 * bw + 3 * gap)) / 2
    rows = [2.55, 1.45]
    for k, s in enumerate(steps):
        r, c = divmod(k, 4)
        x = x0 + c * (bw + gap)
        style = 'teal' if k in (0, 6) else 'light'
        box(ax, x, rows[r], bw, bh, '', style=style)
        text(ax, x + bw / 2, rows[r] + bh - 0.15, f'STEP {k + 1}', size=7, bold=True,
             color='white' if style == 'teal' else TEAL)
        text(ax, x + bw / 2, rows[r] + 0.22, s, size=8.5, wrapw=16, color='white' if style == 'teal' else INK)
        if c < 3:
            arrow(ax, (x + bw + 0.02, rows[r] + bh / 2), (x + bw + gap - 0.02, rows[r] + bh / 2))
    # row 1 end to row 2 start
    xr = x0 + 3 * (bw + gap) + bw / 2
    ax.plot([xr, xr, x0 + bw / 2], [rows[0] - 0.02, 2.33, 2.33], color=GREY, lw=1.1, zorder=1)
    arrow(ax, (x0 + bw / 2, 2.33), (x0 + bw / 2, rows[1] + bh + 0.02))
    # feedback: new information returns the assessment to Step 1
    xl = x0 - 0.12
    ax.plot([x0 + bw / 2, x0 + bw / 2, xl, xl], [rows[1] - 0.02, rows[1] - 0.16, rows[1] - 0.16, rows[0] + bh / 2],
            color=RUST, lw=1.0, ls=(0, (3, 2)), zorder=1)
    arrow(ax, (xl, rows[0] + bh / 2), (x0 - 0.01, rows[0] + bh / 2), color=RUST, lw=1.0)
    text(ax, xl - 0.08, 2.0, 'new information: back to Step 1', size=6.5, color=RUST, italic=True, rotation=90)
    # Step 7 produces two separate judgments
    x7 = x0 + 2 * (bw + gap) + bw / 2
    jw, jh, jy = 2.0, 0.8, 0.3
    for k, (t, s) in enumerate([('Relevance of the interaction', 'Could this combination, in this patient, have changed exposure or response enough to matter?'),
                                ('Causality of the event', 'How likely is it that the drugs, alone or together, caused what happened?')]):
        jx = TEXT_W / 2 - jw - 0.1 + k * (jw + 0.2)
        box(ax, jx, jy, jw, jh, s, style='sand', size=7.5, title=t, align='left')
        arrow(ax, (x7, rows[1] - 0.02), (jx + jw / 2, jy + jh + 0.02), color=SAND_DARK, lw=0.9)
    text(ax, TEXT_W / 2, 0.13, 'Two statements, written separately. Neither is a number.', size=7.5, color=GREY, italic=True)
    text(ax, x0, 3.37, 'Shaded steps: exposure comes first; Step 7 keeps the judgments apart.', size=7.5, color=GREY, ha='left', italic=True)
    save(fig, 'fig01_3')


def fig01_2():
    """Object and precipitant; the same object drug pushed in two directions (refs [5], [6], [11])."""
    fig, ax = diagram(2.75)
    # object drug in the middle
    box(ax, 1.95, 1.0, 1.4, 0.7, 'Simvastatin\nobject drug;\ndepends on CYP3A', style='teal', size=8.5)
    # inhibitor (left) and inducer (right)
    box(ax, 0.1, 2.0, 1.55, 0.5, 'Itraconazole\nprecipitant: inhibitor', style='rust', size=8)
    box(ax, 3.65, 2.0, 1.55, 0.5, 'Rifampin\nprecipitant: inducer', style='sand', size=8)
    arrow(ax, (1.25, 1.99), (2.15, 1.69), color=RUST)
    arrow(ax, (4.05, 1.99), (3.15, 1.69), color=SAND_DARK)
    text(ax, 1.48, 1.73, 'blocks the\npathway', size=7, color=RUST, italic=True)
    text(ax, 3.85, 1.73, 'makes more\nenzyme', size=7, color=SAND_DARK, italic=True)
    # consequences
    box(ax, 0.1, 0.1, 1.95, 0.72, 'Simvastatin acid AUC about 19-fold [11]. Within days.', style='rust', size=7.5,
        title='Toxicity: muscle injury', align='left')
    box(ax, 3.25, 0.1, 1.95, 0.72, 'Acid AUC down 93% [5]. Over about a week; wears off over about two [6].', style='sand',
        size=7.5, title='Therapeutic failure', align='left')
    arrow(ax, (2.25, 1.04), (1.3, 0.84), color=RUST)
    arrow(ax, (3.05, 1.04), (4.0, 0.84), color=SAND_DARK)
    text(ax, 2.65, 0.45, 'exposure\nup or down', size=7, color=GREY, italic=True)
    save(fig, 'fig01_2')


def fig01_4():
    """Fold changes in the itraconazole interaction studies (refs [11], [12])."""
    fig, ax = chart(2.3)
    rows = [('Simvastatin acid, Cmax', 17, TEAL, '17-fold', '[11]'),
            ('Simvastatin acid, AUC', 19, TEAL, '19-fold', '[11]'),
            ('Lovastatin, Cmax and AUC', 20, SAND_DARK, 'more than 20-fold', '[12]'),
            ('Pravastatin', None, GREY, 'small; not statistically significant', '[11]')]
    y = list(range(len(rows)))[::-1]
    for yi, (lab, v, c, txt, ref) in zip(y, rows):
        if v:
            ax.barh(yi, v - 1, left=1, color=c, height=0.55)
            ax.text(v * (1.38 if v == 20 else 1.08), yi, f'{txt} {ref}', va='center', fontsize=8, color=INK)
        else:
            ax.plot([1], [yi], 'o', color=c, ms=6)
            ax.text(1.12, yi, f'{txt} {ref}', va='center', fontsize=8, color=INK, style='italic')
    ax.annotate('', xy=(26, y[2]), xytext=(20.3, y[2]), arrowprops=dict(arrowstyle='-|>', color=SAND_DARK, lw=1.2))
    ax.set_xscale('log'); ax.set_xlim(0.9, 120)
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100], ['1', '2', '5', '10', '20', '50', '100'])
    ax.axvline(1, color=GREY, lw=0.8)
    ax.set_yticks(y, [r[0] for r in rows], fontsize=8.5)
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    ax.set_xlabel('Increase with itraconazole versus placebo (fold, log scale)')
    fig.tight_layout()
    save(fig, 'fig01_4')


def fig01_5():
    """Worked Case 1.1 timeline: CK and creatinine (fictional teaching case)."""
    fig, (a0, a1, a2) = chart(3.3, nrows=3, sharex=True, gridspec_kw={'height_ratios': [0.9, 1.6, 1.2]})
    # drug bars
    a0.barh(1, 13 + 2, left=-2, height=0.5, color=TEAL); a0.text(-1.6, 1, 'simvastatin 40 mg (3 years)', va='center', fontsize=7.5, color='white')
    a0.barh(0, 12, left=1, height=0.5, color=RUST); a0.text(1.4, 0, 'itraconazole 200 mg', va='center', fontsize=7.5, color='white')
    a0.text(13.4, 0.5, 'both stopped\non admission', va='center', fontsize=7, color=GREY, style='italic')
    a0.set_ylim(-0.6, 1.6); a0.set_yticks([]); a0.spines[['left', 'bottom']].set_visible(False); a0.tick_params(axis='x', length=0)
    # CK (log)
    ck_d, ck = [13, 18, 26], [48000, 6200, 410]
    a1.plot(ck_d, ck, '-o', color=RUST, ms=4.5)
    for d_, v in zip(ck_d, ck):
        a1.text(d_ + 0.5, v * 1.25, f'{v:,}', fontsize=7.5, color=RUST)
    a1.axhline(200, color=GREY, lw=0.8, ls=':'); a1.text(-1.6, 240, 'upper reference 200', fontsize=7, color=GREY)
    a1.set_yscale('log'); a1.set_ylim(100, 200000); a1.set_ylabel('CK (U/L)')
    a1.set_yticks([100, 1000, 10000, 100000], ['100', '1,000', '10,000', '100,000'])
    for d_, lab in [(9, 'thigh pain'), (12, 'dark urine')]:
        a1.axvline(d_, color=RUST, lw=0.8, ls=(0, (3, 2))); a1.text(d_ - 0.25, 3000, lab, fontsize=7, color=RUST, ha='right', va='center', rotation=90, style='italic')
    # creatinine
    a2.plot([13, 30], [186, 97], '-o', color=SAND_DARK, ms=4.5)
    a2.text(13.5, 176, '186', fontsize=7.5, color=SAND_DARK, va='top'); a2.text(29.5, 112, '97', fontsize=7.5, color=SAND_DARK, ha='right')
    a2.axhline(88, color=GREY, lw=0.8, ls=':'); a2.text(-1.6, 96, 'six months earlier: 88', fontsize=7, color=GREY)
    a2.set_ylim(60, 220); a2.set_ylabel('Creatinine\n(µmol/L)')
    for a in (a1, a2):
        a.axvspan(13, 20, color=TEAL_LIGHT, zorder=0)
    a2.text(16.5, 205, 'in hospital', fontsize=7, color=TEAL, ha='center')
    a2.set_xlim(-2, 31); a2.set_xticks([1, 9, 13, 18, 20, 26, 30])
    a2.set_xlabel('Day (day 1 = itraconazole started)')
    fig.tight_layout(h_pad=0.4)
    save(fig, 'fig01_5')


if __name__ == '__main__':
    fig01_1(); fig01_2(); fig01_3(); fig01_4(); fig01_5()
