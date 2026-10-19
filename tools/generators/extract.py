"""Extract structured bike data from saved Polygon model pages -> bikes.json"""
import sys, re, json, html, os

SRC = sys.argv[1]          # folder with <slug>.html
OUT = sys.argv[2]          # output json path
SLUGS = sys.argv[3:]


def clean(s):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    return ' '.join(s.split())


def section(t, sid):
    i = t.find(f'<section id="{sid}"')
    if i < 0:
        return ''
    j = t.find('</section>', i)
    return t[i:j]


def parse(slug):
    t = open(os.path.join(SRC, slug + '.html'), encoding='utf-8', errors='ignore').read()
    d = {'slug': slug, 'source': f'https://www.polygonbikes.com/us/{slug}/'}

    m = re.search(r'<h1[^>]*class="[^"]*product_title[^"]*"[^>]*>(.*?)</h1>', t, re.S) or re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    d['name'] = clean(m.group(1)) if m else slug

    # Series intro block: headline, tagline, description precede "Bike type:"
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    lines = [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '\n', body)).split('\n') if l.strip()]
    try:
        k = lines.index('Bike type:')
        d['headline'], d['tagline'], d['intro'] = lines[k - 3], lines[k - 2], lines[k - 1]
        d['bike_type'] = lines[k + 1]
    except ValueError:
        d['headline'] = d['tagline'] = d['intro'] = d['bike_type'] = ''

    # Variations: colors, sizes, SKUs, gallery per color
    m = re.search(r'data-product_variations="([^"]+)"', t)
    colors, sizes, skus = {}, [], {}
    if m and m.group(1) != 'false':
        for v in json.loads(html.unescape(m.group(1))):
            a = v['attributes']
            c = a.get('attribute_pa_color', '')
            s = a.get('attribute_pa_size', '')
            if s and s not in sizes:
                sizes.append(s)
            skus[f'{c}|{s}'] = v.get('sku', '')
            if c and c not in colors:
                imgs = [g['full_src'] for g in (v.get('variation_gallery_images') or [])]
                if not imgs and v.get('image', {}).get('full_src'):
                    imgs = [v['image']['full_src']]
                colors[c] = imgs
    # Human labels for attribute slugs from the select options
    labels = dict(re.findall(r'<option value="([a-z0-9-]+-us|[a-z0-9-]+)"[^>]*>([^<]+)</option>', t))
    d['colors'] = [{'id': c, 'label': labels.get(c, c.replace('-us', '').replace('-', ' ').title()), 'images': imgs} for c, imgs in colors.items()]
    d['sizes'] = [{'id': s, 'label': labels.get(s, s)} for s in sizes]
    d['skus'] = skus

    # Features
    f = section(t, 'features')
    d['feature_images'] = re.findall(r'<img src="([^"]+)"', f.split('product-features__detail')[0])
    d['features'] = [{'title': clean(a), 'text': clean(b)} for a, b in
                     re.findall(r'<a href="#" class="toggle[^"]*">(.*?)</a>\s*<div class="detail"[^>]*>(.*?)</div>\s*</li>', f, re.S)]

    # Specs grouped
    sp = section(t, 'specs')
    groups = []
    for g, block in re.findall(r'<a href="#" class="toggle[^"]*">(.*?)</a>\s*<div class="detail"[^>]*>(.*?)</div>\s*</li>', sp, re.S):
        rows = [(clean(k), clean(v)) for k, v in re.findall(r'<div class="detail-title">(.*?)</div>\s*<div class="detail-message">(.*?)</div>', block, re.S)]
        rows = [(k, v) for k, v in rows if v]
        if rows:
            groups.append({'group': clean(g), 'rows': rows})
    d['specs'] = groups

    # Geometry (metric values)
    g = section(t, 'geometry')
    tb = re.search(r'<table class="product-geometry__table">(.*?)</table>', g, re.S)
    geo = None
    if tb:
        head = [clean(x) for x in re.findall(r'<th[^>]*>(.*?)</th>', re.search(r'<thead>(.*?)</thead>', tb.group(1), re.S).group(1), re.S)]
        rows = []
        for tr in re.findall(r'<tr>(.*?)</tr>', re.search(r'<tbody>(.*?)</tbody>', tb.group(1), re.S).group(1), re.S):
            th = re.search(r'<th[^>]*>(.*?)</th>', tr, re.S)
            label = clean(re.sub(r'<span class="unit">.*', '', th.group(1), flags=re.S)) if th else ''
            unit = re.search(r'<span class="mm">([^<]*)</span>', th.group(1)) if th else None
            vals = []
            for td in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S):
                mm = re.search(r'<span class="mm">(.*?)</span>', td, re.S)
                vals.append(clean(mm.group(1)) if mm else clean(td))
            if label:
                rows.append({'label': label, 'unit': unit.group(1) if unit else '', 'values': vals})
        geo = {'sizes': head[1:], 'rows': rows}
        gi = re.search(r'product-geometry__image[^>]*>.*?<img[^>]+src="([^"]+)"', g, re.S)
        geo['image'] = gi.group(1) if gi else ''
    d['geometry'] = geo
    return d


data = [parse(s) for s in SLUGS]
json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for b in data:
    print(f"{b['slug']:45} {b['name'][:30]:30} type={b['bike_type'][:16]:16} colors={len(b['colors'])} sizes={len(b['sizes'])} "
          f"feat={len(b['features'])} specgroups={len(b['specs'])} geo={'y' if b['geometry'] else 'n'} imgs={sum(len(c['images']) for c in b['colors'])}")
