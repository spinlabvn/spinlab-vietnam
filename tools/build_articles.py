"""Articles: the "Tin tức" and "Hướng dẫn" menus (data/articles.json).

Each article becomes its own page (<slug>.html); tin-tuc.html and huong-dan.html list the articles of
their category, and the homepage "Tin tức & Hướng dẫn" section shows the newest ones. Product cards inside an
article are read from the product pages (name, photo, category), so prices and hover photos follow the usual
post-processing. Run after build_new_products.py and before apply_prices.py:
    python3 tools/build_articles.py
"""
import collections, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'generators'))
from vi import VI  # noqa: E402

R = lambda f: open(os.path.join(ROOT, f), encoding='utf-8').read()
W = lambda f, s: open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)
E = lambda s: html.escape(s, quote=True)
BK = {b['slug']: b for b in json.load(open(os.path.join(ROOT, 'tools', 'generators', 'bikes.json'), encoding='utf-8'))}
PRICES = json.load(open(os.path.join(ROOT, 'data', 'page-prices.json'), encoding='utf-8'))['prices']
_set = os.path.join(ROOT, 'data', 'settings.json')
if os.path.exists(_set) and not json.load(open(_set, encoding='utf-8')).get('show_prices', True):
    PRICES = {}   # prices hidden site-wide: tables show "Liên hệ"
vnd = lambda n: f'{n:,}'.replace(',', '.') + '₫'
CATS = {'tin-tuc': ('Tin tức', 'tin-tuc.html'), 'huong-dan': ('Hướng dẫn', 'huong-dan.html')}
# same contact block as the homepage ("Chưa biết chọn xe nào?")
CTA = ('<div class="help"><div><h2>Cần tư vấn thêm?</h2><p>Đội ngũ kỹ thuật Spinlab sẽ tư vấn chọn size, dòng xe và lốp phù hợp với bạn.</p></div>'
       '<div class="actions"><a class="btn btn-yellow" href="tel:0399337533">Gọi 0399 337 533</a>'
       '<a class="btn btn-zalo" href="https://zalo.me/0399337533" target="_blank" rel="noopener"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg" alt="" width="22" height="22">Chat Zalo</a>'
       '<a class="btn btn-light" href="dai-ly.html">Tìm đại lý</a></div></div>')


def product_card(f, desc=''):
    """A product card built from the product page itself."""
    s = R(f)
    name = re.sub(r'^(Polygon|Vittoria|Story|Emume)\s+', '', re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1)).strip())
    img = re.search(r'id="g-main"[^>]*src="([^"]+)"|src="([^"]+)"[^>]*id="g-main"', s)
    img = (img.group(1) or img.group(2)).replace('width=1000', 'width=600')
    brand = re.sub(r'<[^>]+>', '', re.search(r'<span class="p-brand">(.*?)</span>', s, re.S).group(1)).strip()
    tire = ' tire' if 'cdn.shopify.com' in img else ''
    price = re.search(r'<span class="p-price big">([^<]*)</span>', s).group(1)
    return (f'<article class="p-card"><div class="p-img{tire}"><img src="{E(img)}" alt="{E(brand.split(" · ")[0] + " " + name)}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">{E(brand)}</span><h3 class="p-name"><a class="stretch" href="{f}">{E(name)}</a></h3>'
            + (f'<p class="p-desc">{E(desc)}</p>' if desc else '') + f'<span class="p-price">{E(price)}</span></div></article>')


def products(items, title='Sản phẩm trong bài'):
    return f'<section class="art-products"><h2>{title}</h2><div class="grid">{"".join(product_card(f, d) for f, d in items)}</div></section>'


# ---------- size chart (from the geometry tables of the bikes on the site) ----------
# One table: a row per size, a column per bike family, so every family lines up on the same sizes.
GROUPS = [('Road', 'Helios, Strattos', lambda v: v['cat'] == 'road'),
          ('MTB', 'Mọi dòng MTB', lambda v: v['cat'] in ('dh', 'enduro', 'trail', 'xc')),
          ('Heist', 'City - Hybrid', lambda v: v['series'] == 'Heist'),
          ('Path', 'City &amp; Gravel', lambda v: v['series'] in ('Path', 'Path X'))]
ORDER = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
cols = []
for title, sub, keep in GROUPS:
    agg = collections.defaultdict(collections.Counter)
    for slug, v in VI.items():
        g = BK.get(slug, {}).get('geometry')
        if v.get('brand', 'Polygon') != 'Polygon' or not g or not keep(v):
            continue
        for r in g['rows']:
            if r['label'] == 'Height':
                for sz, val in zip(g['sizes'], r['values']):
                    sz = re.sub(r'\s*\(.*\)$', '', sz)   # 'XS (27.5″)' -> 'XS'
                    if sz in ORDER:
                        agg[sz][val.replace('-', '–')] += 1
    if agg:
        cols.append((title, sub, {sz: c.most_common(1)[0][0] for sz, c in agg.items()}))
sizes = [sz for sz in ORDER if any(sz in c for _, _, c in cols)]
head = ''.join(f'<th scope="col">{t}<small>{s}</small></th>' for t, s, _ in cols)
body = ''.join(f'<tr><th scope="row">{sz}</th>' + ''.join(f'<td>{c[sz]}</td>' if sz in c else '<td class="na">—</td>' for _, _, c in cols) + '</tr>'
               for sz in sizes)
SIZE_TABLE = (f'<div class="table-wrap size-table"><table><caption>Chiều cao người đạp (cm) theo size khung</caption>'
              f'<thead><tr><th scope="col">Size</th>{head}</tr></thead><tbody>{body}</tbody></table></div>')

# ---------- Strattos C: builds from bikes.json + retail prices ----------
SC = [('2026-strattos-c9-axs-road-bike', 'SRAM Force AXS E1 2x12, điện tử không dây', 'LINC Alpha Carbon 35mm'),
      ('2026-strattos-c8-di2-road-bike', 'Shimano Ultegra Di2 2x12', 'Polygon WR4 Carbon'),
      ('2026-strattos-c7-di2-road-bike', 'Shimano 105 Di2 2x12', 'Polygon WR4 Carbon')]
sc_rows = ''.join(f'<tr><th scope="row"><a href="{VI[s]["file"]}.html">{E(BK[s]["name"])}</a></th><td>{g}</td><td>{w}</td>'
                  f'<td>{vnd(PRICES[VI[s]["file"] + ".html"]) if VI[s]["file"] + ".html" in PRICES else "Liên hệ"}</td></tr>' for s, g, w in SC)

# Articles live in data/articles.json (edited from the admin page, tools/admin.py).
# Placeholders in a body are filled with tables computed from the current data.
PLACEHOLDERS = {
    'bang_gia_strattos_c': ('<div class="table-wrap"><table><thead><tr><th scope="col">Phiên bản</th><th scope="col">Bộ truyền động</th>'
                            f'<th scope="col">Bộ vành</th><th scope="col">Giá bán lẻ</th></tr></thead><tbody>{sc_rows}</tbody></table></div>'),
    'bang_size': SIZE_TABLE,
}
fill = lambda body: re.sub(r'(?:<p>\s*)?\{\{(\w+)\}\}(?:\s*</p>)?', lambda m: PLACEHOLDERS.get(m.group(1), m.group(0)), body)
ARTICLES = json.load(open(os.path.join(ROOT, 'data', 'articles.json'), encoding='utf-8'))['articles']
for _a in ARTICLES:
    _a['body'] = fill(_a['body'])
    _a['products'] = [tuple(x) for x in _a.get('products', []) if os.path.exists(os.path.join(ROOT, x[0]))]

ARTICLES.sort(key=lambda a: a['date'], reverse=True)
date_vi = lambda d: '/'.join(reversed(d.split('-')))

CSS = '''/* Articles */
.art-grid{display:grid;gap:24px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));margin:24px 0 56px}
@media (min-width:1024px){.art-grid{grid-template-columns:repeat(3,1fr)}}
.art-card{display:flex;flex-direction:column}
.art-card .n-img{aspect-ratio:16/10;border-radius:var(--radius);overflow:hidden;background:var(--surface);flex:none}
.art-card .n-img img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
.art-card .n-img.fit img{object-fit:contain;padding:8%;mix-blend-mode:multiply}
.art-card:hover .n-img img{transform:scale(1.04)}
.art-card small{display:block;margin-top:12px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-red)}
.art-card h3{margin:4px 0 6px;font-size:18px;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:calc(2em * 1.35)}
.art-card:hover h3{text-decoration:underline;text-underline-offset:3px}
.art-card p{margin:0;color:var(--muted);font-size:14px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;min-height:calc(3em * 1.5)}
.article{max-width:780px;margin:0 auto 48px}
.article .meta{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-red);margin:8px 0}
.article h1{font-size:clamp(28px,4vw,40px);line-height:1.15;margin:0 0 12px}
.article .lead{font-size:18px;color:var(--muted);margin:0 0 24px}
.article .hero-img{margin:0 0 32px;border-radius:var(--radius);overflow:hidden;aspect-ratio:16/9;background:var(--surface)}
.article .hero-img img{width:100%;height:100%;object-fit:cover}
.article .hero-img.fit img{object-fit:contain;padding:6%;mix-blend-mode:multiply}
.article .body{font-size:17px;line-height:1.7}
.article .body h2{font-size:24px;line-height:1.25;margin:36px 0 10px}
.article .body ul{padding-left:22px;display:grid;gap:6px}
.article .body figure{margin:24px 0}
.article .body figure img{width:100%;border-radius:var(--radius)}
.article .body a{color:var(--brand-red);text-decoration:underline;text-underline-offset:2px}
.article .body table{font-size:15px}
.art-help{max-width:780px;margin:0 auto 8px}
.art-help .help{padding:20px 24px;gap:14px}
.art-help .help h2{font-size:20px;margin-bottom:4px}
.art-help .help p{font-size:14px}
.art-help .help .actions{gap:8px}
.art-help .help .btn{min-height:42px;padding:0 18px;font-size:13px}
.art-help .help .btn-zalo img{width:20px;height:20px}
@media (min-width:768px){.art-help .help{grid-template-columns:1fr auto;padding:22px 28px}.art-help .help .actions{justify-content:flex-end;flex-wrap:nowrap}}
.article .cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.size-table table{width:100%;table-layout:fixed}
.size-table caption{text-align:left;font-weight:700;margin-bottom:8px}
.size-table th,.size-table td{text-align:center;padding:10px 6px;white-space:nowrap;font-variant-numeric:tabular-nums}
.size-table thead th{vertical-align:bottom;line-height:1.25;white-space:normal;text-transform:none;letter-spacing:0}
.size-table thead th small{display:block;font-weight:400;color:var(--muted);font-size:12px;white-space:normal;margin-top:2px}
.size-table thead th:first-child,.size-table tbody th{width:56px}
.size-table tbody th{font-weight:800}
.size-table tbody tr:nth-child(even){background:var(--surface)}
.size-table .na{color:var(--muted)}
@media (max-width:560px){.size-table th,.size-table td{padding:8px 3px;font-size:13px}.size-table thead th small{font-size:11px}}
.art-products{margin:40px 0 0}
.art-products h2{font-size:22px;margin:0 0 16px}
.art-more{border-top:1px solid var(--line);padding-top:32px;margin-top:8px}
.art-more h2{font-size:22px;margin:0 0 4px}
.follow{list-style:none;margin:16px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:10px}
.follow a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px 0 14px;border-radius:999px;border:1.5px solid var(--text);background:#fff;color:var(--text);font-weight:700;font-size:14px;transition:transform .2s,background-color .2s,border-color .2s,color .2s}
.follow a:hover,.follow a:focus-visible{transform:translateY(-2px);background:var(--brand-yellow);border-color:var(--brand-yellow);color:var(--brand-red)}
.follow svg{width:20px;height:20px}
'''


def shell(fname, title, desc, main):
    p = R('xe-road.html')
    p = re.sub(r'<title>.*?</title>', f'<title>{E(title)} — Spinlab</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{E(desc)}">', p, 1)
    p = re.sub(r'<main id="main".*?</main>', lambda m: main, p, 1, flags=re.S)
    p = re.sub(r'/\* (Articles|Hub pages) \*/.*?(?=</style>)', '', p, flags=re.S).replace('</style>', CSS + '</style>', 1)
    p = re.sub(r'\s*<meta name="product-id"[^>]*>', '', p)
    W(fname, p)


def art_card(a):
    fit = ' fit' if a.get('contain') else ''
    return (f'<a class="art-card" href="{a["slug"]}.html"><div class="n-img{fit}"><img src="{E(a["thumb"])}" alt="" loading="lazy"></div>'
            f'<small>{E(a["tag"])} · {date_vi(a["date"])}</small><h3>{E(a["title"])}</h3><p>{E(a["lead"][:150].rsplit(" ", 1)[0])}…</p></a>')


crumbs = lambda items: ('<div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li>'
                        + ''.join(f'<li><a href="{h}">{E(t)}</a></li>' if h else f'<li aria-current="page">{E(t)}</li>' for t, h in items) + '</ol></nav></div>')

# remove pages of articles deleted from data/articles.json
_keep = {a['slug'] + '.html' for a in ARTICLES}
for _f in os.listdir(ROOT):
    if _f.endswith('.html') and _f not in _keep and '<article class="article">' in R(_f):
        os.remove(os.path.join(ROOT, _f))
        print('xoá bài:', _f)

for a in ARTICLES:
    cname, chref = CATS[a['cat']]
    fit = ' fit' if a.get('contain') else ''
    more = [x for x in ARTICLES if x is not a][:3]
    main = f'''<main id="main" class="pdp listing">
  {crumbs([(cname, chref), (a['title'], None)])}
  <div class="container"><article class="article">
    <p class="meta">{E(a['tag'])} · {date_vi(a['date'])}</p>
    <h1>{E(a['title'])}</h1>
    <p class="lead">{E(a['lead'])}</p>
    <figure class="hero-img{fit}"><img src="{E(a['image'])}" alt="{E(a['title'])}"></figure>
    <div class="body">{a['body']}</div>
  </article>
  <div class="art-help">{CTA}</div>
  {products(a['products']) if a['products'] else ''}
  <section class="art-more"><h2>Bài viết khác</h2><div class="art-grid">{"".join(art_card(x) for x in more)}</div></section></div>
</main>'''
    shell(a['slug'] + '.html', a['title'], a['lead'][:155], main)

LEADS = {'tin-tuc': 'Tin sản phẩm mới, hoạt động và sự kiện của Spinlab.',
         'huong-dan': 'Chọn size xe, chọn lốp và chăm sóc xe — hướng dẫn từ đội ngũ kỹ thuật Spinlab.'}
SOCIAL = [('Facebook', 'https://www.facebook.com/profile.php?id=61573821032401', 'i-facebook'),
          ('Instagram', 'https://www.instagram.com/spinlabvn/', 'i-instagram'),
          ('YouTube', 'https://www.youtube.com/@Spinlabvn', 'i-youtube'),
          ('TikTok', 'https://www.tiktok.com/@spinlab.vn', 'i-tiktok')]
# white buttons; hover like "Theo dõi Spinlab" in the footer (yellow, red text, lift)
FOLLOW = ('<section class="art-more"><h2>Sự kiện &amp; cộng đồng</h2><p>Lịch chạy thử xe, giải đua và các buổi gặp gỡ cộng đồng của Spinlab được thông báo trên mạng xã hội.</p>'
          '<ul class="follow">' + ''.join(f'<li><a href="{u}" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#{i}"/></svg>{n}</a></li>'
                                          for n, u, i in SOCIAL) + '</ul></section>')
for cat, (cname, chref) in CATS.items():
    items = [a for a in ARTICLES if a['cat'] == cat]
    main = f'''<main id="main" class="pdp listing">
  {crumbs([(cname, None)])}
  <section class="list-hero plain">
    <div class="container"><div class="lh-copy"><span class="kicker">Spinlab</span><h1>{cname}</h1><p>{LEADS[cat]}</p></div></div>
  </section>
  <div class="container"><div class="art-grid">{"".join(art_card(a) for a in items)}</div>{FOLLOW if cat == 'tin-tuc' else ''}</div>
</main>'''
    shell(chref, cname, LEADS[cat], main)

# Homepage: newest articles of both menus
idx = R('index.html')
cards = ''.join(f'\n        <a href="{a["slug"]}.html"><div class="n-img{" y" if a.get("contain") else ""}"><img src="{E(a["thumb"])}" alt="" loading="lazy"></div>'
                f'<small>{E(a["tag"])}</small><h3>{E(a["title"])}</h3></a>' for a in ARTICLES[:3])
idx = re.sub(r'(<div class="news">).*?(\n      </div>\n    </div>\n  </section>\n</main>)', lambda m: m.group(1) + cards + m.group(2), idx, 1, flags=re.S)
idx = re.sub(r'(<h2>Tin tức &amp; Hướng dẫn</h2><a class="see-all" href=")[^"]*(")', r'\1/tin-tuc\2', idx, 1)
W('index.html', idx)
print(len(ARTICLES), 'bài viết; tin-tuc.html, huong-dan.html, trang chủ')
