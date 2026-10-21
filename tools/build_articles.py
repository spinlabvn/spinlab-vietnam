"""Articles: the "Tin tức" and "Hướng dẫn" menus.

Each entry in ARTICLES becomes its own page (<slug>.html); tin-tuc.html and huong-dan.html list the articles of
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
PRICES = json.load(open(os.path.join(ROOT, 'data', 'bike-prices.json'), encoding='utf-8'))['prices']
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
GROUPS = [('Xe Road', 'Polygon Helios, Strattos', lambda v: v['cat'] == 'road'),
          ('Xe MTB', 'Downhill, Enduro, Trail, Cross Country', lambda v: v['cat'] in ('dh', 'enduro', 'trail', 'xc')),
          ('Heist (City - Hybrid)', 'Heist 2, 5, 7', lambda v: v['series'] == 'Heist'),
          ('Path (City & Gravel)', 'Path 2, 3, 4, Path X5', lambda v: v['series'] in ('Path', 'Path X'))]
ORDER = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
tables = []
for title, sub, keep in GROUPS:
    agg = collections.defaultdict(collections.Counter)
    for slug, v in VI.items():
        g = BK.get(slug, {}).get('geometry')
        if v.get('brand', 'Polygon') != 'Polygon' or not g or not keep(v):
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

# ---------- Strattos C: builds from bikes.json + retail prices ----------
SC = [('2026-strattos-c9-axs-road-bike', 'SRAM Force AXS E1 2x12, điện tử không dây', 'LINC Alpha Carbon 35mm'),
      ('2026-strattos-c8-di2-road-bike', 'Shimano Ultegra Di2 2x12', 'Polygon WR4 Carbon'),
      ('2026-strattos-c7-di2-road-bike', 'Shimano 105 Di2 2x12', 'Polygon WR4 Carbon')]
sc_rows = ''.join(f'<tr><th scope="row"><a href="{VI[s]["file"]}.html">{E(BK[s]["name"])}</a></th><td>{g}</td><td>{w}</td>'
                  f'<td>{vnd(PRICES[VI[s]["file"] + ".html"]) if VI[s]["file"] + ".html" in PRICES else "Liên hệ"}</td></tr>' for s, g, w in SC)

ARTICLES = [
    dict(slug='tin-tuc-polygon-strattos-c', cat='tin-tuc', tag='Sản phẩm mới', date='2026-10-21',
         title='Polygon Strattos C: road bike endurance thế hệ mới',
         lead='Khung carbon ACX êm ái, lốp tới 34mm và buồng lái LINC bán tích hợp — Strattos C được Polygon thiết kế cho những cung đường dài cả ngày. Ba phiên bản C7, C8 và C9 đã có mặt tại Spinlab.',
         image='https://media.polygonbikes.com/wp-content/uploads/2026/01/22110900/plg-strattos-c-header.jpg', thumb='https://media.polygonbikes.com/wp-content/uploads/2026/02/23154155/Header-Strattos-C-by-Velo-450x300.jpg',
         body=f'''
<p>Strattos C là dòng road bike <strong>endurance</strong> mới của Polygon, dành cho những chuyến đi dài nơi sự thoải mái quan trọng không kém tốc độ. Thay vì hình học thi đấu gò bó, Strattos C cho tư thế ngồi thả lỏng hơn, khung hấp thụ rung động tốt và đủ chỗ cho lốp bản lớn — một chiếc xe để đạp cả ngày mà vẫn nhanh.</p>
<h2>Khung carbon ACX được tinh chỉnh cho sự êm ái</h2>
<p>Khung và phuộc Strattos C làm từ carbon ACX của Polygon, với cách xếp lớp sợi được điều chỉnh để cân bằng giữa trọng lượng nhẹ và khả năng giảm rung. Gióng sau hạ thấp (dropped seat stays) giúp phần đuôi xe hấp thụ rung động mặt đường, trong khi vùng trục giữa vẫn đủ cứng để truyền lực đạp hiệu quả.</p>
<figure><img src="https://media.polygonbikes.com/wp-content/uploads/2025/12/03115939/AZZ_1147-803x488.jpg" alt="Polygon Strattos C trên đường" loading="lazy"></figure>
<h2>Lốp tới 34mm cho mọi mặt đường</h2>
<p>Khoảng hở lốp tới <strong>34mm</strong> cho phép chạy lốp bản lớn ở áp suất thấp hơn để tăng độ bám và sự êm ái — dù là đường nhựa phẳng, đường bê tông xấu hay đoạn đường đất nhẹ. Cả ba phiên bản xuất xưởng với lốp Schwalbe One Addix TLE 700x28C và vành sẵn băng keo tubeless.</p>
<h2>Buồng lái LINC bán tích hợp và pát SRAM UDH</h2>
<p>Ghi đông carbon LINC đi dây âm hoàn toàn cho vẻ ngoài gọn gàng và khí động học, nhưng vẫn giữ khả năng tinh chỉnh như hệ ghi đông – pô tăng rời, giúp việc bảo dưỡng dễ dàng hơn. Khung dùng pát đề chuẩn <strong>SRAM UDH</strong>: tương thích bộ truyền động SRAM Transmission đời mới và dễ tìm phụ tùng thay thế.</p>
<h2>Ba phiên bản tại Spinlab</h2>
<div class="table-wrap"><table><thead><tr><th scope="col">Phiên bản</th><th scope="col">Bộ truyền động</th><th scope="col">Bộ vành</th><th scope="col">Giá bán lẻ</th></tr></thead><tbody>{sc_rows}</tbody></table></div>
<p>Cả ba phiên bản dùng khung ACX All-Round, phanh đĩa dầu, đĩa phanh 160mm và có 7 size từ XXS đến XXL.</p>
<h2>Strattos C dành cho ai?</h2>
<ul>
<li>Người đạp đường dài, tour cuối tuần, gran fondo — cần sự thoải mái suốt nhiều giờ trên yên.</li>
<li>Người muốn một chiếc road carbon hiệu năng cao nhưng không cần tư thế thi đấu như dòng aero Helios A.</li>
<li>Người hay gặp đường xấu, muốn chạy lốp bản lớn để êm và bám hơn.</li>
</ul>
<p>Chưa chắc chọn size nào? Xem <a href="huong-dan-chon-size-xe-dap.html">hướng dẫn chọn size xe theo chiều cao</a> hoặc liên hệ Spinlab để được tư vấn và đặt lịch xem xe.</p>
''', products=[('polygon-strattos-c9.html', 'SRAM Force AXS'), ('polygon-strattos-c8.html', 'Shimano Ultegra Di2'), ('polygon-strattos-c7.html', 'Shimano 105 Di2')]),

    dict(slug='huong-dan-ap-suat-lop-tubeless', cat='huong-dan', tag='Kỹ thuật lốp', date='2026-10-21',
         title='Áp suất lốp tubeless: bơm bao nhiêu là đúng?',
         lead='Lốp tubeless cho phép chạy áp suất thấp hơn lốp có săm — êm hơn, bám hơn mà không lo thủng do kẹp săm. Nhưng bơm bao nhiêu là vừa? Dưới đây là cách chọn áp suất và bảng điểm khởi đầu tham khảo.',
         image='https://vittoria.com/cdn/shop/files/Banner_HERO_Horizontal_3_69510693-5265-4d5e-95ae-4706d0cb7fdd.webp?width=1600', thumb='https://vittoria.com/cdn/shop/files/Banner_HERO_Horizontal_3_69510693-5265-4d5e-95ae-4706d0cb7fdd.webp?width=600',
         body='''
<h2>Vì sao lốp tubeless chạy được áp suất thấp hơn?</h2>
<p>Lốp có săm khi bơm non dễ bị “kẹp săm” (pinch flat): săm bị ép giữa vành và chướng ngại vật rồi thủng. Lốp tubeless không có săm nên không gặp lỗi này; keo tự vá bên trong còn bịt kín các lỗ thủng nhỏ ngay khi đang chạy. Nhờ vậy bạn có thể giảm áp suất để lốp ôm mặt đường tốt hơn, lăn êm hơn trên đường xấu và bám hơn khi vào cua.</p>
<h2>Những yếu tố quyết định áp suất</h2>
<ul>
<li><strong>Tổng cân nặng</strong> người và xe: càng nặng càng cần áp suất cao hơn.</li>
<li><strong>Bản lốp</strong>: lốp càng to, áp suất cần càng thấp.</li>
<li><strong>Bề rộng trong của vành</strong>: vành rộng làm lốp “nở” hơn, thường cho phép giảm thêm một chút.</li>
<li><strong>Mặt đường và thời tiết</strong>: đường xấu, đường đất hoặc trời mưa nên giảm nhẹ để tăng độ bám.</li>
<li><strong>Bánh trước và bánh sau</strong>: bánh sau chịu nhiều tải hơn nên thường bơm cao hơn bánh trước một chút.</li>
</ul>
<h2>Bảng điểm khởi đầu tham khảo</h2>
<p>Áp dụng cho tổng cân nặng người và xe khoảng 75–85 kg. Nặng hơn khoảng 10 kg thì tăng 5–10%; nhẹ hơn thì giảm tương ứng.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Loại lốp</th><th scope="col">Bản lốp</th><th scope="col">Áp suất (bar)</th><th scope="col">Áp suất (psi)</th></tr></thead><tbody>
<tr><th scope="row">Road</th><td>28mm</td><td>4,5 – 5,5</td><td>65 – 80</td></tr>
<tr><th scope="row">Road / All-road</th><td>32mm</td><td>3,8 – 4,8</td><td>55 – 70</td></tr>
<tr><th scope="row">Gravel</th><td>38–40mm</td><td>2,2 – 3,0</td><td>32 – 44</td></tr>
<tr><th scope="row">Gravel</th><td>45mm trở lên</td><td>1,8 – 2,6</td><td>26 – 38</td></tr>
<tr><th scope="row">MTB Cross Country</th><td>2.2–2.4"</td><td>1,4 – 1,8</td><td>20 – 26</td></tr>
<tr><th scope="row">MTB Trail / Enduro</th><td>2.4–2.6"</td><td>1,3 – 1,7</td><td>19 – 25</td></tr>
</tbody></table></div>
<p>Đây chỉ là điểm bắt đầu. Hãy chạy thử, rồi điều chỉnh mỗi lần khoảng 0,1–0,2 bar cho đến khi thấy vừa ý.</p>
<h2>Giới hạn không được vượt qua</h2>
<ul>
<li>Luôn bơm trong khoảng áp suất tối thiểu – tối đa in trên thành lốp.</li>
<li>Với <strong>vành hookless</strong> (vành không móc), áp suất tối đa theo tiêu chuẩn là <strong>5 bar (72,5 psi)</strong>, kể cả khi lốp ghi cao hơn. Hãy kiểm tra cả giới hạn của nhà sản xuất vành.</li>
<li>Bơm quá non trên MTB/gravel dễ làm lốp “ăn” vào vành khi đi đá, có thể méo vành. Ruột lót chống thủng như Vittoria Air-Liner giúp bảo vệ vành và cho phép chạy áp suất thấp an toàn hơn.</li>
</ul>
<h2>Dấu hiệu bơm chưa đúng</h2>
<ul>
<li><strong>Quá căng:</strong> xe nảy, rung tay, mất bám khi vào cua hoặc trên đường xấu.</li>
<li><strong>Quá non:</strong> lốp lắc, “lả” khi vào cua, cảm giác ì và nặng, nghe tiếng vành chạm đá.</li>
</ul>
<h2>Chăm sóc lốp tubeless</h2>
<ul>
<li>Kiểm tra áp suất trước mỗi chuyến đi bằng đồng hồ chính xác — lốp tubeless mất hơi chậm theo thời gian.</li>
<li>Bổ sung hoặc thay keo tự vá khoảng 3–6 tháng một lần, sớm hơn nếu trời nóng hoặc đạp nhiều.</li>
<li>Dùng băng keo vành và chân van tubeless đúng chuẩn để tránh xì hơi.</li>
</ul>
<p>Cần tư vấn chọn lốp, keo hay chuyển đổi xe sang tubeless? Đội ngũ kỹ thuật Spinlab luôn sẵn sàng hỗ trợ.</p>
''', products=[('vittoria-universal-sealant.html', ''), ('vittoria-air-liner-light-gravel.html', ''), ('vittoria-tubeless-rim-tape.html', ''), ('vittoria-corsa-next.html', '')]),

    dict(slug='huong-dan-chon-size-xe-dap', cat='huong-dan', tag='Hướng dẫn', date='2026-10-21',
         title='Chọn size xe đạp theo chiều cao',
         lead='Chọn đúng size khung là bước quan trọng nhất khi mua xe: xe vừa người giúp đạp thoải mái, kiểm soát tốt và tránh đau mỏi. Bảng dưới đây tổng hợp khuyến nghị của Polygon cho các mẫu xe Spinlab đang phân phối.',
         image='https://media.polygonbikes.com/wp-content/uploads/2026/04/23161748/Heist-Feature-1.jpg', thumb='https://media.polygonbikes.com/wp-content/uploads/2026/04/23161748/Heist-Feature-1.jpg',
         body=f'''
<h2 id="chon-size">Bảng size theo chiều cao</h2>
<p>Số liệu tham khảo theo bảng kích thước khung của Polygon. Mỗi trang sản phẩm có bảng chi tiết của riêng mẫu xe đó.</p>
<div class="size-grid">{"".join(tables)}</div>
<h2>Khi chiều cao nằm giữa hai size</h2>
<ul>
<li>Chọn size nhỏ hơn nếu bạn thích xe linh hoạt, dễ xoay trở; chọn size lớn hơn nếu bạn ưu tiên sự ổn định khi đi đường dài.</li>
<li>Người có chân dài hơn so với thân thường hợp size lớn hơn; thân dài, chân ngắn thường hợp size nhỏ hơn.</li>
<li>Chiều cao yên, độ dài pô tăng và vị trí ghi đông có thể tinh chỉnh thêm sau khi chọn đúng size khung.</li>
</ul>
<h2>Cách đo chiều cao cho chính xác</h2>
<ul>
<li>Đứng thẳng, không mang giày, lưng và gót chân sát tường; đặt một vật phẳng lên đầu và đánh dấu.</li>
<li>Đo thêm chiều dài chân trong (từ sàn đến đáy chậu) để nhân viên tư vấn chọn size và chiều cao yên chuẩn hơn.</li>
</ul>
<h2>Thử xe trước khi mua</h2>
<p>Bảng size là điểm khởi đầu; cảm giác thực tế trên xe mới là quan trọng nhất. Hãy ghé đại lý Spinlab gần nhất để ngồi thử và điều chỉnh xe cho vừa người.</p>
''', products=[]),
]

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
.size-grid{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.size-grid caption small{display:block;font-weight:400;color:var(--muted);font-size:13px}
.art-products{margin:40px 0 0}
.art-products h2{font-size:22px;margin:0 0 16px}
.art-more{border-top:1px solid var(--line);padding-top:32px;margin-top:8px}
.art-more h2{font-size:22px;margin:0 0 4px}
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
FOLLOW = ('<section class="art-more"><h2>Sự kiện &amp; cộng đồng</h2><p>Lịch chạy thử xe, giải đua và các buổi gặp gỡ cộng đồng của Spinlab được thông báo trên mạng xã hội.</p>'
          '<div class="article"><div class="cta" style="margin-top:12px"><a class="btn btn-primary" href="https://www.facebook.com/profile.php?id=61573821032401" target="_blank" rel="noopener">Facebook Spinlab</a>'
          '<a class="btn btn-outline" href="https://www.instagram.com/spinlabvn/" target="_blank" rel="noopener">Instagram</a>'
          '<a class="btn btn-outline" href="https://www.youtube.com/@Spinlabvn" target="_blank" rel="noopener">YouTube</a></div></div></section>')
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
