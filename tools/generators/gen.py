"""Generate Polygon bike detail pages from bikes.json + vi.py, using corsa-pro.html as the page shell."""
import sys, re, json, html, os
sys.path.insert(0, os.path.dirname(__file__))
from vi import VI, CATS, SPEC_GROUPS, SPEC_ROWS, GEO_ROWS

OUTDIR, DATA = sys.argv[1], sys.argv[2]
bikes = {b['slug']: b for b in json.load(open(DATA, encoding='utf-8'))}
shell = open(os.path.join(OUTDIR, 'corsa-pro.html'), encoding='utf-8').read()
E = html.escape
ZALO = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg'

BIKE_CSS = '''
/* Bike detail extras */
.swatches-pick{display:flex;flex-wrap:wrap;gap:8px}
.opt-group{border:0;margin:8px 0 0;padding:0}
.opt-group legend{padding:0;margin-bottom:10px;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.04em;display:flex;gap:10px;flex-wrap:wrap;align-items:baseline}
.siblings{margin:16px 0 0;font-size:14px;color:var(--muted)}
.siblings b{color:var(--text)}
.siblings a{color:var(--brand-red);font-weight:600;text-decoration:underline;text-underline-offset:2px}
.feat-imgs{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-top:20px}
.feat-imgs img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--radius)}
.spec-groups{display:grid;gap:24px}
@media (min-width:1024px){.spec-groups{grid-template-columns:1fr 1fr;gap:24px 40px}}
.spec-groups h3{margin:0 0 4px;font-size:15px;text-transform:uppercase;letter-spacing:.04em;color:var(--brand-red)}
.spec-groups .spec-list div{grid-template-columns:150px 1fr}
.spec-groups dd{font-weight:500;font-size:14px}
.geo td,.geo th{white-space:nowrap;text-align:center}
.geo tbody th{text-align:left;font-weight:500}
.geo .col-on{background:#FFF7D6}
.geo-note{font-size:13px;color:var(--muted);margin:10px 0 0}
.geo-img{margin:20px 0 0;max-width:720px}
.geo-img img{width:100%;mix-blend-mode:multiply}
'''

FAQ_T = [
    ('Chọn size xe như thế nào?', 'Hãy tham khảo hàng “Chiều cao người lái” trong bảng Kích thước khung. Nếu chiều cao của bạn nằm giữa hai size, liên hệ Spinlab để được tư vấn theo tư thế và nhu cầu đạp.'),
    ('Xe được bảo hành thế nào?', 'Xe chính hãng {brand} phân phối bởi Spinlab được bảo hành theo chính sách của {brand}. Liên hệ hotline để biết chi tiết điều kiện và thời hạn.'),
    ('Có thể nâng cấp linh kiện không?', 'Có. Liên hệ Spinlab để được tư vấn nâng cấp phù hợp, ví dụ lốp Vittoria hay dây cuốn ghi đông Emume.'),
]


ORDER = ['XXXS', 'XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'ONE SIZE']


def size_code(label):
    u = label.upper().replace('XTRA LARGE', 'XL').replace('LARGE', 'L').replace('MEDIUM', 'M').replace('SMALL', 'S')
    import re as _re
    m = _re.search(r'\b(XXXS|XXS|XS|XXL|XL|S|M|L|ONE SIZE)\b', u)
    wheel = '27.5' if '27.5' in u else ('29' if '29' in u else '')
    return (m.group(1) if m else u, wheel)


def order_sizes(sizes, geo_sizes):
    """Sort sizes small->large and map each to its geometry column index."""
    key = lambda s: (ORDER.index(size_code(s['label'])[0]) if size_code(s['label'])[0] in ORDER else 99, size_code(s['label'])[1])
    out = sorted(sizes, key=key)
    gcodes = [size_code(g) for g in geo_sizes]
    for i, s in enumerate(out):
        c = size_code(s['label'])
        col = next((k for k, g in enumerate(gcodes) if g == c), None)
        if col is None:
            col = next((k for k, g in enumerate(gcodes) if g[0] == c[0] and not (g[1] and c[1] and g[1] != c[1])), i if len(gcodes) == len(out) else -1)
        s['col'] = col
    return out


def display_name(n):
    n = n.replace('RELIC20', 'RELIC 20').replace(' with UDH', '')
    return n


def img(u, alt, lazy=True, extra=''):
    lz = ' loading="lazy"' if lazy else ''
    return '<img src="%s" alt="%s"%s%s>' % (E(u), E(alt), lz, extra)


def page(slug):
    b, v = bikes[slug], VI[slug]
    brand = v.get('brand', 'Polygon')
    name = display_name(b['name'])
    cat_label, cat_href = CATS[v['cat']]
    colors = b['colors'] or [{'id': 'default', 'label': '—', 'images': []}]
    first_imgs = colors[0]['images'] or ['']
    sku0 = ''

    thumbs = ''.join(
        f'<li><button aria-pressed="{"true" if i == 0 else "false"}" data-src="{E(u)}" data-alt="{E(brand)} {E(name)} – ảnh {i+1}">{img(u, f"Ảnh {i+1}")}</button></li>'
        for i, u in enumerate(first_imgs))
    color_opts = ''.join(
        f'<label><input type="radio" name="color" value="{E(c["id"])}"{" checked" if i == 0 else ""}><span>{E(c["label"])}</span></label>'
        for i, c in enumerate(colors))
    sizes = order_sizes(b['sizes'], b['geometry']['sizes'] if b['geometry'] else [])
    size_opts = ''.join(
        f'<label><input type="radio" name="size" value="{E(s["id"])}" data-col="{s["col"]}"{" checked" if i == 0 else ""}><span>{E(s["label"])}</span></label>'
        for i, s in enumerate(sizes))
    chips = ''.join(f'<li>{E(c)}</li>' for c in v['chips'])
    tag_emtb = '<li>E-MTB</li>' if v.get('emtb') else ''

    feats = ''.join(f'<article><span class="num">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></article>' for i, (t, d) in enumerate(v['features']))
    feat_imgs = ''.join(img(u, f'{brand} {v["series"]} – hình ảnh tính năng') for u in b['feature_images'][:3])
    intro_img = (b['feature_images'] or [c['images'][1] if len(c['images']) > 1 else c['images'][0] for c in colors if c['images']] or [''])[0]

    spec_html = ''
    for g in b['specs']:
        rows = ''.join(f'<div><dt>{E(SPEC_ROWS.get(k, k))}</dt><dd>{E(val)}</dd></div>' for k, val in g['rows'])
        spec_html += f'<section><h3>{E(SPEC_GROUPS.get(g["group"], g["group"]))}</h3><dl class="spec-list">{rows}</dl></section>'

    geo_html = ''
    if b['geometry'] and b['geometry']['rows']:
        gsz = b['geometry']['sizes']
        head = ''.join(f'<th scope="col">{E(s)}</th>' for s in gsz)
        body = ''
        for r in b['geometry']['rows']:
            m = re.match(r'(.*?)\s*(\([A-Z0-9]+\))?$', r['label'])
            lab = GEO_ROWS.get(m.group(1), m.group(1)) + (f' {m.group(2)}' if m.group(2) else '')
            body += f'<tr><th scope="row">{E(lab)}</th>' + ''.join(f'<td>{E(x)}</td>' for x in r['values']) + '</tr>'
        gimg = f'<figure class="geo-img">{img(b["geometry"]["image"], "Sơ đồ ký hiệu kích thước khung")}</figure>' if b['geometry'].get('image') else ''
        geo_html = f'''<section class="pdp-sec" id="kich-thuoc"><h2>Kích thước khung (geometry)</h2>
      <div class="table-wrap"><table class="geo"><caption>Đơn vị: mm và độ (°), trừ chiều cao người lái (cm)</caption><thead><tr><th scope="col">Thông số</th>{head}</tr></thead><tbody>{body}</tbody></table></div>
      <p class="geo-note">Cột size đang chọn được tô màu. Số liệu theo {"Polygon Bikes" if brand == "Polygon" else brand}.</p>{gimg}</section>'''

    # related: same category, else same MTB family
    mtb = {'dh', 'enduro', 'trail', 'xc'}
    pool = [s for s in VI if s != slug and (VI[s]['cat'] == v['cat'] or (v['cat'] in mtb and VI[s]['cat'] in mtb))]
    MO = ['dh', 'enduro', 'trail', 'xc']
    dist = lambda c: abs(MO.index(c) - MO.index(v['cat'])) if c in MO and v['cat'] in MO else (c != v['cat'])
    pool.sort(key=lambda s: (VI[s]['series'] != v['series'], dist(VI[s]['cat'])))
    rel = ''
    for s in pool[:3]:
        rb = bikes[s]
        ri = rb['colors'][0]['images'][0] if rb['colors'] and rb['colors'][0]['images'] else ''
        rel += (f'<article class="p-card"><div class="p-img">{img(ri, VI[s].get("brand", "Polygon") + " " + display_name(rb["name"]))}</div>'
                f'<div class="p-body"><span class="p-brand">{E(VI[s].get("brand", "Polygon"))} · {E(CATS[VI[s]["cat"]][0])}</span>'
                f'<h3 class="p-name"><a class="stretch" href="{VI[s]["file"]}.html">{E(display_name(rb["name"]))}</a></h3>'
                f'<p class="p-desc">{E(VI[s]["headline"])}</p><span class="p-price">1.980.000₫</span></div></article>')

    # sibling versions: link those that have their own page
    fam = sorted((s for s in VI if VI[s]['series'] == v['series']), key=lambda s: next((i for i, t in enumerate(v['siblings'].split(' · ')) if display_name(bikes[s]['name']).upper().replace(' DI2', '').endswith(t.upper().replace(' DI2', ''))), 99))
    if len(fam) > 1:
        sib = ' · '.join(f'<b aria-current="page">{E(display_name(bikes[s]["name"]))}</b>' if s == slug else
                         f'<a href="{VI[s]["file"]}.html">{E(display_name(bikes[s]["name"]))}</a>' for s in fam)
    else:
        sib = E(v['siblings'])
    rel_html = (f'''    <section class="pdp-sec"><div class="sec-head"><h2>Xe đạp tương tự</h2><a class="see-all" href="{cat_href}">Xem tất cả</a></div>
      <div class="grid related">{rel}</div></section>''' if rel else '')
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in (v.get('faq') or [(q, x.replace('{brand}', brand)) for q, x in FAQ_T]))
    nav_geo = '<a href="#kich-thuoc">Kích thước khung</a>' if geo_html else ''
    nav_feat = '<a href="#tinh-nang">Tính năng</a>' if feats else ''
    feat_imgs_html = ('<div class="feat-imgs">%s</div>' % feat_imgs) if feat_imgs else ''
    feat_sec = f'''<section class="pdp-sec" id="tinh-nang"><h2>Tính năng nổi bật</h2><div class="tech">{feats}</div>
      {feat_imgs_html}</section>''' if feats else ''
    size_hint = '<p class="hint"><a href="#kich-thuoc">Xem bảng kích thước khung để chọn size</a></p>' if geo_html else ''
    size_hint_and_opts = size_opts + '</div>' + size_hint
    sku_meta = f'<span class="size-meta" aria-live="polite">Mã <span id="sz-sku">{E(sku0)}</span></span>' if b['skus'] else ''
    size_field = f'''<fieldset class="sizes"><legend>Size {sku_meta}</legend>
          <div class="size-opts">{size_hint_and_opts}</fieldset>''' if b['sizes'] else ''

    main_img = img(first_imgs[0], brand + " " + name, lazy=False, extra=' id="g-main" width="1400" height="1050"')
    main = f'''<main id="main" class="pdp">
  <div class="container">
    <nav class="crumbs" aria-label="Đường dẫn"><ol>
      <li><a href="index.html">Trang chủ</a></li><li><a href="xe-dap.html">Xe đạp</a></li>
      <li><a href="{cat_href}">{E(cat_label)}</a></li><li aria-current="page">{E(name)}</li></ol></nav>

    <div class="pdp-top">
      <div class="gallery">
        <div class="g-main">{main_img}</div>
        <ul class="g-thumbs" aria-label="Ảnh sản phẩm">{thumbs}</ul>
      </div>
      <div class="buy">
        <span class="p-brand">{E(brand)} · {E(cat_label)}</span>
        <h1>{E(brand)} {E(name)}</h1>
        <p class="tagline">{E(v["headline"])}</p>
        <ul class="models">{tag_emtb}{chips}</ul>
        <fieldset class="opt-group"><legend>Màu sắc <span class="size-meta" id="color-name">{E(colors[0]["label"])}</span></legend>
          <div class="size-opts">{color_opts}</div></fieldset>
        {size_field}
        <div class="price-row"><span class="label">Giá bán lẻ</span><span class="p-price big">1.980.000₫</span></div>
        <div class="buy-ctas">
          <a class="btn btn-zalo outline" href="https://zalo.me/0399337533" target="_blank" rel="noopener"><img src="{ZALO}" alt="" width="22" height="22">Chat Zalo</a>
          <a class="btn btn-outline" href="tel:0399337533">Gọi 0399 337 533</a>
        </div>
        <ul class="assure">
          <li><svg aria-hidden="true"><use href="#i-shield"/></svg>Xe chính hãng {E(brand)}, phân phối bởi Spinlab</li>
          <li><svg aria-hidden="true"><use href="#i-truck"/></svg>Giao hàng toàn quốc</li>
          <li><svg aria-hidden="true"><use href="#i-chat"/></svg>Tư vấn chọn size miễn phí qua hotline</li>
        </ul>
      </div>
    </div>

    <nav class="pdp-nav" aria-label="Nội dung sản phẩm"><a href="#gioi-thieu">Giới thiệu</a>{nav_feat}<a href="#thong-so">Thông số</a>{nav_geo}<a href="#hoi-dap">Hỏi đáp</a></nav>

    <section class="pdp-sec intro" id="gioi-thieu">
      <div><h2>{E(v["headline"])}</h2><p>{E(v["intro"])}</p>
        <p class="siblings">Các phiên bản trong dòng <b>{E(v["series"])}</b>: {sib}</p></div>
      <figure>{img(intro_img, brand + " " + v["series"])}</figure>
    </section>

    {feat_sec}

    <section class="pdp-sec" id="thong-so"><h2>Thông số kỹ thuật</h2><div class="spec-groups">{spec_html}</div>
      <p class="geo-note">Thông số có thể thay đổi theo lô hàng. Vui lòng liên hệ Spinlab để xác nhận cấu hình xe tại Việt Nam.</p></section>

    {geo_html}

    <section class="pdp-sec" id="hoi-dap"><h2>Hỏi đáp</h2><div class="faq">{faq}</div></section>

{rel_html}
  </div>
</main>'''

    data = {'colors': {c['id']: {'label': c['label'], 'images': c['images']} for c in colors}, 'skus': b['skus'], 'name': name, 'brand': brand}
    js = '''
// Bike gallery, colour & size selector
(() => {
  const D = %s;
  const main=document.getElementById('g-main'), list=document.querySelector('.g-thumbs');
  const bindThumbs=()=>{ const t=[...list.querySelectorAll('button')]; t.forEach(b=>b.addEventListener('click',()=>{ main.src=b.dataset.src; main.alt=b.dataset.alt; t.forEach(x=>x.setAttribute('aria-pressed',x===b)); })); };
  const val=n=>(document.querySelector(`input[name=${n}]:checked`)||{}).value||'';
  const updSku=()=>{ const el=document.getElementById('sz-sku'); if(el) el.textContent=D.skus[val('color')+'|'+val('size')]||'—'; };
  document.querySelectorAll('input[name=color]').forEach(r=>r.addEventListener('change',()=>{
    const c=D.colors[r.value]; document.getElementById('color-name').textContent=c.label;
    if(c.images.length){ main.src=c.images[0]; list.innerHTML=c.images.map((u,i)=>`<li><button aria-pressed="${i===0}" data-src="${u}" data-alt="${D.brand} ${D.name} – ${c.label} – ảnh ${i+1}"><img src="${u}" alt="Ảnh ${i+1}"></button></li>`).join(''); bindThumbs(); }
    updSku(); }));
  const geo=document.querySelector('table.geo');
  const hl=()=>{ if(!geo) return; const r=document.querySelector('input[name=size]:checked'); if(!r) return;
    const i=+r.dataset.col;
    geo.querySelectorAll('tr').forEach(tr=>[...tr.cells].forEach((c,k)=>c.classList.toggle('col-on',k===i+1))); };
  document.querySelectorAll('input[name=size]').forEach(r=>r.addEventListener('change',()=>{ updSku(); hl(); }));
  bindThumbs(); updSku(); hl();
})();
''' % json.dumps(data, ensure_ascii=False)

    p = shell
    p = re.sub(r'<title>.*?</title>', f'<title>{E(brand)} {E(name)} — Spinlab</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{E(brand + " " + name + ": " + v["headline"] + ". Phân phối chính hãng bởi Spinlab.")}">', p, 1)
    p = p.replace('</style>', BIKE_CSS + '</style>', 1)
    p = re.sub(r'<main id="main" class="pdp">.*?</main>', lambda m: main, p, 1, flags=re.S)
    p = re.sub(r'// Product gallery \+ size selector.*?\}\)\(\);\n', lambda m: js.lstrip('\n'), p, 1, flags=re.S)
    open(os.path.join(OUTDIR, v['file'] + '.html'), 'w', encoding='utf-8').write(p)
    return v['file'] + '.html', len(p)


ONLY = sys.argv[3:]
for s in VI:
    if not ONLY or s in ONLY:
        print(*page(s))
