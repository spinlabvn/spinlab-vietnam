"""Hub pages that replace the old 'index.html#hot' / '#brands' links:
xe-dap.html (bike categories), phu-tung.html (parts categories), thuong-hieu.html (brands);
plus the main-menu pages huong-dan.html (guides: size chart from bikes.json) and su-kien.html (events).
Counts are read from the listing pages, so run after the listings are up to date:
    python3 tools/build_hubs.py
"""
import collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda f: open(os.path.join(ROOT, f), encoding='utf-8').read()
W = lambda f, s: open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)
count = lambda f: R(f).count('<article class="p-card"') if os.path.exists(os.path.join(ROOT, f)) else 0
first_img = lambda f: (re.search(r'<article class="p-card".*?<img src="([^"]+)"', R(f), re.S) or [None, ''])[1]

CSS = '''/* Hub pages */
.hub-grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin:24px 0 56px}
.hub{position:relative;display:flex;flex-direction:column;border:1px solid var(--line);border-radius:var(--radius);background:#fff;overflow:hidden;transition:box-shadow .2s}
.hub:hover{box-shadow:0 6px 20px rgba(0,0,0,.08)}
.hub .hi{position:relative;aspect-ratio:4/3;background:var(--surface);display:grid;place-items:center;padding:16px}
.hub:not(.hub-logo) .hi img{position:absolute;inset:16px;width:calc(100% - 32px);height:calc(100% - 32px);object-fit:contain;mix-blend-mode:multiply;transition:transform .3s}
.hub:not(.hub-logo):hover .hi img{transform:scale(1.04)}
.hub .hb{flex:1;padding:14px 16px 16px;display:flex;flex-direction:column;gap:4px}
.hub h2{margin:0;font-size:20px;font-weight:800;text-transform:uppercase}
.hub p{margin:0;color:var(--muted);font-size:14px}
.hub .n{margin-top:auto;padding-top:6px;font-size:13px;font-weight:700;color:var(--brand-red)}
.hub a.stretch::after{content:"";position:absolute;inset:0}
.hub-logo .hi{aspect-ratio:3/1;background:#fff;border-bottom:1px solid var(--line)}
.guide{max-width:860px;margin:8px 0 56px}
.guide h2{font-size:24px;margin:40px 0 8px}
.guide>p{color:var(--muted);margin:0 0 16px}
.size-grid{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.size-grid caption small{display:block;font-weight:400;color:var(--muted);font-size:13px}
.tips{margin:0;padding-left:20px;display:grid;gap:8px}
.guide .cta,.events .cta{display:flex;flex-wrap:wrap;gap:10px}
.events{margin:40px 0 56px;padding:40px 24px;border:1px dashed var(--line);border-radius:var(--radius);text-align:center}
.events h2{margin:0 0 8px;font-size:22px}
.events p{margin:0 auto 20px;max-width:52ch;color:var(--muted)}
.events .cta{justify-content:center}
'''


def tile(href, title, desc, n, img, unit='sản phẩm', logo=False):
    nn = f'<span class="n">{n} {unit}</span>' if n else ''
    return (f'<article class="hub{" hub-logo" if logo else ""}"><div class="hi">{img}</div>'
            f'<div class="hb"><h2><a class="stretch" href="{href}">{title}</a></h2><p>{desc}</p>{nn}</div></article>')


def page(fname, title, crumb, kicker, h1, lead, tiles, desc, body=None):
    p = R('xe-road.html')
    main = f'''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li aria-current="page">{crumb}</li></ol></nav></div>
  <section class="list-hero plain">
    <div class="container"><div class="lh-copy"><span class="kicker">{kicker}</span><h1>{h1}</h1><p>{lead}</p></div></div>
  </section>
  {body or f'<div class="container"><div class="hub-grid">{"".join(tiles)}</div></div>'}
</main>'''
    p = re.sub(r'<title>.*?</title>', f'<title>{title} — Spinlab</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{desc}">', p, 1)
    p = re.sub(r'<main id="main".*?</main>', lambda m: main, p, 1, flags=re.S)
    p = re.sub(r'/\* Hub pages \*/.*?(?=</style>)', '', p, flags=re.S).replace('</style>', CSS + '</style>', 1)
    p = re.sub(r'\s*<meta name="product-id"[^>]*>', '', p)
    W(fname, p)


im = lambda src, alt: f'<img src="{src}" alt="{alt}" loading="lazy">'
# square photos cropped to the 4:3 tile so every bike shows at the same size
HUB_IMG = {'xe-trial.html': 'img/story/continue-yellow-43.jpg'}
bikes = [('xe-road.html', 'Road', 'Xe đua aero, endurance và xe road nhập môn Polygon.'),
         ('xe-mtb.html', 'MTB', 'Downhill, Enduro, Trail-AM, Cross Country và Dirt Jump.'),
         ('xe-gravel.html', 'Gravel', 'Polygon Path X đa dụng cho phố và đường đất.'),
         ('xe-city.html', 'City - Hybrid', 'Polygon Heist và Path cho đi làm, đi phố.'),
         ('xe-trial.html', 'Trial', 'Xe street trial Story Bike.')]
page('xe-dap.html', 'Xe đạp', 'Xe đạp', 'Spinlab', 'Xe đạp', 'Xe đạp Polygon và Story Bike chính hãng, phân phối bởi Spinlab.',
     [tile(f, t, d, count(f), im(HUB_IMG.get(f) or first_img(f), f'Xe đạp {t}'), 'mẫu xe') for f, t, d in bikes],
     'Xe đạp Polygon và Story Bike chính hãng tại Spinlab: Road, MTB, Gravel, City - Hybrid, Trial.')
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

# ---------- Hướng dẫn: size chart by category, from the geometry tables of the bikes on the site ----------
sys.path.insert(0, os.path.join(ROOT, 'tools', 'generators'))
from vi import VI  # noqa: E402
BK = {b['slug']: b for b in json.load(open(os.path.join(ROOT, 'tools', 'generators', 'bikes.json'), encoding='utf-8'))}
GROUPS = [('Xe Road', 'Polygon Helios, Strattos', lambda v, s: v['cat'] == 'road'),
          ('Xe MTB', 'Downhill, Enduro, Trail, Cross Country', lambda v, s: v['cat'] in ('dh', 'enduro', 'trail', 'xc')),
          ('Heist (City - Hybrid)', 'Heist 2, 5, 7', lambda v, s: v['series'] == 'Heist'),
          ('Path (City & Gravel)', 'Path 2, 3, 4, Path X5', lambda v, s: v['series'] in ('Path', 'Path X'))]
ORDER = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
tables = []
for title, sub, keep in GROUPS:
    agg = collections.defaultdict(collections.Counter)
    for slug, v in VI.items():
        g = BK.get(slug, {}).get('geometry')
        if v.get('brand', 'Polygon') != 'Polygon' or not g or not keep(v, slug):
            continue
        for r in g['rows']:
            if r['label'] == 'Height':
                for sz, val in zip(g['sizes'], r['values']):
                    if sz in ORDER:
                        agg[sz][val] += 1
    if agg:
        rows = ''.join(f'<tr><th scope="row">{sz}</th><td>{agg[sz].most_common(1)[0][0]} cm</td></tr>' for sz in ORDER if sz in agg)
        tables.append(f'<div class="table-wrap"><table><caption>{title}<small>{sub}</small></caption><thead><tr><th scope="col">Size</th>'
                      f'<th scope="col">Chiều cao người đạp</th></tr></thead><tbody>{rows}</tbody></table></div>')
CTA = ('<div class="cta"><a class="btn btn-primary" href="tel:0399337533">Gọi 0399 337 533</a>'
       '<a class="btn btn-zalo" href="https://zalo.me/0399337533" target="_blank" rel="noopener">Chat Zalo</a>'
       '<a class="btn btn-outline" href="/dai-ly">Tìm đại lý</a></div>')
guide = f'''<div class="container"><div class="guide">
  <h2 id="chon-size">Chọn size xe theo chiều cao</h2>
  <p>Bảng tham khảo theo khuyến nghị của Polygon cho các mẫu xe Spinlab đang phân phối. Mỗi trang sản phẩm có bảng kích thước khung chi tiết của riêng mẫu xe đó.</p>
  <div class="size-grid">{"".join(tables)}</div>
  <h2>Khi chiều cao nằm giữa hai size</h2>
  <ul class="tips">
    <li>Chọn size nhỏ hơn nếu bạn thích xe linh hoạt, dễ xoay trở; chọn size lớn hơn nếu bạn ưu tiên sự ổn định khi đi đường dài.</li>
    <li>Người có chân dài hơn so với thân thường hợp size lớn hơn; thân dài, chân ngắn thường hợp size nhỏ hơn.</li>
    <li>Chiều cao yên, độ dài pô tăng và vị trí ghi đông có thể tinh chỉnh thêm sau khi chọn đúng size khung.</li>
  </ul>
  <h2>Cần tư vấn trực tiếp?</h2>
  <p>Đội ngũ kỹ thuật Spinlab tư vấn chọn size, dòng xe, lốp và phụ kiện phù hợp với bạn — hoặc ghé đại lý gần nhất để thử xe.</p>
  {CTA}
</div></div>'''
page('huong-dan.html', 'Hướng dẫn', 'Hướng dẫn', 'Spinlab', 'Hướng dẫn', 'Chọn size xe theo chiều cao và tư vấn kỹ thuật từ đội ngũ Spinlab.',
     [], 'Hướng dẫn chọn size xe đạp Polygon theo chiều cao và tư vấn kỹ thuật từ Spinlab.', body=guide)

# ---------- Sự kiện: no event announced yet ----------
events = ('<div class="container"><div class="events"><h2>Sự kiện sắp tới đang được cập nhật</h2>'
          '<p>Lịch chạy thử xe, giải đua và các buổi gặp gỡ cộng đồng của Spinlab sẽ được đăng tại đây. Theo dõi Spinlab trên Facebook, Instagram và YouTube để nhận thông báo sớm nhất.</p>'
          '<div class="cta"><a class="btn btn-primary" href="https://www.facebook.com/profile.php?id=61573821032401" target="_blank" rel="noopener">Facebook Spinlab</a>'
          '<a class="btn btn-outline" href="https://www.instagram.com/spinlabvn/" target="_blank" rel="noopener">Instagram</a>'
          '<a class="btn btn-outline" href="https://www.youtube.com/@Spinlabvn" target="_blank" rel="noopener">YouTube</a></div></div></div>')
page('su-kien.html', 'Sự kiện', 'Sự kiện', 'Spinlab', 'Sự kiện', 'Chạy thử xe, giải đua và hoạt động cộng đồng cùng Spinlab.',
     [], 'Sự kiện xe đạp của Spinlab: chạy thử xe, giải đua và hoạt động cộng đồng.', body=events)
print('xe-dap.html, phu-tung.html, thuong-hieu.html, huong-dan.html, su-kien.html')
