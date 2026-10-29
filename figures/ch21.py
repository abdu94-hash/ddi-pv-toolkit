# Figures for Chapter 21.
import datetime as dt
import matplotlib.dates as mdates
from figlib import *


def fig21_2():
    """Effect remaining after a precipitant is stopped: single-exponential recovery (Calculation 21.1)."""
    days = [d / 20 for d in range(0, 42 * 20 + 1)]
    curves = [(1.0, GREY, 'Reversible inhibitor\n(voriconazole, about 1 day)'),
              (2.3, TEAL, 'Time-dependent inhibitor\n(ritonavir estimate, 2.3 days)'),
              (8.0, RUST, 'Inducer\n(rifampin, about 8 days)')]
    fig, ax = chart(3.0)
    # washout markers (fictional RVX-305 protocol)
    for x, lab in [(14, 'RVX-305 inhibitor\nwashout, 14 days'), (28, 'RVX-305 inducer\nwashout, 28 days')]:
        ax.axvline(x, color=RULE, lw=1.0, ls=(0, (4, 2)), zorder=0)
        ax.text(x + 0.4, 104, lab, ha='left', va='top', fontsize=7, color=GREY)
    # schematic plasma curve for the time-dependent inhibitor
    pl = [100 * 0.5 ** (t / 0.3) for t in days]
    ax.plot(days, pl, color=GREY, lw=1.0, ls=(0, (2, 1.5)), label='Time-dependent inhibitor in plasma (schematic)')
    names = ['Reversible inhibitor: recovery half-life about 1 day (voriconazole)',
             'Time-dependent inhibitor: 2.3 days (ritonavir estimate)',
             'Inducer: about 8 days (rifampin)']
    for (t_half, c, _), nm in zip(curves, names):
        ax.plot(days, [100 * 0.5 ** (t / t_half) for t in days], color=c, lw=1.8, label=nm)
    h, l = ax.get_legend_handles_labels()
    order = [1, 2, 3, 0]
    ax.legend([h[i] for i in order], [l[i] for i in order], loc='upper right', bbox_to_anchor=(1.0, 0.85),
              fontsize=7.5, handlelength=2.2, labelspacing=0.5, borderaxespad=0.2, frameon=True,
              facecolor='white', edgecolor='none', framealpha=1.0)
    # points stated in Calculation 21.1
    ax.plot([11.5], [3], 'o', color=TEAL, ms=4.5, zorder=4)
    ax.annotate('five half-lives:\nabout 3% remains', xy=(11.5, 3.6), xytext=(8.6, 15), fontsize=7, color=TEAL,
                ha='left', va='bottom', arrowprops=dict(arrowstyle='-', color=TEAL, lw=0.7, shrinkA=0, shrinkB=2))
    ax.plot([28], [9], 'o', color=RUST, ms=4.5, zorder=4)
    ax.text(28.6, 11, 'about 9% of the\ninduction remains', ha='left', va='bottom', fontsize=7, color=RUST)
    ax.set_xlim(0, 42)
    ax.set_ylim(0, 105)
    ax.set_xticks([0, 7, 14, 21, 28, 35, 42])
    ax.set_xlabel('Days after the last dose of the precipitant', fontsize=8)
    ax.set_ylabel('Effect on the enzyme remaining (%)', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig21_2')


def fig21_5():
    """Participant 114-0087: central QTcF over time against the protocol thresholds (fictional)."""
    D = lambda m, d: dt.date(2026, m, d)
    fig, ax = chart(3.1)
    base = 428
    # exposure spans
    ax.axvspan(D(3, 6), D(3, 10) + dt.timedelta(hours=12), color=RUST_LIGHT, lw=0, zorder=0)
    ax.axvspan(D(3, 11), D(3, 24), color='#EEF1F2', lw=0, zorder=0)
    ax.text(D(3, 8), 515, 'Clarithromycin\n6–10 Mar', ha='center', va='top', fontsize=7, color=RUST)
    ax.text(D(3, 17) + dt.timedelta(hours=12), 515, 'Study drug interrupted\n11–23 Mar', ha='center', va='top',
            fontsize=7, color=GREY)
    # restart criterion band and thresholds
    ax.axhspan(base, base + 10, color=TEAL_LIGHT, lw=0, zorder=0)
    ax.axhline(base, color=TEAL_MID, lw=0.8, zorder=1)
    ax.text(D(2, 27), base - 1.5, 'Baseline 428; shaded: restart criterion, within 10 ms of baseline', ha='left',
            va='top', fontsize=7, color=TEAL)
    for y, lab, c in [(base + 30, 'Rise above 30 ms: interrupt', SAND_DARK),
                      (480, '480 ms: interrupt', SAND_DARK),
                      (500, '500 ms: discontinue', RUST)]:
        ax.axhline(y, color=c, lw=0.8, ls=(0, (4, 2)), zorder=1)
        ax.text(D(2, 21), y + 0.8, lab, ha='left', va='bottom', fontsize=7, color=c)
    # central QTcF
    pts = [(D(2, 24), 433), (D(3, 10), 462), (D(3, 11), 455), (D(3, 13), 444), (D(3, 17), 432)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=TEAL, lw=1.4, marker='o', ms=4.5, zorder=3)
    ax.plot([D(3, 27)], [437], marker='o', color=TEAL, ms=4.5, zorder=3)
    labels = [(D(2, 24), 433, '433\nweek 12', 'center', 2.5), (D(3, 10), 462, '462', 'right', 0),
              (D(3, 11), 455, '455', 'left', 3.6), (D(3, 13), 444, '444', 'left', 1.5),
              (D(3, 17), 432, '432', 'left', 1.5), (D(3, 27), 437, '437\n2 h post-dose', 'center', 2.5)]
    for d, v, s, ha, dy in labels:
        off = {'center': dt.timedelta(0), 'right': -dt.timedelta(hours=14), 'left': dt.timedelta(hours=10)}[ha]
        ax.text(d + off, v + dy + (0 if ha == 'center' else 0.6), s, ha=ha, va='bottom', fontsize=7, color=TEAL,
                fontweight='bold' if v == 462 else 'normal', linespacing=1.1)
    # site machine Bazett value
    ax.plot([D(3, 10)], [498], marker='o', mfc='white', mec=GREY, mew=1.1, ms=4.5, zorder=3)
    ax.text(D(3, 9) + dt.timedelta(hours=6), 491, 'Site machine QTc (Bazett) 498:\nnot the measure the rules use',
            ha='right', va='center', fontsize=7, color=GREY, style='italic')
    ax.text(D(3, 10) + dt.timedelta(hours=14), 466, 'K 3.2, Mg 0.68', ha='left', va='bottom', fontsize=7,
            color=RUST)
    # restart
    ax.text(D(3, 24) + dt.timedelta(hours=10), 470, 'Restart\n24 Mar', ha='left', va='center', fontsize=7, color=INK)
    ax.set_xlim(D(2, 20), D(3, 31))
    ax.set_ylim(420, 516)
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 8, 15, 22]))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: f'{mdates.num2date(v).day} {mdates.num2date(v):%b}'))
    ax.set_ylabel('Central QTcF (ms)', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig21_5')




def fig21_1():
    """Three tiers of concomitant medicines in RVX-305, defined by mechanism and strength."""
    fig, ax = diagram(3.55)
    cols = [('Prohibited', 'Risk cannot be managed in the trial, or efficacy assessment would be invalid', 'accent',
             ['Strong CYP3A4 inhibitors, e.g. itraconazole, clarithromycin',
              'Strong CYP3A4 inducers, e.g. rifampin',
              'Medicines with a known risk of torsade de pointes']),
            ('Restricted', 'Allowed under conditions', 'sand',
             ['Moderate CYP3A4 inhibitors, e.g. diltiazem, fluconazole: only with medical monitor approval '
              'and an extra ECG (illustrative)']),
            ('Permitted', 'Everything else, including background therapy for the disease', 'light',
             ['e.g. methotrexate', 'Thiazide: permitted, but predisposes to hypokalemia; '
              'review as a risk modifier'])]
    cw, gap = 1.62, 0.12
    x0 = (TEXT_W - (3 * cw + 2 * gap)) / 2
    yt = 2.68
    for k, (name, why, st, items) in enumerate(cols):
        x = x0 + k * (cw + gap)
        box(ax, x, yt, cw, 0.42, name, style=st, size=9)
        text(ax, x + cw / 2, yt - 0.08, why, size=7, color=GREY, italic=True, va='top', wrapw=30)
        y = yt - 0.62
        for it in items:
            lines = wrap(it, 30).count('\n') + 1
            hh = 0.16 * lines + 0.14
            box(ax, x, y - hh, cw, hh, it, style='white', size=7.5, wrapw=30)
            y -= hh + 0.08
    # clarithromycin: two grounds
    text(ax, x0 + cw + gap, 0.75, 'Clarithromycin is prohibited on two separate grounds: strong CYP3A4 inhibition and '
         'its own QT warning.', size=7.5, color=RUST, ha='left', wrapw=62)
    arrow(ax, (x0, 3.27), (TEXT_W - x0, 3.27), color=RULE, lw=1.0, head=7)
    text(ax, TEXT_W / 2, 3.33, 'risk increasingly manageable within the trial', size=7, color=GREY, italic=True,
         va='bottom')
    text(ax, x0 + cw + gap, 0.3, 'Lists are written by mechanism and strength, then illustrated with named examples.',
         size=7, color=GREY, italic=True, ha='left')
    save(fig, 'fig21_1')


def fig21_3():
    """SUSAR decision for an event that may involve an interaction, with the path of participant 114-0087."""
    fig, ax = diagram(4.0)
    qx, qw, qh = 0.1, 2.9, 0.68
    ox, ow = 3.35, TEXT_W - 0.17 - 3.35
    qs = [('Serious?', 'ICH E2A criteria. An asymptomatic QTc increase usually is not; torsade de pointes usually is.'),
          ('Suspected?', 'An interaction that raised exposure strengthens suspicion of the investigational '
                         'product; the concomitant drug can be coded as interacting.'),
          ('Unexpected?', 'Judged against the IB reference safety information. If it lists ECG QT prolonged, '
                          'torsade de pointes is unexpected.')]
    ys = [3.1, 2.15, 1.2]
    exits = ['Not a SUSAR: adverse event, or AESI under the protocol', 'Not a SUSAR', 'Not a SUSAR: listed']
    for (t, d), y, ex in zip(qs, ys, exits):
        box(ax, qx, y, qw, qh, '', style='white')
        text(ax, qx + 0.1, y + qh - 0.1, t, size=8.5, bold=True, color=TEAL, ha='left', va='top')
        text(ax, qx + 0.1, y + qh - 0.29, d, size=7, ha='left', va='top', wrapw=66)
        if y == ys[0]:
            box(ax, ox, y - 0.06, ow, qh + 0.12, '', style='grey')
            text(ax, ox + 0.1, y + qh - 0.02, ex, size=7.5, ha='left', va='top', wrapw=36)
        else:
            box(ax, ox, y + 0.12, ow, qh - 0.24, ex, style='grey', size=7.5, wrapw=36)
        arrow(ax, (qx + qw + 0.02, y + qh / 2), (ox - 0.02, y + qh / 2))
        text(ax, (qx + qw + ox) / 2, y + qh / 2 + 0.08, 'no', size=7, color=GREY, italic=True)
    for y0, y1 in zip(ys[:-1], ys[1:]):
        arrow(ax, (qx + 0.3, y0 - 0.01), (qx + 0.3, y1 + qh + 0.01))
        text(ax, qx + 0.38, (y0 + y1 + qh) / 2, 'yes', size=7, color=GREY, italic=True, ha='left')
    yp = 0.12
    arrow(ax, (qx + 0.3, ys[-1] - 0.01), (qx + 0.3, yp + 0.72 + 0.01))
    text(ax, qx + 0.38, (ys[-1] + yp + 0.72) / 2, 'yes', size=7, color=GREY, italic=True, ha='left')
    box(ax, qx, yp, qw, 0.72, 'Unblind this case only; on placebo, generally not reported as a SUSAR. '
        'US IND: 15 days, or 7 days if fatal or life-threatening.', style='accent', size=7.5,
        title='Potential SUSAR', align='left', wrapw=56)
    # path of the worked case
    ax.add_patch(FancyBboxPatch((ox - 0.05, ys[0] - 0.11), ow + 0.1, qh + 0.22, boxstyle='round,pad=0,rounding_size=0.06',
                                fc='none', ec=RUST, lw=1.4, zorder=5))
    text(ax, ox + 0.1, ys[0] + 0.02, 'Participant 114-0087: nonserious; QT prolonged is also listed '
         'in the RSI.', size=7, color=RUST, italic=True, ha='left', va='bottom', wrapw=40)
    save(fig, 'fig21_3')


def fig21_4():
    """Restart timing after clarithromycin for participant 114-0087 (Calculation 21.2)."""
    D = lambda m, d: dt.date(2026, m, d)
    fig, ax = chart(2.5)
    rows = [('Ravolixan elimination,\nusual half-life', D(3, 10), D(3, 13), TEAL_MID, '5 × 14 h ≈ 70 h'),
            ('Ravolixan elimination,\nupper bound with inhibition', D(3, 10), D(3, 21), RULE, '5 × about 55 h: up to about 11 days'),
            ('CYP3A4 recovery after\nlast clarithromycin dose', D(3, 10), D(3, 24), RUST, 'about 14 days (Calculation 21.1)')]
    ys = [2, 1, 0]
    for (lab, a, b, c, note_), y in zip(rows, ys):
        ax.barh(y, (b - a).days, left=mdates.date2num(a), color=c, height=0.5)
        xt = mdates.date2num(b) + 0.3 if (b - a).days < 5 else mdates.date2num(a) + 0.3
        ax.text(xt, y, note_, ha='left', va='center', fontsize=7.5, color='white' if c == RUST else INK)
    ax.axvline(mdates.date2num(D(3, 24)), color=INK, lw=1.0, ls=(0, (3, 2)))
    ax.text(mdates.date2num(D(3, 24)) + 0.3, 2.45, 'Restart 24 Mar', ha='left', va='center', fontsize=7.5,
            color=INK, fontweight='bold')
    ax.plot([mdates.date2num(D(3, 27))], [0.0], 'D', color=TEAL, ms=5)
    ax.text(mdates.date2num(D(3, 27)), 0.3, 'ECG near Tmax,\nday 3–4 after restart', ha='center', va='bottom',
            fontsize=7, color=TEAL)
    ax.set_yticks(ys, [r[0] for r in rows], fontsize=7.5)
    ax.set_xlim(mdates.date2num(D(3, 9)), mdates.date2num(D(3, 31)))
    ax.set_ylim(-0.45, 2.7)
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[10, 17, 24, 31]))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: f'{mdates.num2date(v).day} {mdates.num2date(v):%b}'))
    ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    ax.set_xlabel('From the last doses on 10 March', fontsize=8)
    fig.tight_layout()
    save(fig, 'fig21_4')


if __name__ == '__main__':
    fig21_1(); fig21_2(); fig21_3(); fig21_4(); fig21_5()
