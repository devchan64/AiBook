"""Render P3-8.2 from the existing P3-4.1 fictional log; no copied dataset.

Run from any directory: python path/to/p3_8_2_boxplot.py
Quartiles use medians of the lower/upper halves; whiskers use min/max.
"""
from pathlib import Path
import csv
from statistics import median
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'chapter-04' / 'p3_4_1_measurement_log.csv'

def load_groups():
    with SOURCE.open(newline='') as handle:
        rows = [r for r in csv.DictReader(handle) if r['elapsed_seconds'] == '2']
    assert len(rows) == len({r['event_id'] for r in rows}) == 12
    return [[float(r['flow']) for r in rows if r['is_recent'] == flag] for flag in ('0', '1')]

def summary(values):
    values = sorted(values)
    half = len(values) // 2
    return dict(med=median(values), q1=median(values[:half]),
                q3=median(values[-half:]), whislo=min(values),
                whishi=max(values), fliers=[])

def main():
    groups = load_groups()
    plt.rcParams.update({'font.size': 14, 'svg.fonttype': 'none', 'svg.hashsalt': 'p3-8-2'})
    fig, ax = plt.subplots(figsize=(7.6, 4.8), layout='constrained')
    boxes = ax.bxp([summary(v) for v in groups], positions=[1, 2],
                   widths=.4, showfliers=False, patch_artist=True,
                   medianprops={'color': '#111111', 'linewidth': 2})
    for patch, color in zip(boxes['boxes'], ['#d4e6f5', '#f9d9be']):
        patch.set_facecolor(color)
    offsets = [-.10, -.06, -.02, .02, .06, .10]
    for i, values in enumerate(groups, 1):
        ax.scatter([i+x for x in offsets], sorted(values), s=32,
                   color='#1d425a', zorder=3)
    ax.set_xticks([1, 2], ['Reference (n=6)', 'Recent (n=6)'])
    ax.set_ylabel('Flow at t = 2 s (L/min)')
    ax.set_ylim(0, 2.1)
    ax.set_yticks([0, .5, 1, 1.5, 2])
    ax.grid(axis='y', alpha=.25)
    ax.set_axisbelow(True)
    ax.spines[['top', 'right']].set_visible(False)
    fig.savefig(HERE / 'p3-8-2-boxplot.svg', metadata={'Date': None})
    fig.savefig('/tmp/p3-8-2-boxplot.png', dpi=140)
    plt.close(fig)
    p = HERE / 'p3-8-2-boxplot.svg'
    s = p.read_text()
    end = s.index('>', s.index('<svg')) + 1
    s = s[:end] + '\n<title>Flow at two seconds: reference and recent operations</title>\n<desc>Fictional data, six distinct operations per group. Medians 1.05 and 1.65 L/min; boxes from 1.00 to 1.10 and 1.50 to 1.80. Dots show all values; whiskers show minimum and maximum.</desc>' + s[end:]
    p.write_text("\n".join(line.rstrip() for line in s.splitlines()) + "\n")

if __name__ == '__main__':
    main()
