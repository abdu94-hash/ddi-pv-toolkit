# Figures for Chapter 17 (ravolixan QT series; fictional teaching data from Section 17.6).
from figlib import *


def count_box(ax, x, y, w, h, label, n, sub, style='light', size=7.5, wrapw=None):
    """Box with a bold label and count on the first line and smaller detail below."""
    box(ax, x, y, w, h, '', style=style)
    tc = 'white' if style in ('teal', 'accent') else INK
    hc = 'white' if style in ('teal', 'accent') else (RUST if style == 'rust' else TEAL)
    top = y + h - 0.09
    ax.text(x + 0.1, top, label, ha='left', va='top', fontsize=8.5, fontweight='bold', color=hc, zorder=3)
    ax.text(x + w - 0.1, top, str(n), ha='right', va='top', fontsize=10, fontweight='bold', color=hc, zorder=3)
    if sub:
        ax.text(x + 0.1, top - 0.21, wrap(sub, wrapw or int(w * 72 / (size * 0.5)) - 2), ha='left', va='top',
                fontsize=size, color=tc, zorder=3, linespacing=1.25)


def fig17_4():
    """Retrieval flow for the ravolixan QT series with method at each step."""
    fig, ax = diagram(3.75)
    mx, mw = 0.15, 2.85          # main column
    rx, rw = 3.25, 1.9           # side column
    # Row 1: retrieval
    y1, h1 = 2.92, 0.72
    count_box(ax, mx, y1, mw, h1, 'Retrieved', 52,
              'SMQ Torsade de pointes/QT prolongation, broad scope; all drug roles; data lock point 30 June 2026')
    # Row 2: deduplication
    y2, h2 = 2.18, 0.42
    count_box(ax, mx, y2, mw, h2, 'Unique cases after deduplication', 47, '', style='teal')
    xc = mx + mw / 2
    arrow(ax, (xc, y1 - 0.01), (xc, y2 + h2 + 0.02))
    # side box: duplicates merged
    yd, hd = 2.12, 1.0
    count_box(ax, rx, yd, rw, hd, 'Duplicates merged', 5,
              '3 received directly and again from a regulatory authority; 1 literature report of a patient '
              'already reported; 1 follow-up entered as a new case', style='grey', size=7, wrapw=38)
    ymid = (y1 + y2 + h2) / 2 + 0.02
    ax.plot([xc, rx - 0.02], [ymid, ymid], color=GREY, lw=1.0, zorder=1)
    arrow(ax, (rx - 0.15, ymid), (rx - 0.01, ymid))
    # Row 3: split by inhibitor
    y3, h3 = 0.86, 0.78
    lw_, gap = 2.42, 0.16
    lx = mx
    rx3 = lx + lw_ + gap
    rw3 = TEXT_W - 0.15 - rx3
    count_box(ax, lx, y3, lw_, h3, 'Moderate or strong CYP3A4 inhibitor', 21,
              'Clarithromycin 9, fluconazole 7, diltiazem 3, itraconazole 2 (inhibitor defined by active '
              'ingredient before the search)', style='rust', size=7, wrapw=46)
    count_box(ax, rx3, y3, rw3, h3, 'No CYP3A4 inhibitor', 26,
              '14 with another QT-prolonging drug; 12 with structural heart disease or electrolyte abnormality',
              style='white', size=7, wrapw=44)
    ysplit = y2 - 0.16
    ax.plot([lx + lw_ / 2, rx3 + rw3 / 2], [ysplit, ysplit], color=GREY, lw=1.0, zorder=1)
    ax.plot([xc, xc], [y2 - 0.01, ysplit], color=GREY, lw=1.0, zorder=1)
    arrow(ax, (lx + lw_ / 2, ysplit), (lx + lw_ / 2, y3 + h3 + 0.02))
    arrow(ax, (rx3 + rw3 / 2, ysplit), (rx3 + rw3 / 2, y3 + h3 + 0.02))
    # Row 4: what happens next
    y4, h4 = 0.1, 0.56
    box(ax, lx, y4, lw_, h4, 'Each case classified for overlap, label adherence and information quality; '
        'none dropped (Figure 17.5)', style='sand', size=7.5, wrapw=46)
    box(ax, rx3, y4, rw3, h4, 'Not a clean comparison group: more than half co-reported another '
        'QT-prolonging drug', style='sand', size=7.5, wrapw=46)
    arrow(ax, (lx + lw_ / 2, y3 - 0.01), (lx + lw_ / 2, y4 + h4 + 0.02), color=SAND_DARK, lw=0.9)
    arrow(ax, (rx3 + rw3 / 2, y3 - 0.01), (rx3 + rw3 / 2, y4 + h4 + 0.02), color=SAND_DARK, lw=0.9)
    save(fig, 'fig17_4')


def fig17_5():
    """The 21 inhibitor cases classified on three separate axes."""
    rows = [
        ('Exposure overlap', [('Confirmed', 11, TEAL), ('Probable', 5, TEAL_MID), ('Unknown', 4, RULE), ('None', 1, GREY)]),
        ('Label adherence', [('Not followed', 8, RUST), ('Reduced to 20 mg', 4, TEAL_MID), ('Not applicable or\nnot assessable', 9, RULE)]),
        ('Information quality', [('Grade A', 7, TEAL), ('Grade B', 9, TEAL_MID), ('Grade C', 5, RULE)]),
    ]
    fig, ax = chart(3.1)
    ys = [2.5, 1.25, 0.0]
    for y, (lab, segs) in zip(ys, rows):
        left = 0
        for name, n, c in segs:
            ax.barh(y, n, left=left, color=c, height=0.5, edgecolor='white', linewidth=1.2)
            tc = 'white' if c in (TEAL, RUST, GREY) else INK
            ax.text(left + n / 2, y, str(n), ha='center', va='center', fontsize=8.5, fontweight='bold', color=tc)
            if name == 'None':
                ax.text(left + n / 2, y + 0.33, name, ha='center', va='bottom', fontsize=7.5, color=INK)
            else:
                ax.text(left + n / 2, y + 0.33, name, ha='center', va='bottom', fontsize=7.5, color=INK,
                        wrap=False)
            left += n
    # bracket: follow-up requested for probable + unknown
    yb = 2.5 + 0.66
    ax.plot([11.1, 11.1, 19.9, 19.9], [yb - 0.07, yb, yb, yb - 0.07], color=RUST, lw=0.9)
    ax.text(15.5, yb + 0.05, 'follow-up requested: 9 cases', ha='center', va='bottom', fontsize=7.5, color=RUST, style='italic')
    # breakdown of 'not followed'
    ax.text(0.1, 1.25 - 0.33, 'not followed: strong inhibitor 5; moderate inhibitor without dose reduction 3',
            ha='left', va='top', fontsize=7, color=GREY, style='italic')
    ax.set_yticks(ys, [r[0] for r in rows], fontsize=8.5)
    ax.set_xlim(0, 21.3); ax.set_ylim(-0.4, 3.45)
    ax.set_xticks([0, 5, 10, 15, 21])
    ax.set_xlabel('Cases with a co-reported moderate or strong CYP3A4 inhibitor (n = 21)')
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    save(fig, 'fig17_5')




def fig17_1():
    """What the narrow and broad SMQ scopes retrieve, and what neither catches."""
    fig, ax = diagram(3.0)
    # nested scopes on the left
    bx, by, bw, bh = 0.1, 0.55, 2.75, 2.35
    box(ax, bx, by, bw, bh, '', style='light')
    text(ax, bx + 0.12, by + bh - 0.15, 'BROAD SCOPE', size=7, bold=True, color=TEAL, ha='left')
    text(ax, bx + 0.12, by + bh - 0.33, 'adds terms that might represent an unrecognized arrhythmia:',
         size=7.5, ha='left', va='top', wrapw=44)
    text(ax, bx + 0.12, by + bh - 0.72, 'syncope · loss of consciousness · cardiac arrest · '
         'ventricular arrhythmias · sudden death', size=7.5, ha='left', va='top', wrapw=44, color=TEAL)
    nx, ny, nw, nh = bx + 0.22, by + 0.2, bw - 0.44, 0.8
    box(ax, nx, ny, nw, nh, '', style='teal')
    text(ax, nx + 0.12, ny + nh - 0.15, 'NARROW SCOPE', size=7, bold=True, color='white', ha='left')
    text(ax, nx + 0.12, ny + nh - 0.33, 'Terms that describe QT prolongation and torsade de pointes themselves',
         size=7.5, color='white', ha='left', va='top', wrapw=40)
    note(ax, 'Torsade de pointes often presents as syncope or cardiac arrest with no recorded rhythm,',
         y=0.36, size=7)
    note(ax, 'so the ravolixan series retrieves with the broad scope and classifies each case clinically.',
         y=0.2, size=7)
    # what the definition still misses, on the right
    rx, rw = 3.05, TEXT_W - 0.1 - 3.05
    box(ax, rx, 1.95, rw, 0.95, 'A QTc result only in the narrative, in a case coded as palpitations. '
        'Recoding after follow-up that moves a case in or out between reviews.', style='rust', size=7.5,
        title='Missed by either scope', align='left', wrapw=37)
    box(ax, rx, 0.55, rw, 1.15, 'Hypokalemia and hypomagnesemia: extracted as co-reported terms within '
        'the series, not part of the event definition.', style='sand', size=7.5,
        title='Extracted separately', align='left', wrapw=37)
    save(fig, 'fig17_1')


def fig17_3():
    """Decision rules for classifying exposure overlap, with an example case for each category."""
    fig, ax = diagram(3.55)
    qx, qw, qh = 0.1, 2.75, 0.62
    ox, ow, oh = 3.3, TEXT_W - 0.1 - 3.3, 0.62
    qs = ['Do dates or clear statements place both drugs in use at event onset?',
          'Do the dates show the precipitant was not in use at the relevant time, allowing for its offset?',
          'Does the narrative describe concurrent use, with at least one date missing or partial?']
    outs = [('Confirmed overlap', 'MT-25-0457: fluconazole, onset day 5', 'teal'),
            ('No overlap', 'MT-26-0390: diltiazem stopped 3 weeks before ravolixan', 'grey'),
            ('Probable overlap', 'MT-26-0219: clarithromycin, not dated', 'light')]
    ys = [2.8, 1.95, 1.1]
    for q, (name, ex, st), y in zip(qs, outs, ys):
        box(ax, qx, y, qw, qh, q, style='white', size=7.5, wrapw=50)
        box(ax, ox, y, ow, oh, '', style=st)
        tc = 'white' if st == 'teal' else (TEAL if st == 'light' else INK)
        text(ax, ox + 0.1, y + oh - 0.17, name, size=8, bold=True, color=tc, ha='left')
        text(ax, ox + 0.1, y + 0.2, ex, size=7, color='white' if st == 'teal' else INK, ha='left', wrapw=42)
        arrow(ax, (qx + qw + 0.02, y + qh / 2), (ox - 0.02, y + qh / 2))
        text(ax, (qx + qw + ox) / 2, y + qh / 2 + 0.09, 'yes', size=7, color=GREY, italic=True)
    for y0, y1 in zip(ys[:-1], ys[1:]):
        arrow(ax, (qx + 0.4, y0 - 0.01), (qx + 0.4, y1 + qh + 0.01))
        text(ax, qx + 0.5, (y0 + y1 + qh) / 2, 'no', size=7, color=GREY, italic=True, ha='left')
    # final: unknown
    yu = 0.3
    arrow(ax, (qx + 0.4, ys[-1] - 0.01), (qx + 0.4, yu + oh / 2), )
    ax.plot([qx + 0.4, ox - 0.02], [yu + oh / 2, yu + oh / 2], color=GREY, lw=1.1, zorder=1)
    arrow(ax, (ox - 0.2, yu + oh / 2), (ox - 0.02, yu + oh / 2))
    text(ax, qx + 0.5, (ys[-1] + yu + oh / 2) / 2 + 0.05, 'no', size=7, color=GREY, italic=True, ha='left')
    text(ax, qx + 0.55, yu + oh / 2 + 0.1, 'Both drugs listed, no basis for judging timing', size=7,
         color=GREY, italic=True, ha='left')
    box(ax, ox, yu, ow, oh, '', style='sand')
    text(ax, ox + 0.1, yu + oh - 0.17, 'Unknown', size=8, bold=True, color=SAND_DARK, ha='left')
    text(ax, ox + 0.1, yu + 0.2, 'MT-25-1106: consumer report, no dates', size=7, ha='left', wrapw=42)
    text(ax, qx, 0.1, 'Every category stays in the series; none is deleted.', size=7.5, color=GREY,
         italic=True, ha='left')
    save(fig, 'fig17_3')




def fig17_2():
    """Where duplicates come from, how candidate pairs are compared, and what is recorded."""
    fig, ax = diagram(3.2)
    sx, sw = 0.1, 2.15
    srcs = [('Same patient reported by a physician and by a pharmacist or the patient', ''),
            ('Received directly and again from a regulatory authority or partner', 'ravolixan: 3'),
            ('Published case that duplicates a spontaneous report', 'ravolixan: 1'),
            ('Follow-up entered as a new case, not a new version', 'ravolixan: 1')]
    text(ax, sx, 2.96, 'Usual sources', size=8, bold=True, color=TEAL, ha='left')
    bh, gap = 0.56, 0.1
    ys = [2.83 - (k + 1) * bh - k * gap for k in range(4)]
    for (s, n), y in zip(srcs, ys):
        box(ax, sx, y, sw, bh, s, style='light', size=7.5, wrapw=38 if not n else 30,
            align='left')
        if n:
            text(ax, sx + sw - 0.08, y + bh / 2, n, size=7, color=RUST, bold=True, ha='right')
    mx, mw = 2.55, 1.25
    my, mh = 1.1, 1.2
    box(ax, mx, my, mw, mh, 'age, sex, country, onset date, drugs, and narrative', style='white', size=7.5,
        title='Compare each candidate pair on', align='left', wrapw=20)
    for y in ys:
        arrow(ax, (sx + sw + 0.02, y + bh / 2), (mx - 0.02, my + mh / 2), color=RULE, lw=0.9, head=5)
    rx, rw = 4.05, TEXT_W - 0.1 - 4.05
    box(ax, rx, 1.1, rw, 1.2, 'Merged or not, and why, for every pair, so the counts can be reproduced at the '
        'next review.', style='sand', size=7.5, title='Record', align='left', wrapw=20)
    arrow(ax, (mx + mw + 0.02, my + mh / 2), (rx - 0.02, 1.7))
    text(ax, (mx + TEXT_W - 0.1) / 2, 0.62, 'Ravolixan series: 52 retrieved, 5 merged, 47 unique.', size=7.5,
         color=RUST, ha='center')
    text(ax, (mx + TEXT_W - 0.1) / 2, 0.3, 'In VigiBase, suspected duplicates were more common among literature '
         '(11%) and fatal (5%) reports [13].', size=7, color=GREY, italic=True, ha='center', wrapw=56)
    save(fig, 'fig17_2')


if __name__ == '__main__':
    fig17_1(); fig17_2(); fig17_3(); fig17_4(); fig17_5()
