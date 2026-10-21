"""Build brand pages (all products of one brand) from the existing listing pages.
Usage: python3 brands.py <design-preview dir> <bikes.json>"""
import sys, os, re, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vi import VI
E = html.escape
D, DATA = sys.argv[1], sys.argv[2]
rd = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
B = {b['slug']: b for b in json.load(open(DATA, encoding='utf-8'))}

CSS = '''
/* Brand page */
.brand-nav{background:#fff;border-bottom:1px solid var(--line)}
.brand-nav ul{list-style:none;margin:0;padding:12px 0;display:flex;gap:8px;overflow-x:auto;scrollbar-width:none}
.brand-nav a{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border:1px solid var(--line);border-radius:999px;font-size:14px;font-weight:600;white-space:nowrap}
.brand-nav a:hover{border-color:var(--text)}
.brand-nav small{margin-left:6px;color:var(--muted);font-weight:500}
.brand-cat{padding:40px 0 8px;scroll-margin-top:150px}
.brand-cat+.brand-cat{border-top:1px solid var(--line)}
.bc-title{margin:0 0 4px;font-size:clamp(26px,3.2vw,38px);font-weight:800;text-transform:uppercase;line-height:1.1}
.bc-sub{margin:0 0 8px;color:var(--muted);font-size:15px}
.brand-cat .road-group{padding-top:24px}
.brand-cat .rg-head h3{margin:0;font-size:clamp(18px,2vw,22px);font-weight:800;text-transform:uppercase}
.brand-cat>.grid{margin-top:20px}
.brand-empty{margin:40px 0 56px;padding:40px 24px;border:1px dashed var(--line);border-radius:var(--radius);text-align:center}
.brand-empty h2{margin:0 0 8px;font-size:22px}
.brand-empty p{margin:0 auto 20px;max-width:52ch;color:var(--muted)}
.brand-empty .lines{list-style:none;margin:0 0 20px;padding:0;display:flex;justify-content:center;flex-wrap:wrap;gap:8px}
.brand-empty .lines li{padding:6px 14px;border-radius:999px;background:var(--surface);font-weight:600;font-size:14px}
.brand-empty .cta{display:flex;justify-content:center;flex-wrap:wrap;gap:12px}
.list-hero.plain{background:var(--text)}
'''


def shell(src, title, desc, crumb, hero, body):
    p = rd(src)
    p = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{E(desc)}">', p, 1)
    if '/* Brand page */' not in p:
        p = p.replace('</style>', CSS + '</style>', 1)
    if '.road-group{' not in p:
        rg = '\n'.join(l for l in rd('xe-road.html').split('\n') if l.startswith(('.road-group', '.rg-')))
        p = p.replace('</style>', rg + '\n</style>', 1)
    main = (f'<main id="main" class="pdp listing">\n'
            f'  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li>'
            f'<li><a href="thuong-hieu.html">Thương hiệu</a></li><li aria-current="page">{E(crumb)}</li></ol></nav></div>\n'
            f'{hero}\n{body}\n</main>')
    p = re.sub(r'<main id="main".*?</main>', lambda m: main, p, 1, flags=re.S)
    # listing-page scripts (tabs / tire filter) are not needed on brand pages
    p = re.sub(r'\n// (Tire listing|Open the discipline tab)[^\n]*\n.*?\}\)\(\);\n', '\n', p, flags=re.S)
    return p


def hero(img, alt, kicker, h1, text):
    im = f'<img src="{E(img)}" alt="{E(alt)}">' if img else ''
    return (f'  <section class="list-hero{"" if img else " plain"}">\n    {im}\n'
            f'    <div class="container"><div class="lh-copy"><span class="kicker">{E(kicker)}</span><h1>{E(h1)}</h1><p>{E(text)}</p></div></div>\n  </section>')


def nav(cats):
    return ('  <nav class="brand-nav" aria-label="Danh mục sản phẩm"><div class="container"><ul>' +
            ''.join(f'<li><a href="#{cid}">{E(t)}<small>{n}</small></a></li>' for cid, t, n in cats) + '</ul></div></nav>')


def cat(cid, title, sub, inner):
    return (f'  <section class="brand-cat" id="{cid}"><div class="container"><h2 class="bc-title">{E(title)}</h2>'
            + (f'<p class="bc-sub">{E(sub)}</p>' if sub else '') + f'{inner}</div></section>')


def groups_from(page, panel=None):
    """road-group sections of a listing page (optionally one MTB panel), with h2 demoted to h3."""
    p = rd(page)
    if panel:
        a = p.index(f'id="panel-{panel}"')
        z = p.find('id="panel-', a + 10)
        p = p[a:z if z > 0 else len(p)]
    gs = re.findall(r'<section class="road-group">.*?</section>', p, re.S)
    return [g.replace('<h2>', '<h3>').replace('</h2>', '</h3>') for g in gs]


def ncards(html_):
    return html_.count('<article class="p-card"')


def bike_card(slug, desc):
    b, v = B[slug], VI[slug]
    nm = b['name'].replace('RELIC20', 'RELIC 20').replace(' with UDH', '')
    img = b['colors'][0]['images'][0] if b['colors'] and b['colors'][0]['images'] else ''
    return (f'<article class="p-card"><div class="p-img"><img src="{E(img)}" alt="Polygon {E(nm)}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">Polygon · {E(v["series"])}</span><h3 class="p-name"><a class="stretch" href="{v["file"]}.html">{E(nm)}</a></h3>'
            f'<p class="p-desc">{E(desc)}</p><span class="p-price">1.980.000₫</span></div></article>')


# ---------- Polygon ----------
pc = []
road = ''.join(groups_from('xe-road.html'))
pc.append(('road', 'Road', 'Xe đua aero, endurance và xe road nhập môn.', road))
for k, t, s in [('dh', 'Downhill', 'Hành trình 200mm cho đường đổ đèo và giải đua downhill.'),
                ('enduro', 'Enduro', 'Leo được, đổ đèo mạnh — hành trình 170mm.'),
                ('trail', 'Trail-AM', 'Cân bằng giữa leo dốc và đổ đèo.'),
                ('xc', 'Cross Country', 'Nhẹ, đạp nhanh, leo dốc hiệu quả.')]:
    pc.append((k, t, s, ''.join(groups_from('xe-mtb.html', k))))
other = [('gravel', 'Gravel', 'Xe đa địa hình cho đường nhựa lẫn đường đất.', [('tambora-9-axs', 'SRAM Force XPLR AXS 1x13'), ('tambora-7-di2', 'Shimano GRX Di2 1x12'), ('tambora-6', 'Shimano GRX 2x12'), ('tambora-4', 'Shimano CUES 2x10'), ('path-x5', 'Gravel · Adventure')]),
         ('city', 'City - Hybrid', 'Đi làm, đi phố và dạo chơi cuối tuần.', [('heist-7', 'Hybrid · Shimano Deore 1x12'), ('heist-5', 'Hybrid · Shimano CUES 1x'),
                                                                             ('heist-2', 'Hybrid · Shimano Altus 1x8'), ('heist-x7', 'Hybrid · Đi phố'),
                                                                             ('path-4', 'City · Phuộc carbon'), ('path-3', 'City · Shimano CUES 1x9'),
                                                                             ('path-2', 'City · Shimano Altus 1x8'), ('cleo-2', 'Xe dạo phố')])]
for k, t, s, items in other:
    items = [(sl, d) for sl, d in items if sl in VI and sl in B]
    if items:
        pc.append((k, t, s, '<div class="grid">' + ''.join(bike_card(sl, d) for sl, d in items) + '</div>'))
pc = [c for c in pc if ncards(c[3])]
total = sum(ncards(c[3]) for c in pc)
body = nav([(k, t, ncards(h)) for k, t, s, h in pc]) + '\n' + '\n'.join(cat(k, t, s, h) for k, t, s, h in pc)
out = shell('xe-mtb.html', 'Polygon — Toàn bộ xe đạp — Spinlab', f'Toàn bộ {total} mẫu xe đạp Polygon chính hãng tại Spinlab: Road, MTB, Gravel, xe thành phố và xe trẻ em.',
            'Polygon', hero('https://media.polygonbikes.com/wp-content/uploads/2024/11/15080846/design-asset-product-highlight-website-polygon-siskiu-t-3.jpg',
                            'Xe đạp Polygon trên đường mòn', 'Thương hiệu', 'Polygon', f'{total} mẫu xe đạp chính hãng — từ xe đua road, xe địa hình đến xe thành phố và xe trẻ em. Phân phối bởi Spinlab.'), body)
open(os.path.join(D, 'thuong-hieu-polygon.html'), 'w', encoding='utf-8').write(out)
print('polygon', total, [(k, ncards(h)) for k, t, s, h in pc])

# ---------- Vittoria ----------
lp = rd('lop-xe.html')
cards = re.findall(r'<article class="p-card" data-type="([a-z]+)".*?</article>', lp, re.S)
full = re.findall(r'(<article class="p-card" data-type="[a-z]+".*?</article>)', lp, re.S)
vc = []
for k, t, s in [('road', 'Lốp Road', 'Lốp đua và tập luyện cho xe đường trường.'), ('mtb', 'Lốp MTB', 'Cross country, trail và enduro.'),
                ('gravel', 'Lốp Gravel', 'Dòng Terreno PRO và Terreno Endurance cho mọi loại địa hình gravel.'),
                ('dirtjump', 'Lốp DirtJump', 'BMX, dirt jump và street.')]:
    h = ''.join(c for t_, c in zip(cards, full) if t_ == k)
    if h:
        vc.append((k, t, s, '<div class="grid">' + h + '</div>'))
tl = re.findall(r'<article class="p-card" data-type="[a-z-]+".*?</article>', rd('tubeless.html'), re.S)
if tl:
    vc.append(('tubeless', 'Tubeless', 'Keo tự vá, chân van, băng keo vành, Air-Liner, săm và phụ kiện.', '<div class="grid">' + ''.join(tl) + '</div>'))
total = sum(ncards(c[3]) for c in vc)
body = nav([(k, t.replace('Lốp ', ''), ncards(h)) for k, t, s, h in vc]) + '\n' + '\n'.join(cat(k, t, s, h) for k, t, s, h in vc)
out = shell('lop-xe.html', 'Vittoria — Toàn bộ sản phẩm — Spinlab', f'Toàn bộ {total} sản phẩm Vittoria chính hãng tại Spinlab: lốp Road, MTB, Gravel, DirtJump và phụ kiện tubeless.',
            'Vittoria', hero('https://vittoria.com/cdn/shop/files/Banner_HERO_Horizontal_3_69510693-5265-4d5e-95ae-4706d0cb7fdd.webp?width=1920',
                             'Nhóm người đạp xe gravel trên đường đất', 'Thương hiệu', 'Vittoria', f'{total} sản phẩm chính hãng — lốp xe và phụ kiện tubeless từ thương hiệu hàng đầu nước Ý. Phân phối bởi Spinlab.'), body)
open(os.path.join(D, 'thuong-hieu-vittoria.html'), 'w', encoding='utf-8').write(out)
print('vittoria', total, [(k, ncards(h)) for k, t, s, h in vc])

# ---------- Story Bike ----------
st = re.findall(r'<section class="road-group" id="(street|competition)">.*?<div class="grid">(.*?)</div></section>', rd('xe-trial.html'), re.S)
sc = [(k, {'street': 'Street trial', 'competition': 'Competition'}[k], '', '<div class="grid">' + h + '</div>') for k, h in st if ncards(h)]
dj = ''.join(re.findall(r'<div class="grid">(.*?)</div></section>', rd('xe-mtb.html')[rd('xe-mtb.html').index('id="panel-dj"'):], re.S))
if ncards(dj):
    sc.insert(0, ('dirt-jump', 'Dirt Jump', '', '<div class="grid">' + dj + '</div>'))
if sc:
    total = sum(ncards(c[3]) for c in sc)
    body = nav([(k, t, ncards(h)) for k, t, s, h in sc]) + '\n' + '\n'.join(cat(k, t, s, h) for k, t, s, h in sc)
    out = shell('xe-road.html', 'Story Bike — Xe dirt jump & trial — Spinlab', 'Xe đạp dirt jump và trial Story Bike chính hãng tại Spinlab.', 'Story Bike',
                hero('img/story/continue-silver-3.jpg', 'Rider bên xe trial Story Continue', 'Thương hiệu', 'Story Bike',
                     f'{total} mẫu xe dirt jump và street trial chính hãng. Phân phối bởi Spinlab.'), body)
    open(os.path.join(D, 'thuong-hieu-story-bike.html'), 'w', encoding='utf-8').write(out)
    print('story', total)

# ---------- Emume ----------
dc = rd('day-cuon-tay-lai.html')
ec = [(k, t, sub, '<div class="grid">' + h + '</div>') for k, t, sub, h in
      re.findall(r'<section class="brand-cat" id="([a-z-]+)"><div class="container"><h2 class="bc-title">([^<]+)</h2><p class="bc-sub">([^<]*)</p><div class="grid">(.*?)</div></div></section>', dc, re.S)]
if ec:
    total = sum(ncards(c[3]) for c in ec)
    body = nav([(k, html.unescape(t), ncards(h)) for k, t, s_, h in ec]) + '\n' + '\n'.join(cat(k, html.unescape(t), html.unescape(s_), h) for k, t, s_, h in ec)
    out = shell('tubeless.html', 'Emume — Dây cuốn tay lái & phụ kiện — Spinlab', 'Dây cuốn tay lái và phụ kiện Emume chính hãng tại Spinlab.', 'Emume',
                hero('', '', 'Thương hiệu', 'Emume',
                     f'{total} sản phẩm dây cuốn tay lái và phụ kiện chính hãng. Phân phối bởi Spinlab.'), body)
    open(os.path.join(D, 'thuong-hieu-emume.html'), 'w', encoding='utf-8').write(out)
    print('emume', total)

# ---------- Brands without products online yet ----------
EMPTY = []
for f, name, kind, text, lines in EMPTY:
    body = ('  <div class="container"><div class="brand-empty"><h2>Sản phẩm đang được cập nhật</h2>'
            f'<p>Spinlab đang cập nhật danh sách sản phẩm {E(name)} lên website. Liên hệ để được tư vấn và báo hàng có sẵn.</p>'
            '<ul class="lines">' + ''.join(f'<li>{E(l)}</li>' for l in lines) + '</ul>'
            '<div class="cta"><a class="btn btn-primary" href="tel:0399337533">Gọi 0399 337 533</a>'
            '<a class="btn btn-zalo" href="https://zalo.me/0399337533" target="_blank" rel="noopener">Chat Zalo</a></div></div></div>')
    out = shell('xe-road.html', f'{name} — {kind} — Spinlab', f'{name} chính hãng tại Spinlab. {text}', name,
                hero('', '', 'Thương hiệu', name, text), body)
    open(os.path.join(D, f), 'w', encoding='utf-8').write(out)
    print(f)
