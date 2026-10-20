"""Hub pages that replace the old 'index.html#hot' / '#brands' links:
xe-dap.html (bike categories), phu-tung.html (parts categories), thuong-hieu.html (brands).
Counts are read from the listing pages, so run after the listings are up to date:
    python3 tools/build_hubs.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda f: open(os.path.join(ROOT, f), encoding='utf-8').read()
W = lambda f, s: open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)
count = lambda f: R(f).count('<article class="p-card"') if os.path.exists(os.path.join(ROOT, f)) else 0
first_img = lambda f: (re.search(r'<article class="p-card".*?<img src="([^"]+)"', R(f), re.S) or [None, ''])[1]

CSS = '''/* Hub pages */
.hub-grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));margin:24px 0 56px}
.hub{position:relative;display:flex;flex-direction:column;border:1px solid var(--line);border-radius:var(--radius);background:#fff;overflow:hidden;transition:box-shadow .2s}
.hub:hover{box-shadow:0 6px 20px rgba(0,0,0,.08)}
.hub .hi{aspect-ratio:4/3;background:var(--surface);display:grid;place-items:center;padding:16px}
.hub .hi img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.hub .hb{padding:14px 16px 16px;display:grid;gap:4px}
.hub h2{margin:0;font-size:20px;font-weight:800;text-transform:uppercase}
.hub p{margin:0;color:var(--muted);font-size:14px}
.hub .n{font-size:13px;font-weight:700;color:var(--brand-red)}
.hub a.stretch::after{content:"";position:absolute;inset:0}
.hub-logo .hi{aspect-ratio:3/1;background:#fff;border-bottom:1px solid var(--line)}
.hub-logo .hi img{max-height:56px}
'''


def tile(href, title, desc, n, img, unit='sản phẩm', logo=False):
    nn = f'<span class="n">{n} {unit}</span>' if n else ''
    return (f'<article class="hub{" hub-logo" if logo else ""}"><div class="hi">{img}</div>'
            f'<div class="hb"><h2><a class="stretch" href="{href}">{title}</a></h2><p>{desc}</p>{nn}</div></article>')


def page(fname, title, crumb, kicker, h1, lead, tiles, desc):
    p = R('xe-road.html')
    main = f'''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li aria-current="page">{crumb}</li></ol></nav></div>
  <section class="list-hero plain">
    <div class="container"><div class="lh-copy"><span class="kicker">{kicker}</span><h1>{h1}</h1><p>{lead}</p></div></div>
  </section>
  <div class="container"><div class="hub-grid">{"".join(tiles)}</div></div>
</main>'''
    p = re.sub(r'<title>.*?</title>', f'<title>{title} — Spinlab</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{desc}">', p, 1)
    p = re.sub(r'<main id="main".*?</main>', lambda m: main, p, 1, flags=re.S)
    p = re.sub(r'/\* Hub pages \*/.*?(?=</style>)', '', p, flags=re.S).replace('</style>', CSS + '</style>', 1)
    p = re.sub(r'\s*<meta name="product-id"[^>]*>', '', p)
    W(fname, p)


im = lambda src, alt: f'<img src="{src}" alt="{alt}" loading="lazy">'
bikes = [('xe-road.html', 'Road', 'Xe đua aero, endurance và xe road nhập môn Polygon.'),
         ('xe-mtb.html', 'MTB', 'Downhill, Enduro, Trail-AM, Cross Country và Dirt Jump.'),
         ('xe-gravel.html', 'Gravel', 'Polygon Tambora carbon và Path X đa dụng.'),
         ('xe-trial.html', 'Trial', 'Xe street trial Story Bike.')]
page('xe-dap.html', 'Xe đạp', 'Xe đạp', 'Spinlab', 'Xe đạp', 'Xe đạp Polygon và Story Bike chính hãng, phân phối bởi Spinlab.',
     [tile(f, t, d, count(f), im(first_img(f), f'Xe đạp {t}'), 'mẫu xe') for f, t, d in bikes],
     'Xe đạp Polygon và Story Bike chính hãng tại Spinlab: Road, MTB, Gravel, Trial.')
parts = [('lop-xe.html', 'Lốp xe', 'Lốp Vittoria cho road, MTB và gravel.'),
         ('tubeless.html', 'Tubeless & phụ kiện', 'Keo tự vá, chân van, băng keo vành, Air-Liner, săm và phụ kiện.'),
         ('day-cuon-tay-lai.html', 'Dây cuốn tay lái', 'Dây cuốn ghi đông và nút bịt Emume.')]
page('phu-tung.html', 'Phụ tùng', 'Phụ tùng', 'Spinlab', 'Phụ tùng', 'Lốp, phụ kiện tubeless và dây cuốn tay lái chính hãng.',
     [tile(f, t, d, count(f), im(first_img(f), t)) for f, t, d in parts],
     'Phụ tùng chính hãng tại Spinlab: lốp Vittoria, phụ kiện tubeless, dây cuốn tay lái Emume.')
idx = R('index.html')
logos = re.findall(r'<a class="brand-tile" href="([^"]+)" aria-label="Sản phẩm ([^"]+)"><span class="bt-inner">(.*?)</span></a>', idx, re.S)
blurb = {'Polygon': 'Xe đạp road, MTB, gravel, thành phố và trẻ em.', 'Vittoria': 'Lốp xe đạp và phụ kiện tubeless từ Ý.',
         'Emume': 'Dây cuốn tay lái và phụ kiện ghi đông.', 'Story Bike': 'Xe dirt jump và street trial.'}
brand_tiles = []
for href, name, inner in logos:
    f = href.lstrip('/')
    f = f if f.endswith('.html') else f + '.html'
    brand_tiles.append(tile(f, name, blurb.get(name, ''), count(f), inner, logo=True))
page('thuong-hieu.html', 'Thương hiệu', 'Thương hiệu', 'Spinlab', 'Thương hiệu', 'Các thương hiệu Spinlab phân phối chính hãng tại Việt Nam.',
     brand_tiles, 'Thương hiệu phân phối bởi Spinlab: Polygon, Vittoria, Emume, Story Bike.')
print('xe-dap.html, phu-tung.html, thuong-hieu.html')
