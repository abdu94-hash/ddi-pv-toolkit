# Figures for Chapter 11.
import datetime as dt
import matplotlib.dates as mdates
from figlib import *


def fig11_2():
    """The relevant window depends on the mechanism and the event (Section 11.4). Schematic."""
    fig, ax = diagram(2.62)
    x0, x1 = 1.55, 5.15            # time axis extent (inches)

    def X(t):                       # t in 0..10 relative time units
        return x0 + (x1 - x0) * t / 10
    rows = [(1.92, 'Toxicity from\ninhibition'), (1.1, 'Failure from\ninduction'), (0.28, 'Unintended\npregnancy')]
    bh = 0.2
    for y, lab in rows:
        text(ax, 0.1, y + 0.25, lab, size=8.5, bold=True, color=TEAL, ha='left')
        ax.plot([x0, x1], [y, y], color=RULE, lw=0.7, zorder=0)

    def window(y, a, b, label):
        ax.add_patch(matplotlib.patches.Rectangle((X(a), y - 0.05), X(b) - X(a), 0.6, fc=RUST_LIGHT, ec='none',
                                                  zorder=0.5))
        text(ax, (X(a) + X(b)) / 2, y + 0.47, label, size=6.8, color=RUST, italic=True)

    def bar(y, a, b, label, color=TEAL_MID):
        ax.add_patch(matplotlib.patches.Rectangle((X(a), y + 0.06), X(b) - X(a), bh, fc=color, ec='none', zorder=2))
        text(ax, X(a) + 0.05, y + 0.06 + bh / 2, label, size=7, color='white', ha='left', bold=True)

    def event(y, t, label):
        ax.plot([X(t)], [y + 0.16], marker='D', color=RUST, ms=5, zorder=3)
        text(ax, X(t) + 0.08, y + 0.16, label, size=7, color=RUST, ha='left')

    # inhibition: window is the days before onset
    y = rows[0][0]
    window(y, 5.6, 7.0, 'days before onset')
    bar(y, 1.5, 7.0, 'inhibitor taken')
    event(y, 7.0, 'toxicity')
    # induction: window starts some days after the inducer and ends when induction has waned
    y = rows[1][0]
    window(y, 2.4, 7.4, 'from some days after start until induction wanes')
    bar(y, 1.0, 5.0, 'inducer taken')
    event(y, 6.4, 'failure')
    # pregnancy: conception window dated backwards from a scan
    y = rows[2][0]
    window(y, 3.4, 5.0, 'conception window')
    ax.plot([X(8.6)], [y + 0.16], marker='o', color=TEAL, ms=5, zorder=3)
    text(ax, X(8.6) + 0.08, y + 0.16, 'dating scan', size=7, color=TEAL, ha='left')
    arrow(ax, (X(8.45), y + 0.16), (X(5.1), y + 0.16), color=TEAL, lw=1.0, ls=(0, (3, 2)))
    text(ax, X(6.8), y + 0.24, 'dated backwards', size=6.8, color=TEAL, italic=True, va='bottom')
    arrow(ax, (x0, 0.08), (x1, 0.08), color=GREY, lw=0.8)
    text(ax, x1, 0.12, 'Time', size=7.5, color=GREY, ha='right', va='bottom')
    save(fig, 'fig11_2')


def D(m, d):
    return dt.date(2025 if m >= 10 else 2026, m, d)


def fig11_4():
    """Worked Case 11.1 medication timeline, Stage 3 (fictional)."""
    fig, ax = chart(3.4)
    fig.subplots_adjust(left=0.2, right=0.97, top=0.97, bottom=0.09)
    lo, hi = D(11, 1), D(4, 5)
    ax.set_xlim(lo, hi)
    ax.set_ylim(-0.85, 4.55)
    ax.spines['left'].set_visible(False)
    ax.set_yticks([])
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', labelsize=7.5)
    # conception window across all rows
    ax.axvspan(D(2, 2), D(2, 16), color=RUST_LIGHT, lw=0, zorder=0)
    ax.axvline(D(2, 9), color=RUST, lw=0.8, ls=(0, (3, 2)), zorder=0.5)
    rows = {'pill': 4.1, 'sjw': 3.0, 'top': 2.0, 'spot': 1.05, 'preg': 0.15}
    labels = {'pill': 'EE/LNG pill', 'sjw': "St John's wort", 'top': 'Topiramate', 'spot': 'Spotting',
              'preg': 'Pregnancy'}
    for k, y in rows.items():
        ax.text(-0.02, y, labels[k], transform=ax.get_yaxis_transform(), ha='right', va='center', fontsize=8)
    h = 0.32

    def bar(a, b, y, color=TEAL_MID, **kw):
        ax.barh(y, (b - a).days, left=a, height=h, color=color, lw=0, **kw)
    # contraceptive
    y = rows['pill']
    bar(lo, D(2, 2), y)
    bar(D(2, 6), hi, y)
    ax.barh(y, 4, left=D(2, 2), height=h, color='white', edgecolor=RUST, hatch='////', lw=0.6)
    for d in (D(11, 10), D(2, 6)):
        ax.plot(d, y + 0.3, marker='v', color=SAND_DARK, ms=5)
    ax.text(D(11, 13), y + 0.32, 'dispensed 10 Nov (3 packs)', fontsize=6.8, color=SAND_DARK, va='center')
    ax.text(D(2, 18), y + 0.32, 'next supply 6 Feb', fontsize=6.8, color=SAND_DARK, va='center')
    ax.text(D(1, 30), y - 0.36, 'possible late pack start, 2–6 Feb (inferred)', fontsize=6.8, color=RUST,
            va='center', ha='right', style='italic')
    # St John's wort
    y = rows['sjw']
    bar(D(12, 25), D(3, 4), y)
    ax.plot([D(3, 4), D(3, 25)], [y, y], color=TEAL_MID, lw=2.5, ls=(0, (2, 1.5)))
    ax.text(D(12, 23), y, 'from about Christmas', fontsize=6.8, color=GREY, ha='right', va='center', style='italic')
    ax.text(D(2, 19), y + 0.24, 'stop: early Mar (patient)\nor after 18 Mar (midwife)', fontsize=6.8, color=GREY,
            ha='left', va='bottom', style='italic')
    # topiramate
    y = rows['top']
    bar(D(1, 12), D(2, 4), y, color=TEAL_MID)
    bar(D(2, 4), hi, y, color=TEAL)
    ax.text(D(1, 10), y, '12 or 14 Jan', fontsize=6.8, color=GREY, ha='right', va='center', style='italic')
    ax.text(D(1, 13), y - 0.33, '25 mg nightly', fontsize=6.8, color=TEAL, va='center')
    ax.text(D(2, 19), y - 0.33, '25 mg twice daily', fontsize=6.8, color=TEAL, va='center')
    # spotting
    y = rows['spot']
    bar(D(1, 1), D(2, 28), y, color=SAND_BORDER)
    ax.text(D(12, 30), y, 'January and February', fontsize=6.8, color=GREY, ha='right', va='center', style='italic')
    # pregnancy anchors
    y = rows['preg']
    ax.text(D(1, 30), y, 'estimated conception, 2–16 Feb', fontsize=6.8, color=RUST, ha='right', va='center')
    ax.plot(D(3, 3), y, marker='o', color=TEAL, ms=5)
    ax.text(D(3, 6), y - 0.2, 'positive test\nearly Mar', fontsize=6.8, color=INK, ha='right', va='top')
    ax.plot(D(3, 18), y, marker='o', color=TEAL, ms=5)
    ax.text(D(3, 15), y - 0.2, 'dating scan\n18 Mar', fontsize=6.8, color=INK, ha='left', va='top')
    save(fig, 'fig11_4')


def fig11_1():
    """Where exposure information goes missing along the medication path (Sections 11.1 and 11.2)."""
    fig, ax = diagram(2.75)
    bw, gap, by, bh = 0.9, 0.17, 1.6, 0.5
    x0 = (TEXT_W - (5 * bw + 4 * gap)) / 2
    xs = [x0 + k * (bw + gap) for k in range(5)]
    layers = ['Prescribed', 'Dispensed', 'Taken', 'Taken as directed', 'Systemic exposure']
    for k, (x, t) in enumerate(zip(xs, layers)):
        box(ax, x, by, bw, bh, t, style='teal' if k in (2, 3) else 'light', size=7.8)
        if k < 4:
            arrow(ax, (x + bw + 0.02, by + bh / 2), (xs[k + 1] - 0.02, by + bh / 2), lw=1.1)
    # brackets above
    def bracket(a, b, label, color):
        y = by + bh + 0.14
        ax.plot([a, a, b, b], [y, y + 0.08, y + 0.08, y], color=color, lw=0.9)
        text(ax, (a + b) / 2, y + 0.2, label, size=7.2, color=color, italic=True, va='bottom')
    bracket(xs[0], xs[1] + bw, 'what most reports supply', GREY)
    bracket(xs[2], xs[3] + bw, 'what an interaction assessment needs', TEAL)
    text(ax, xs[4] + bw / 2, by + bh + 0.22, 'seldom\nmeasured', size=7, color=GREY, italic=True, va='bottom')
    # where information goes missing
    lw_, lh, ly = 1.22, 0.86, 0.12
    lx = [(TEXT_W - (4 * lw_ + 3 * 0.1)) / 2 + k * (lw_ + 0.1) for k in range(4)]
    leaks = [(0, 'Stopped drugs', 'Recent discontinuations drop off every list, yet can matter as much as starts.'),
             (1, 'Other sources', 'Other prescribers, other pharmacies, samples.'),
             (2, 'Enter unrecorded', 'Nonprescription, herbal and supplement products, often not mentioned [2].'),
             (3, 'Use and adherence', 'As-needed doses, missed or late doses, vomiting or diarrhea.')]
    for k, (target, t, s) in enumerate(leaks):
        box(ax, lx[k], ly, lw_, lh, s, style='rust', size=6.8, title=t, align='left')
        tx = xs[target] + bw / 2
        arrow(ax, (lx[k] + lw_ / 2, ly + lh + 0.03), (tx, by - 0.04), color=RUST, lw=0.9, ls=(0, (3, 2)))
    save(fig, 'fig11_1')


def fig11_3():
    """Worked Case 11.1: what each stage of information changed (Section 11.6)."""
    fig, ax = diagram(3.4)
    lx, lw_ = 0.06, 0.98
    cw, gap = 1.32, 0.05
    cx = [lx + lw_ + 0.06 + k * (cw + gap) for k in range(3)]
    heads = ['Stage 1: report\n23 Mar', 'Stage 2: patient call\n27 Mar', 'Stage 3: GP and pharmacy\n14 Apr']
    for x, h in zip(cx, heads):
        text(ax, x + cw / 2, 3.18, h, size=7.5, bold=True, color=TEAL)
    rows = [
        ('Event window', [('No dates', 'grey'), ('Conception about 2–16 Feb', 'light'), ('Unchanged', 'white')]),
        ("St John's wort", [('Not reported ("no other medicines")', 'grey'), ('Since about Christmas; product unknown', 'rust'),
                            ('Still taken at 18 Mar (midwife)', 'rust')]),
        ('Migraine drug', [('Not reported', 'grey'), ('"A new tablet"; name unknown', 'grey'),
                           ('Topiramate 25–50 mg: unlikely contributor', 'light')]),
        ('Adherence', [('"Takes the pill every day"', 'grey'), ('"No missed pills" (patient)', 'grey'),
                       ('Possible late pack start, 2–6 Feb', 'rust')]),
        ('Assessment', [('Exposure not yet characterized', 'sand'), ('Plausible inducer; second candidate', 'sand'),
                        ('Possible contributor; competing explanation', 'sand')]),
    ]
    rh, rg = 0.46, 0.07
    y = 2.88
    for lab, cells in rows:
        y -= rh
        text(ax, lx, y + rh / 2, lab, size=8, bold=True, color=TEAL, ha='left')
        for x, (t, st) in zip(cx, cells):
            box(ax, x, y, cw, rh, t, style=st, size=7, radius=0.04, lw=0.7)
        y -= rg
    note(ax, 'Grey: unknown or untested.  Teal: resolved.  Rust: raises the interaction or a competing cause.  Sand: judgment.',
         y=0.06, size=6.5)
    save(fig, 'fig11_3')


if __name__ == '__main__':
    fig11_1(); fig11_2(); fig11_3(); fig11_4()
