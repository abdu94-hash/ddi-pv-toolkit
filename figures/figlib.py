# Shared look for every figure in the book: palette, fonts, sizes, and small
# drawing helpers. Figure scripts (figures/partN.py) import this and call save().
# Diagram axes use inch coordinates (0..w across, 0..h up) so layouts are exact.
import os, textwrap
import matplotlib, matplotlib.ticker
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)

# Same palette as build.js
INK, TEAL, TEAL_LIGHT, TEAL_MID = '#1F2A30', '#0E5C63', '#E6F1F1', '#7FAFB3'
SAND, SAND_BORDER, SAND_DARK = '#F6F1E7', '#C9B88F', '#7A5C1E'
RUST, RUST_LIGHT, GREY, RULE = '#9A3412', '#F7E3D9', '#5B6770', '#B7C7C9'
# Data series, in order of use (teal, rust, sand-dark, grey, mid-teal)
SERIES = [TEAL, RUST, SAND_DARK, GREY, TEAL_MID]

TEXT_W = 5.3  # printable width of the 7 x 10 in page, inches

plt.rcParams.update({
    'font.family': ['Calibri', 'DejaVu Sans'], 'font.size': 9, 'text.color': INK,
    'axes.edgecolor': GREY, 'axes.labelcolor': INK, 'axes.linewidth': 0.7,
    'axes.titlesize': 10, 'axes.titleweight': 'bold', 'axes.titlecolor': INK,
    'xtick.color': GREY, 'ytick.color': GREY, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
    'xtick.labelcolor': INK, 'ytick.labelcolor': INK,
    'legend.fontsize': 8, 'legend.frameon': False, 'lines.linewidth': 1.8,
    'savefig.dpi': 300, 'figure.dpi': 100,
})

STYLES = {  # fill, edge, text colour, bold
    'teal':   (TEAL, TEAL, 'white', True),
    'light':  (TEAL_LIGHT, TEAL, INK, False),
    'sand':   (SAND, SAND_BORDER, INK, False),
    'white':  ('white', RULE, INK, False),
    'rust':   (RUST_LIGHT, RUST, INK, False),
    'accent': (RUST, RUST, 'white', True),
    'grey':   ('#EEF1F2', GREY, INK, False),
}


def diagram(h, w=TEXT_W):
    """Blank canvas in inch units for box-and-arrow figures."""
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis('off')
    return fig, ax


def chart(h, w=TEXT_W, ncols=1, nrows=1, **kw):
    """Data chart(s) with light spines; returns fig and axes."""
    fig, axes = plt.subplots(nrows, ncols, figsize=(w, h), **kw)
    for a in (axes.flat if hasattr(axes, 'flat') else [axes]):
        a.spines[['top', 'right']].set_visible(False)
        a.tick_params(length=3, width=0.6)
    return fig, axes


def wrap(text, width):
    return '\n'.join('\n'.join(textwrap.wrap(p, width)) if p else '' for p in text.split('\n'))


def box(ax, x, y, w, h, text='', style='light', size=8.5, wrapw=None, bold=None, align='center', pad=0.06, radius=0.06, lw=0.9, title=None):
    """Rounded box with (x, y) its lower-left corner. Text wraps to fit if wrapw is
    not given. Optional title is drawn bold at the top and text below it."""
    fill, edge, tc, b = STYLES[style]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={radius}',
                                fc=fill, ec=edge, lw=lw, zorder=2))
    if wrapw is None:
        wrapw = max(8, int(w * 72 / (size * 0.52)) - 1)
    weight = 'bold' if (b if bold is None else bold) else 'normal'
    ha = {'center': 'center', 'left': 'left'}[align]
    tx = x + w / 2 if align == 'center' else x + pad + 0.04
    if title:
        t = wrap(title, wrapw)
        top = y + h - pad - 0.02
        ax.text(tx, top, t, ha=ha, va='top', fontsize=size + 0.5, fontweight='bold', zorder=3,
                color=tc if style in ('teal', 'accent') else (RUST if style == 'rust' else TEAL))
        if text:
            below = top - (t.count('\n') + 1) * (size + 0.5) * 1.3 / 72 - 0.04
            ax.text(tx, below, wrap(text, wrapw), ha=ha, va='top', fontsize=size, color=tc,
                    zorder=3, linespacing=1.25)
    elif text:
        ax.text(tx, y + h / 2, wrap(text, wrapw), ha=ha, va='center', fontsize=size, color=tc,
                fontweight=weight, zorder=3, linespacing=1.25)
    return (x, y, w, h)


def arrow(ax, p, q, color=GREY, lw=1.1, style='-|>', ls='-', rad=0.0, head=7):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=head, color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f'arc3,rad={rad}', zorder=1,
                                 shrinkA=0, shrinkB=0))


def text(ax, x, y, s, size=8.5, color=INK, ha='center', va='center', bold=False, italic=False, wrapw=None, **kw):
    ax.text(x, y, wrap(s, wrapw) if wrapw else s, ha=ha, va=va, fontsize=size, color=color,
            fontweight='bold' if bold else 'normal', fontstyle='italic' if italic else 'normal',
            zorder=4, linespacing=1.25, **kw)


def note(ax, s, x=None, y=0.08, size=7, w=TEXT_W):
    """Small grey footnote line along the bottom of a diagram."""
    text(ax, x if x is not None else w / 2, y, s, size=size, color=GREY, italic=True)


def save(fig, name):
    path = os.path.join(OUT, f'{name}.png')
    fig.savefig(path, dpi=300, facecolor='white')
    plt.close(fig)
    return path
