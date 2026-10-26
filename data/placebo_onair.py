"""Placebo for the 'on air' months: refit with the same calendar months in years with no broadcast."""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
exec(open('analysis.py').read().split("SERIES = {")[0])  # reuse data prep
REAL = ['2014-10','2014-11','2015-10','2015-11','2015-12','2017-11','2017-12','2022-12','2023-01']
def fit_onair(d, y, months):
    d = d.copy(); d['fake'] = d['month'].isin(months).astype(int)
    ctrl = 'lockdown' if y.startswith('metal') else 'covid + bulk'
    return smf.ols(f'np.log({y}) ~ t + C(cal) + {ctrl} + fake', d).fit().params['fake']
res = {}
for y, lo, hi in [('metal_detecting','2004-01','2026-09'),('metal_detector','2004-01','2026-09'),('created','2005-01','2026-09'),('created_md','2005-01','2026-09'),('discovered','2005-01','2019-12')]:
    d = df[(df['month'] >= lo) & (df['month'] <= hi) & (df[y] > 0)]
    real = fit_onair(d, y, [m for m in REAL if m <= hi])
    fakes = []
    for shift in range(-9, 10):
        if shift in (0,): continue
        months = []
        for m in REAL:
            yy = int(m[:4]) + shift
            mm = f'{yy}-{m[5:]}'
            months.append(mm)
        if any(m in REAL for m in months): continue
        months = [m for m in months if lo <= m <= hi]
        if len(months) < 4: continue
        fakes.append(fit_onair(d, y, months))
    fakes = np.array(fakes)
    res[y] = {'real_pct': round(100*(np.exp(real)-1),1), 'fakes_pct': [round(100*(np.exp(f)-1),1) for f in fakes],
              'share_fakes_as_big': round(float(np.mean(fakes >= real)),2)}
json.dump(res, open('placebo_onair.json','w'), indent=1); print(json.dumps(res, indent=1))
