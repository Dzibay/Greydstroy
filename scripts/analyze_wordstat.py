# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

files = [
    (r'c:\Users\user\Downloads\wordstat_top_queries.xlsx', 'лазерная резка металла'),
    (r'c:\Users\user\Downloads\wordstat_top_queries (1).xlsx', 'плазменная резка металла'),
    (r'c:\Users\user\Downloads\wordstat_top_queries (2).xlsx', 'лазерная резка металла'),  # broader laser cutting
    (r'c:\Users\user\Downloads\wordstat_top_queries (3).xlsx', 'металлоконструкции'),
]

all_rows = []
for path, seed in files:
    if not os.path.exists(path):
        print(f'MISSING: {path}')
        continue
    df = pd.read_excel(path, sheet_name=0)
    # columns: query, frequency, seed_keyword
    df = df.iloc[:, :2].copy()
    df.columns = ['query', 'freq']
    df['seed'] = seed
    df['source'] = os.path.basename(path)
    all_rows.append(df)
    print(f'\n=== {os.path.basename(path)} | seed: {seed} ===')
    print(f'Rows: {len(df)}')
    print(df.head(15).to_string(index=False))

combined = pd.concat(all_rows, ignore_index=True)
combined['query_norm'] = combined['query'].astype(str).str.strip().str.lower()
combined['freq'] = pd.to_numeric(combined['freq'], errors='coerce').fillna(0).astype(int)

# dedupe: max freq per query, keep seeds
deduped = combined.groupby('query_norm', as_index=False).agg({
    'freq': 'max',
    'query': 'first',
    'seed': lambda x: ', '.join(sorted(set(x))),
})

deduped = deduped.sort_values('freq', ascending=False)
print(f'\n\n=== SUMMARY ===')
print(f'Total raw rows: {len(combined)}')
print(f'Unique queries: {len(deduped)}')
print(f'Total frequency (deduped sum): {deduped["freq"].sum():,}')

print('\n=== TOP 80 QUERIES ===')
for _, r in deduped.head(80).iterrows():
    print(f"{r['freq']:>8}  [{r['seed'][:20]}]  {r['query']}")

# Intent classification
def classify(q):
    q = q.lower()
    tags = []
    if any(w in q for w in ['лазер', 'laser']): tags.append('laser')
    if any(w in q for w in ['плазм', 'plasma']): tags.append('plasma')
    if any(w in q for w in ['гибк', 'листогиб', 'гнут', 'гибочн']): tags.append('bend')
    if any(w in q for w in ['сварк', 'сварить', 'сварщик']): tags.append('weld')
    if any(w in q for w in ['металлоконструк', 'мк ', 'каркас', 'ферм', 'балк', 'колонн', 'прогон']): tags.append('metal_struct')
    if any(w in q for w in ['резк', 'раскро', 'cut']): tags.append('cut')
    if any(w in q for w in ['цен', 'стоим', 'прайс', 'расцен', 'сколько']): tags.append('price')
    if any(w in q for w in ['нижн', 'нижегород', 'н.новгород', 'н новгород', 'дзержинск', 'арзамас', 'кстово', 'бор ', 'саров', ' balakhna']): tags.append('geo_nn')
    if any(w in q for w in ['москв', 'мск', 'подмоск']): tags.append('geo_msk')
    if any(w in q for w in ['петербург', 'спб', 'ленинград']): tags.append('geo_spb')
    if any(w in q for w in ['екатеринбург', 'казань', 'самара', 'воронеж', 'ростов', 'краснодар', 'уфа', 'новосибирск', 'челябинск']): tags.append('geo_other')
    if any(w in q for w in ['сталь', 'нержав', 'алюмин', 'мед', 'лист', 'труб']): tags.append('material')
    if any(w in q for w in ['ворот', 'навес', 'лестниц', 'перил', 'козыр', 'калит', 'забор', 'анг', 'склад', 'навес', 'навес']): tags.append('product')
    if any(w in q for w in ['чпу', 'cnc', 'dxf', 'чертеж', 'autocad']): tags.append('tech')
    if any(w in q for w in ['заказ', 'изготов', 'производ', 'услуг', 'под ключ']): tags.append('commercial')
    if any(w in q for w in ['монтаж', 'установк', 'сборк']): tags.append('install')
    if not tags:
        tags.append('other')
    return tags

deduped['tags'] = deduped['query_norm'].apply(classify)

# cluster stats
cluster_keys = ['laser', 'plasma', 'bend', 'weld', 'metal_struct', 'cut', 'price', 'geo_nn', 'geo_msk', 'product', 'material', 'commercial', 'tech', 'install']
print('\n\n=== CLUSTER FREQUENCY (queries may belong to multiple) ===')
for ck in cluster_keys:
    subset = deduped[deduped['tags'].apply(lambda t: ck in t)]
    total = subset['freq'].sum()
    cnt = len(subset)
    print(f'\n{ck}: {cnt} queries, Σfreq={total:,}')
    for _, r in subset.sort_values('freq', ascending=False).head(8).iterrows():
        print(f"    {r['freq']:>8}  {r['query']}")

# Geo NN laser/plasma/metal_struct top
print('\n\n=== GEO NN (priority for Greydstroy) ===')
geo_nn = deduped[deduped['tags'].apply(lambda t: 'geo_nn' in t)].sort_values('freq', ascending=False)
for _, r in geo_nn.head(40).iterrows():
    print(f"{r['freq']:>8}  {r['query']}")

# Laser + geo_nn combined
print('\n\n=== LASER + GEO NN ===')
laser_geo = deduped[deduped['tags'].apply(lambda t: 'laser' in t and 'geo_nn' in t)].sort_values('freq', ascending=False)
for _, r in laser_geo.head(25).iterrows():
    print(f"{r['freq']:>8}  {r['query']}")

print('\n\n=== PLASMA + GEO NN ===')
plasma_geo = deduped[deduped['tags'].apply(lambda t: 'plasma' in t and 'geo_nn' in t)].sort_values('freq', ascending=False)
for _, r in plasma_geo.head(25).iterrows():
    print(f"{r['freq']:>8}  {r['query']}")

print('\n\n=== METAL_STRUCT + GEO NN ===')
mk_geo = deduped[deduped['tags'].apply(lambda t: 'metal_struct' in t and 'geo_nn' in t)].sort_values('freq', ascending=False)
for _, r in mk_geo.head(25).iterrows():
    print(f"{r['freq']:>8}  {r['query']}")

# Price intent
print('\n\n=== PRICE INTENT ===')
price_q = deduped[deduped['tags'].apply(lambda t: 'price' in t)].sort_values('freq', ascending=False)
for _, r in price_q.head(30).iterrows():
    print(f"{r['freq']:>8}  {r['query']}")

# Material + service combos for landing pages
print('\n\n=== MATERIAL x SERVICE (landing page candidates) ===')
material_service = deduped[
    deduped['tags'].apply(lambda t: 'material' in t and any(x in t for x in ['laser', 'plasma', 'cut', 'bend', 'weld']))
].sort_values('freq', ascending=False)
for _, r in material_service.head(40).iterrows():
    print(f"{r['freq']:>8}  {r['query']}")

# Thickness queries
print('\n\n=== THICKNESS / SPEC QUERIES ===')
thick = deduped[deduped['query_norm'].str.contains(r'\d+\s*(мм|mm)', regex=True)].sort_values('freq', ascending=False)
for _, r in thick.head(30).iterrows():
    print(f"{r['freq']:>8}  {r['query']}")
