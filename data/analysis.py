"""Did Detectorists change metal detecting in Britain?

Interrupted time series on monthly data, 2004-2026:
  - Google Trends (UK): "metal detecting", "metal detector", "detectorists" (0-100 index)
  - Portable Antiquities Scheme: records created per month, metal-detector records created,
    and records by date of discovery.
Model: log(y) ~ linear trend + calendar-month dummies + level shift after each broadcast
       + Covid lockdown dummies. HAC (Newey-West) standard errors.
Placebo: the same model with one fake break at every month 2006-2023 that is at least
         12 months from a real broadcast, to see how unusual the real step is.
"""
import json
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

AIR = {  # first broadcast month of each run
    'S1 (BBC Four)': '2014-10', 'S2 (BBC Four)': '2015-10',
    'S3 (BBC Four)': '2017-11', 'Special (BBC Two)': '2022-12',
}
LOCKDOWN = ['2020-04', '2020-05', '2020-11', '2021-01', '2021-02', '2021-03']

gt = pd.read_csv('google_trends_gb.csv')
pas = pd.read_csv('pas_monthly.csv')
df = gt.merge(pas, on='month', how='outer').sort_values('month').reset_index(drop=True)
df['t'] = np.arange(len(df))
df['cal'] = df['month'].str[5:7]
df['lockdown'] = df['month'].isin(LOCKDOWN).astype(int)
df['covid'] = ((df['month'] >= '2020-04') & (df['month'] <= '2021-12')).astype(int)  # recording disrupted
df['bulk'] = df['month'].isin(['2007-03', '2010-03', '2015-01']).astype(int)  # one-off bulk uploads
df['post14'] = (df['month'] >= '2014-10').astype(int)
df['post17'] = (df['month'] >= '2017-11').astype(int)
df['post22'] = (df['month'] >= '2022-12').astype(int)
df['on_air'] = df['month'].isin(['2014-10', '2014-11', '2015-10', '2015-11', '2015-12',
                                 '2017-11', '2017-12', '2022-12', '2023-01']).astype(int)

SERIES = {
    'metal_detector': 'Searches: "metal detector"',
    'metal_detecting': 'Searches: "metal detecting"',
    'created': 'PAS records created',
    'created_md': 'PAS records created, metal-detector finds',
    'discovered': 'PAS records by date found',
}

def fit(d, y, breaks, extra=''):
    ctrl = 'lockdown' if y.startswith('metal') else 'covid + bulk'
    f = f'np.log({y}) ~ t + C(cal) + {ctrl} + ' + ' + '.join(breaks) + extra
    return smf.ols(f, d).fit(cov_type='HAC', cov_kwds={'maxlags': 6})

out = {}
for y, label in SERIES.items():
    d = df[(df[y] > 0) & (df['month'] >= '2004-01') & (df['month'] <= '2026-09')].copy()
    if y in ('created', 'created_md'):
        d = d[d['month'] >= '2005-01']          # database growth phase before 2005
    if y == 'discovered':
        d = d[(d['month'] >= '2005-01') & (d['month'] <= '2019-12')]  # later finds still being recorded
    brks = ['post14', 'post17', 'post22'] if y != 'discovered' else ['post14', 'post17']
    m = fit(d, y, brks, ' + on_air')
    res = {k: {'pct': round(100 * (np.exp(m.params[k]) - 1), 1),
               'lo': round(100 * (np.exp(m.conf_int().loc[k, 0]) - 1), 1),
               'hi': round(100 * (np.exp(m.conf_int().loc[k, 1]) - 1), 1),
               'p': round(float(m.pvalues[k]), 4)} for k in ['post14', 'post17', 'post22', 'on_air'] if k in m.params}
    # placebo: single fake break, compare with the real 2014 step in the same single-break model
    real = fit(d, y, ['post14']).params['post14']
    fakes = []
    for mo in d['month']:
        if not ('2006-01' <= mo <= '2023-12'): continue
        yy, mm = int(mo[:4]), int(mo[5:])
        far = all(abs((yy * 12 + mm) - (int(a[:4]) * 12 + int(a[5:]))) >= 12 for a in AIR.values())
        if not far: continue
        dd = d.copy(); dd['fake'] = (dd['month'] >= mo).astype(int)
        fakes.append(fit(dd, y, ['fake']).params['fake'])
    fakes = np.array(fakes)
    res['placebo'] = {'real_single_break_pct': round(100 * (np.exp(real) - 1), 1),
                      'share_fakes_as_big': round(float(np.mean(np.abs(fakes) >= abs(real))), 3),
                      'n_fakes': int(len(fakes))}
    res['n'] = int(m.nobs); res['label'] = label
    out[y] = res

# simple before/after means for the write-up (12 months either side of series 1)
def win(col, a, b):
    s = df[(df['month'] >= a) & (df['month'] <= b)][col]
    return round(float(s.mean()), 1)
out['windows'] = {c: {'before_S1': win(c, '2013-10', '2014-09'), 'after_S1': win(c, '2014-12', '2015-09'),
                      '2016': win(c, '2016-01', '2016-12'), '2019': win(c, '2019-01', '2019-12'),
                      '2024': win(c, '2024-01', '2024-12')}
                  for c in ['metal_detector', 'metal_detecting', 'detectorists', 'created', 'created_md', 'discovered']}
json.dump(out, open('results.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
