"""Dealer network page dai-ly.html (Bắc / Trung / Nam), built on xe-road.html shell.
Real dealer list (no sample data); a region without dealers shows a hotline note. Usage: python3 daily.py <design-preview dir>"""
import sys, os, re, html
from urllib.parse import quote
E = html.escape
D = sys.argv[1]
HOT = '0399 337 533'

REGIONS = [
 ('mien-bac', 'Miền Bắc', [
   dict(name='Tuấn Biker', city='Hà Nội', addr='79 Đường 23, KĐT Thành Phố Giao Lưu, Cổ Nhuế 1, Bắc Từ Liêm, Hà Nội', phone='0888967777',
        brands=['Emume', 'Vittoria']),
   dict(name='Bon Bon Bike', city='Hải Phòng', addr='18 P. Thế Lữ, Hồng Bàng, Hải Phòng', phone='0936635489', brands=['Emume', 'Vittoria'])]),
 ('mien-trung', 'Miền Trung', []),
 ('mien-nam', 'Miền Nam', [
   dict(name='Spinlab Việt Nam', city='TP. Hồ Chí Minh', addr='13 đường 14, khu phố 4, phường An Khánh, TP. Hồ Chí Minh',
        phone='0399337533', brands=['Polygon', 'Vittoria', 'Emume', 'Story Bike'], hq=True),
   dict(name='HP Cycle', city='TP. Hồ Chí Minh', addr='13 đường số 11, KDC Him Lam 6A, xã Bình Hưng, TP. Hồ Chí Minh', phone='0932019931'),
   dict(name='644 Store', city='TP. Hồ Chí Minh', addr='644 Đ. Cách Mạng Tháng Tám, Thủ Dầu Một, TP. Hồ Chí Minh', phone='0943435455'),
   dict(name='Phú Quý Bike', city='TP. Hồ Chí Minh', addr='106/14 Vạn Kiếp, phường Gia Định, TP. Hồ Chí Minh', phone='0319204022'),
   dict(name='2Bike', city='TP. Hồ Chí Minh', addr='54B Nguyễn Bỉnh Khiêm, Tân Định, TP. Hồ Chí Minh', phone='0936313213')]),
]

CSS = '''
/* Dealer page */
.dealer-grid{display:grid;gap:16px;grid-template-columns:1fr;margin-top:20px}
@media (min-width:768px){.dealer-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1024px){.dealer-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.dealer{display:flex;flex-direction:column;gap:10px;padding:20px;border:1px solid var(--line);border-radius:var(--radius);background:#fff}
.dealer.hq{border-color:var(--brand-red);box-shadow:inset 0 0 0 1px var(--brand-red)}
.dealer .d-city{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-red)}
.dealer h3{margin:0;font-size:18px;line-height:1.3}
.dealer .d-tag{display:inline-block;margin-left:6px;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:700;text-transform:uppercase;vertical-align:middle;background:var(--surface);color:var(--muted)}
.dealer .d-tag.main{background:var(--brand-yellow);color:var(--brand-red)}
.dealer dl{margin:0;display:grid;gap:6px;font-size:14px}
.dealer dl div{display:grid;grid-template-columns:88px 1fr;gap:8px}
.dealer dt{color:var(--muted)}
.dealer dd{margin:0;font-weight:500}
.dealer .d-brands{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.dealer .d-brands li{font-size:12px;font-weight:600;padding:4px 8px;border-radius:3px;background:var(--surface)}
.dealer .d-cta{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto;padding-top:6px}
.dealer .d-cta .btn{min-height:44px;padding:0 16px;font-size:13px}
.dealer-note{margin:12px 0 0;padding:12px 16px;border-radius:var(--radius);background:#FFF7D6;font-size:14px}
.dealer-empty{margin-top:20px;padding:24px;border:1px dashed var(--line);border-radius:var(--radius);display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between}
.dealer-empty p{margin:0;max-width:60ch;color:var(--muted)}
'''


def fmt_phone(n):
    return f'{n[:4]} {n[4:7]} {n[7:]}' if len(n) == 10 else n


def card(d):
    """Real dealers carry their own phone; sample cards fall back to the Spinlab hotline. Hours/brands only shown when known."""
    tag = '<span class="d-tag main">Showroom</span>' if d.get('hq') else ('<span class="d-tag">Dữ liệu mẫu</span>' if d.get('sample') else '')
    real = not d.get('sample')
    maps = 'https://www.google.com/maps/search/?api=1&query=' + quote(d['addr'] if real else 'Spinlab ' + d['city'])
    tel = d.get('phone', '0399337533')
    rows = f'<div><dt>Địa chỉ</dt><dd>{E(d["addr"])}</dd></div><div><dt>Điện thoại</dt><dd><a href="tel:{tel}">{fmt_phone(tel)}</a></dd></div>'
    hours = d.get('hours') or (None if real else '8:00 – 20:00, thứ Hai – Chủ nhật')
    if hours:
        rows += f'<div><dt>Giờ mở cửa</dt><dd>{E(hours)}</dd></div>'
    brands = ('<ul class="d-brands" aria-label="Thương hiệu có bán">' + ''.join(f'<li>{E(b)}</li>' for b in d['brands']) + '</ul>') if d.get('brands') else ''
    return (f'<article class="dealer{" hq" if d.get("hq") else ""}"><span class="d-city">{E(d["city"])}</span>'
            f'<h3>{E(d["name"])}{tag}</h3><dl>{rows}</dl>{brands}'
            f'<div class="d-cta"><a class="btn btn-primary" href="tel:{tel}">Gọi ngay</a>'
            f'<a class="btn btn-outline" href="{E(maps)}" target="_blank" rel="noopener">Chỉ đường</a></div></article>')


p = open(os.path.join(D, 'xe-road.html'), encoding='utf-8').read()
brand_css = re.search(r'/\* Brand page \*/.*?(?=</style>)', open(os.path.join(D, 'thuong-hieu-vittoria.html'), encoding='utf-8').read(), re.S).group(0)
p = p.replace('</style>', brand_css + CSS + '</style>', 1)
total = sum(len(ds) for _, _, ds in REGIONS)
nav = ('  <nav class="brand-nav" aria-label="Khu vực"><div class="container"><ul>' +
       ''.join(f'<li><a href="#{rid}">{E(t)}' + (f'<small>{len(ds)}</small>' if ds else '') + '</a></li>' for rid, t, ds in REGIONS) + '</ul></div></nav>')
EMPTY = ('<div class="dealer-empty"><p>Spinlab đang mở rộng hệ thống đại lý tại khu vực này. Gọi hotline để được tư vấn, đặt hàng và giao tận nơi.</p>'
         f'<a class="btn btn-yellow" href="tel:0399337533">Gọi {HOT}</a></div>')
secs = ''.join(f'  <section class="brand-cat" id="{rid}"><div class="container"><h2 class="bc-title">{E(t)}</h2>'
               + (f'<p class="bc-sub">{len(ds)} điểm bán</p><div class="dealer-grid">{"".join(card(d) for d in ds)}</div>' if ds else '<p class="bc-sub">Đang cập nhật</p>' + EMPTY)
               + '</div></section>\n' for rid, t, ds in REGIONS)
main = f'''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li aria-current="page">Hệ thống đại lý</li></ol></nav></div>
  <section class="list-hero">
    <img src="https://media.polygonbikes.com/wp-content/uploads/2026/01/22110900/plg-strattos-c-header.jpg" alt="Người đạp xe road Polygon trên đường">
    <div class="container"><div class="lh-copy"><span class="kicker">Spinlab</span><h1>Hệ thống đại lý</h1><p>Mua xe đạp Polygon, lốp Vittoria và phụ kiện chính hãng tại các đại lý Spinlab trên khắp ba miền.</p></div></div>
  </section>
{nav}
{secs}</main>'''
p = re.sub(r'<title>.*?</title>', '<title>Hệ thống đại lý — Spinlab</title>', p, 1, flags=re.S)
p = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Hệ thống đại lý Spinlab tại miền Bắc, miền Trung và miền Nam — mua xe đạp Polygon, lốp Vittoria chính hãng gần bạn.">', p, 1)
p = re.sub(r'<main id="main".*?</main>', lambda m: main, p, 1, flags=re.S)
open(os.path.join(D, 'dai-ly.html'), 'w', encoding='utf-8').write(p)
print('dai-ly.html', total)
