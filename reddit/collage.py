import json, os
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'data')
F = '/tmp/claude-0/-home-claude/c232619d-81e0-53f3-9de6-41e973630753/scratchpad/fonts/'
for f in ['FrauncesVar.ttf', 'IBMPlexMono-Regular.ttf', 'IBMPlexMono-Medium.ttf', 'SourceSerif4-Regular.ttf', 'SourceSerif4-Semibold.ttf', 'SourceSerif4-It.ttf']:
    fm.fontManager.addfont(F + f)
DISP = fm.FontProperties(fname=F + 'FrauncesVar.ttf', weight=900)
SER = 'Source Serif 4'; MONO = 'IBM Plex Mono'

BG = '#E7EDDC'; FG = '#1C1F17'; MUT = '#5F6656'; GRID = '#CFD8C2'
BAND = '#E3AE3A'; GREEN = '#3D6B35'; RUST = '#B4461E'; INDIGO = '#57478A'; BLUE = '#27445E'; LBLUE = '#86A7C2'

g = pd.read_csv(os.path.join(D, 'google_trends_gb.csv')); g['d'] = pd.to_datetime(g.month)
p = pd.read_csv(os.path.join(D, 'pas_monthly.csv')); p['d'] = pd.to_datetime(p.month)
R = json.load(open(os.path.join(D, 'results.json')))
PL = json.load(open(os.path.join(D, 'placebo_onair.json')))
W = R['windows']

# broadcast months, as used in analysis.py
AIR = [('Series 1', 'BBC Four, Oct 2014', '2014-10-01', '2014-12-01'), ('Series 2', 'BBC Four, Oct 2015', '2015-10-01', '2016-01-01'),
       ('Series 3', 'BBC Four, Nov 2017', '2017-11-01', '2018-01-01'), ('Special', 'BBC Two, Dec 2022', '2022-12-01', '2023-02-01')]
X0, X1 = pd.Timestamp('2004-01-01'), pd.Timestamp('2026-11-01')

def style(a):
    a.set_facecolor(BG)
    for s in ['top', 'right', 'left']: a.spines[s].set_visible(False)
    a.spines['bottom'].set_color(MUT)
    a.tick_params(colors=MUT, labelsize=10.5, length=0)
    a.grid(axis='y', color=GRID, lw=0.8); a.set_axisbelow(True)
    for t in a.get_xticklabels() + a.get_yticklabels(): t.set_family(MONO)

def bands(a):
    for _, _, s, e in AIR:
        a.axvspan(pd.Timestamp(s), pd.Timestamp(e), color=BAND, alpha=0.5, lw=0, zorder=0)

fig = plt.figure(figsize=(12, 15), dpi=200, facecolor=BG)
fig.text(0.04, 0.968, 'Did Detectorists start a boom?', fontproperties=DISP, fontsize=48, color=FG, va='top')
fig.text(0.04, 0.914, 'The BBC comedy is often credited with getting Britain out metal detecting. Twenty-two years of UK\n'
         'Google searches and the finds register say: a burst every time it aired, but no lasting boom.',
         family=SER, fontsize=15, color=FG, va='top', linespacing=1.35)

# ---------------- panel A: searches
a = fig.add_axes([0.06, 0.615, 0.9, 0.205]); style(a); bands(a)
for col, c, lab, lw in [('detectorists', INDIGO, '"detectorists"', 1.3), ('metal_detector', RUST, '"metal detector"', 1.6), ('metal_detecting', GREEN, '"metal detecting"', 2.0)]:
    a.plot(g.d, g[col], color=c, lw=lw, label=lab, solid_joinstyle='round')
a.set_xlim(X0, X1); a.set_ylim(0, 102); a.set_yticks([0, 25, 50, 75, 100])
a.xaxis.set_major_locator(mdates.YearLocator(2)); a.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
for t in a.get_xticklabels() + a.get_yticklabels(): t.set_family(MONO)
fig.text(0.04, 0.845, 'UK GOOGLE SEARCHES  monthly, 100 = busiest month for any of the three terms', family=MONO, fontsize=11, color=MUT)
lg = a.legend(loc='upper left', frameon=False, prop={'family': MONO, 'size': 11}, handlelength=1.6, bbox_to_anchor=(0.0, 1.0))
for (name, sub, s, e), ha in zip(AIR, ['right', 'center', 'center', 'center']):
    xm = pd.Timestamp(s) + (pd.Timestamp(e) - pd.Timestamp(s)) / 2
    a.text(xm, 104, name, family=MONO, fontsize=10, color=FG, ha=ha, va='bottom')
a.annotate('lockdown\n2020', (pd.Timestamp('2020-05-01'), g.set_index('month').loc['2020-05', 'metal_detector']), (pd.Timestamp('2019-03-01'), 62),
           family=MONO, fontsize=10, color=RUST, ha='center', arrowprops=dict(arrowstyle='-', color=RUST, lw=0.8))

# ---------------- panel B: PAS records
b = fig.add_axes([0.06, 0.39, 0.9, 0.175]); style(b); bands(b)
b.axvspan(pd.Timestamp('2020-04-01'), pd.Timestamp('2022-01-01'), color='#C6CEB8', alpha=0.75, lw=0, zorder=0)
b.text(pd.Timestamp('2021-02-15'), 7550, 'Covid', family=MONO, fontsize=10, color=MUT, ha='center', va='top')
pp = p[p.d >= '2005-01-01']
b.plot(pp.d, pp.created, color=BLUE, lw=1.7, label='all records created')
b.plot(pp.d, pp.created_md, color=LBLUE, lw=1.3, label='metal-detector finds')
b.set_xlim(X0, X1); b.set_ylim(0, 8000); b.set_yticks([0, 2000, 4000, 6000, 8000]); b.set_yticklabels(['0', '2k', '4k', '6k', '8k'])
b.xaxis.set_major_locator(mdates.YearLocator(2)); b.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
for t in b.get_xticklabels() + b.get_yticklabels(): t.set_family(MONO)
for m in ['2007-03', '2010-03', '2015-01']:
    v = int(p.set_index('month').loc[m, 'created'])
    if v > 8000:
        b.text(pd.Timestamp(m + '-01') + pd.Timedelta(days=60), 7700, f'bulk upload\n{v:,}', family=MONO, fontsize=9.5, color=MUT,
               ha='left', va='top', zorder=5, bbox=dict(facecolor=BG, edgecolor='none', pad=1.5))
b.legend(loc='lower left', frameon=False, prop={'family': MONO, 'size': 11}, handlelength=1.6, ncol=2)
fig.text(0.04, 0.578, 'PORTABLE ANTIQUITIES SCHEME  finds recorded per month, England and Wales', family=MONO, fontsize=11, color=MUT)
fig.text(0.04, 0.358, 'Yellow bands: the months each series was on air. Series 1, 2 and 3 on BBC Four; the special on BBC Two.',
         family=SER, fontsize=12, color=FG, style='italic')

# ---------------- headline numbers
tot = [(f"+{PL['metal_detecting']['real_pct']:.0f}%", 'searches for "metal detecting"\nin on-air months, against the\nsame months in other years'),
       (f"+{PL['created']['real_pct']:.0f}%", 'finds recorded in the same\nbroadcast months'),
       (f"+{PL['discovered']['real_pct']:.0f}%", 'objects actually dug up in\nthose months, by date found:\nwithin normal variation'),
       ('No step', 'no lasting rise in searches\nor recorded finds after any\nseries, against placebo breaks')]
for i, (big, small) in enumerate(tot):
    x = 0.04 + i * 0.235
    # Source Serif 4 Semibold: its plus and figures sit together cleanly (Fraunces' curled 4 collides with the plus)
    fig.text(x, 0.337, big, family=SER, weight='semibold', fontsize=42, color=RUST, va='top')
    fig.text(x, 0.283, small, family=SER, fontsize=12.5, color=FG, va='top', linespacing=1.28)

# ---------------- bottom: placebo strips and the later boom
def placebo(ax, key, title, col):
    style(ax); ax.grid(False); ax.spines['bottom'].set_visible(False)
    fk = PL[key]['fakes_pct']; real = PL[key]['real_pct']
    ax.plot([0, 0], [-0.22, 0.22], color=MUT, lw=0.8)
    ax.scatter(fk, [0] * len(fk), s=70, facecolor='none', edgecolor=MUT, lw=1.3, zorder=3)
    ax.scatter([real], [0], s=130, color=col, zorder=4)
    ax.text(real, 0.32, f'real  +{real:.0f}%', family=MONO, fontsize=10.5, color=col, ha='center', va='bottom')
    ax.text(-28, -0.36, f'{len(fk)} fake broadcast years', family=MONO, fontsize=10, color=MUT, ha='left', va='top')
    ax.set_ylim(-0.8, 0.8); ax.set_yticks([]); ax.set_xlim(-30, 50)
    ax.set_xticks([-20, 0, 20, 40]); ax.set_xticklabels(['-20%', '0', '+20%', '+40%'], family=MONO)
    ax.set_title(title, family=MONO, fontsize=11, color=MUT, loc='left', pad=6)

c1 = fig.add_axes([0.05, 0.1, 0.27, 0.08]); placebo(c1, 'metal_detecting', 'TEST: "metal detecting"', GREEN)
c2 = fig.add_axes([0.37, 0.1, 0.27, 0.08]); placebo(c2, 'created', 'TEST: finds recorded', BLUE)
fig.text(0.05, 0.208, 'Is the on-air bump real? Refit with the broadcast months moved to other years.',
         family=SER, fontsize=12, color=FG, style='italic')

c3 = fig.add_axes([0.73, 0.1, 0.24, 0.075]); style(c3)
g['y'] = g.d.dt.year; yr = g[g.y <= 2025].groupby('y')[['metal_detector', 'metal_detecting']].mean()
c3.plot(yr.index, yr.metal_detector, color=RUST, lw=2.2); c3.plot(yr.index, yr.metal_detecting, color=GREEN, lw=2.2)
c3.set_xlim(2004, 2025); c3.set_ylim(0, 30); c3.set_yticks([0, 10, 20, 30])
c3.set_xticks([2004, 2014, 2025]); c3.set_xticklabels(['2004', '2014', '2025'], family=MONO)
c3.text(2020, 27.5, '2020', family=MONO, fontsize=10, color=RUST, ha='center')
c3.set_title('THE REAL BOOM CAME LATER\nyearly mean of searches', family=MONO, fontsize=11, color=MUT, loc='left', pad=6, linespacing=1.3)
c3.text(2004.5, 22.5, '"metal detector"', family=MONO, fontsize=10, color=RUST)
c3.text(2006, 1.5, '"metal detecting"', family=MONO, fontsize=10, color=GREEN)

fig.text(0.04, 0.016, 'Data: Google Trends, United Kingdom, web search, January 2004 to October 2026, retrieved October 2026. Portable Antiquities\n'
         'Scheme database (British Museum, finds.org.uk), records per month, retrieved October 2026. Models: log scale, trend, calendar\n'
         'month, Covid terms, Newey-West errors. Recording depends on finds officers\' capacity, not only on detecting.\n'
         'Analysis and chart: Tristan Hotham, with Python and matplotlib.',
         family=MONO, fontsize=9, color=MUT, linespacing=1.45)
fig.savefig(os.path.join(HERE, 'detectorists_effect.png'), facecolor=BG, dpi=200)
print('ok')
