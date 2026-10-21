"""City - Hybrid listing page (xe-city.html), built on the xe-gravel.html shell.
Groups and order below; a bike is listed only while it is in vi.VI and bikes.json.
    python3 city_listing.py ../.. bikes.json
Then run the usual post-processing (brands.py, build_new_products, apply_prices, build_compare, brand_logos, build_hubs, clean_urls).
"""
import html, json, os, re, sys

from vi import VI

D, DATA = sys.argv[1], sys.argv[2]
E = lambda s: html.escape(s, quote=True)
B = {b['slug']: b for b in json.load(open(DATA, encoding='utf-8'))}

GROUPS = [
    ('Heist', 'Hybrid · Khung nhôm ALX · Phuộc nhún trước', 'Hybrid đời 2027 cho cả đường phố lẫn đường đất — truyền động 1x, phanh đĩa dầu, lốp 700x45c.',
     [('heist-7', 'Shimano Deore 1x12 · Phuộc hơi'), ('heist-5', 'Shimano CUES 1x · Khoá nhún'), ('heist-2', 'Shimano Altus 1x8')]),
    ('Path', 'City · Khung nhôm ALX · Phuộc cứng', 'Xe đi phố ghi đông phẳng: nhanh như xe road, ngồi thẳng dễ quan sát, có sẵn lỗ bắt baga và chắn bùn.',
     [('path-4', 'Shimano Tiagra 1x10 · Phuộc carbon'), ('path-3', 'Shimano CUES 1x9 · Phanh đĩa dầu'), ('path-2', 'Shimano Altus 1x8')]),
]


def card(slug, desc):
    b, v = B[slug], VI[slug]
    img = b['colors'][0]['images'][0] if b['colors'] and b['colors'][0]['images'] else ''
    return (f'<article class="p-card"><div class="p-img"><img src="{E(img)}" alt="Polygon {E(b["name"])}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">Polygon · {E(v["series"])}</span><h3 class="p-name"><a class="stretch" href="{v["file"]}.html">{E(b["name"])}</a></h3>'
            f'<p class="p-desc">{E(desc)}</p><span class="p-price">1.980.000₫</span></div></article>')


sections = []
for name, sub, desc, items in GROUPS:
    cards = ''.join(card(s, d) for s, d in items if s in VI and s in B)
    if cards:
        sections.append(f'<section class="road-group"><div class="rg-head"><div><h2>{E(name)}</h2><p class="rg-sub">{E(sub)}</p></div>'
                        f'<p class="rg-desc">{E(desc)}</p></div><div class="grid">{cards}</div></section>')

main = f'''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li><a href="xe-dap.html">Xe đạp</a></li><li aria-current="page">City - Hybrid</li></ol></nav></div>
  <section class="list-hero">
    <img src="https://media.polygonbikes.com/wp-content/uploads/2026/04/23161748/Heist-Feature-1.jpg" alt="Xe đạp Polygon Heist trên đường phố">
    <div class="container"><div class="lh-copy"><span class="kicker">Polygon City - Hybrid</span><h1>City - Hybrid</h1><p>Heist và Path — xe đi phố, đi làm và dạo chơi cuối tuần chính hãng Polygon, phân phối bởi Spinlab.</p></div></div>
  </section>
  <div class="container">{"".join(sections)}</div>
</main>'''

p = open(os.path.join(D, 'xe-gravel.html'), encoding='utf-8').read()
p = re.sub(r'<title>.*?</title>', '<title>Xe đạp City - Hybrid Polygon — Spinlab</title>', p, 1, flags=re.S)
p = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Xe đạp City - Hybrid Polygon chính hãng tại Spinlab: Heist 2, 5, 7 và Path 2, 3, 4.">', p, 1)
p = re.sub(r'<main id="main".*?</main>', lambda m: main, p, 1, flags=re.S)
p = re.sub(r'\s*<meta name="product-id"[^>]*>', '', p)
open(os.path.join(D, 'xe-city.html'), 'w', encoding='utf-8').write(p)
print('xe-city.html', sum(s.count('<article') for s in sections), 'xe')
