"""Keep only the newest colour version of each bike (Spinlab's request, 2026-10-21).
Chosen by model year of the photos, SKU series and the "NEW COLOR" rows of Polygon's price list.
Cascade 3, 4 and 5 keep both colours (Spinlab's request, 2026-10-23). Bikes whose colours are all the same generation (Helios, Collosus T, Siskiu T...) keep every colour.
cascade.py and city.py apply it themselves; run it after extract.py or any other merge into bikes.json:
    python3 latest_colors.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
# slug: (colour id to keep, Frame Color spec text)
KEEP = {
    'siskiu-d7': ('blue-white-us', 'BLUE - WHITE'),
    'siskiu-d6': ('green-brown', 'GREEN - BROWN'),
    'siskiu-d5': ('cream-orange-us', 'CREAM - ORANGE'),
}



def latest(b):
    """Drop older colour versions of bike dict b in place; returns the removed colour labels."""
    if b['slug'] not in KEEP or not any(c['id'] == KEEP[b['slug']][0] for c in b['colors']):
        return []
    cid, frame = KEEP[b['slug']]
    gone = [c['label'] for c in b['colors'] if c['id'] != cid]
    b['colors'] = [c for c in b['colors'] if c['id'] == cid]
    b['skus'] = {k: v for k, v in b['skus'].items() if k.split('|')[0] == cid}
    for g in b['specs']:
        g['rows'] = [[k, frame] if k == 'Frame Color' else [k, v] for k, v in g['rows'] if k != 'Decal Color']
    return gone


if __name__ == '__main__':
    p = os.path.join(HERE, 'bikes.json')
    bikes = json.load(open(p, encoding='utf-8'))
    removed = [f"{b['name']}: {x}" for b in bikes for x in latest(b)]
    json.dump(bikes, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('bỏ màu cũ:', ', '.join(removed) or 'không có')
