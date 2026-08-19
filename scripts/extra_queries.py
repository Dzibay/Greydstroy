# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

files = [
    r'c:\Users\user\Downloads\wordstat_top_queries.xlsx',
    r'c:\Users\user\Downloads\wordstat_top_queries (1).xlsx',
    r'c:\Users\user\Downloads\wordstat_top_queries (2).xlsx',
    r'c:\Users\user\Downloads\wordstat_top_queries (3).xlsx',
]
rows = []
for f in files:
    df = pd.read_excel(f, sheet_name=0).iloc[:, :2]
    df.columns = ['query', 'freq']
    rows.append(df)
d = pd.concat(rows)
d['q'] = d['query'].astype(str).str.lower()
d['freq'] = pd.to_numeric(d['freq'], errors='coerce').fillna(0).astype(int)
d = d.groupby('q', as_index=False).agg({'freq': 'max', 'query': 'first'})

for kw in ['гибк', 'сварк', 'листогиб', 'металлообработ', 'дзержинск', 'област', 'услуг', 'склад', 'анг', 'навес', 'ворот']:
    s = d[d['q'].str.contains(kw, na=False)].sort_values('freq', ascending=False).head(12)
    print(f'\n=== {kw} ===')
    for _, r in s.iterrows():
        print(f"  {r['freq']:>6}  {r['query']}")
