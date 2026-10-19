"""Tự động cập nhật mục "Sản phẩm mới" (trang chủ) và trang san-pham-moi.html.

Cách hoạt động
- Nguồn sản phẩm: mọi thẻ sản phẩm trên các trang thương hiệu (thuong-hieu-*.html).
- data/catalog.json lưu ngày đăng ("added") của từng sản phẩm, theo đường dẫn trang chi tiết.
- Sản phẩm chưa có trong catalog được coi là MỚI ĐĂNG: ghi ngày giờ hiện tại.
- Sản phẩm đã gỡ khỏi website sẽ tự bị loại khỏi catalog.
- Trang chủ hiện 8 sản phẩm đăng gần nhất; san-pham-moi.html hiện 24 sản phẩm gần nhất.

Chạy sau mỗi lần thêm / gỡ sản phẩm (sau khi các trang thương hiệu đã được tạo lại):
    python3 tools/build_new_products.py
Tuỳ chọn: --home N (số sản phẩm trên trang chủ, mặc định 8), --page N (mặc định 24).
"""
import argparse, glob, html, json, os, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, 'data', 'catalog.json')
E = html.escape


def read(f):
    return open(os.path.join(ROOT, f), encoding='utf-8').read()


def write(f, s):
    open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)


def scan():
    """Every product card currently on the site, in brand-page order: {href: card_html}."""
    cards = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'thuong-hieu-*.html'))):
        for a in re.findall(r'<article class="p-card"[^>]*>.*?</article>', open(f, encoding='utf-8').read(), re.S):
            m = re.search(r'class="stretch" href="([^"]+)"', a)
            if m and m.group(1) not in cards:
                cards[m.group(1)] = a
    return cards


def clean(card):
    """Normalise a card for the 'new' grids: one 'Mới' tag, no listing-only attributes."""
    c = re.sub(r'\s*\n\s*', '', card)
    c = re.sub(r'<article class="p-card"[^>]*>', '<article class="p-card">', c, 1)
    c = re.sub(r'<span class=("tag[^"]*"|tag)>[^<]*</span>', '', c)
    return re.sub(r'(<div class="p-img[^"]*">)', r'\1<span class="tag">Mới</span>', c, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--home', type=int, default=8)
    ap.add_argument('--page', type=int, default=24)
    args = ap.parse_args()

    cards = scan()
    cat = json.load(open(CATALOG, encoding='utf-8')) if os.path.exists(CATALOG) else {'products': []}
    known = {p['href']: p for p in cat['products']}
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    seq = max([p.get('seq', 0) for p in known.values()] + [0])
    products, added = [], []
    fresh = [h for h in cards if h not in known]
    for href in cards:
        if href in known:
            products.append(known[href])
        else:
            # new items in one run: the first card on the brand pages gets the highest seq, so it is shown first
            p = {'href': href, 'added': now, 'seq': seq + len(fresh) - fresh.index(href)}
            products.append(p); added.append(href)
    removed = [h for h in known if h not in cards]
    products.sort(key=lambda p: (p['added'], p['seq']), reverse=True)
    for p in products:
        nm = re.search(r'class="stretch" href="[^"]+">([^<]+)</a>', cards[p['href']])
        p['name'] = html.unescape(nm.group(1)) if nm else p['href']
    json.dump({'note': 'Ngày đăng sản phẩm — do tools/build_new_products.py quản lý', 'products': products},
              open(CATALOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    newest = products[:max(args.home, args.page)]
    # homepage grid
    idx = read('index.html')
    a = idx.index('<div class="grid">', idx.index('id="new"')) + len('<div class="grid">')
    z = idx.index('\n      </div>', a)
    grid = ''.join('\n        ' + clean(cards[p['href']]) for p in newest[:args.home])
    idx = idx[:a] + grid + idx[z:]
    idx = re.sub(r'(<section class="section" id="new"[^>]*>\s*<div class="container">\s*)<div class="sec-head"><h2>Sản phẩm mới</h2>(?:<a[^>]*>[^<]*</a>)?</div>',
                 r'\1<div class="sec-head"><h2>Sản phẩm mới</h2><a class="see-all" href="san-pham-moi.html">Xem tất cả</a></div>', idx, 1)
    write('index.html', idx)

    # full "new products" page, built on the brand-page shell
    shell = read('thuong-hieu-vittoria.html')
    items = ''
    for p in newest[:args.page]:
        d = datetime.strptime(p['added'], '%Y-%m-%d %H:%M').strftime('%d/%m/%Y')
        c = clean(cards[p['href']]).replace('<span class="p-price">', f'<span class="p-date">Đăng ngày {d}</span><span class="p-price">', 1)
        items += c
    main_html = f'''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li aria-current="page">Sản phẩm mới</li></ol></nav></div>
  <section class="list-hero plain">
    <div class="container"><div class="lh-copy"><span class="kicker">Spinlab</span><h1>Sản phẩm mới</h1><p>{len(newest[:args.page])} sản phẩm đăng gần đây nhất — xe đạp Polygon, lốp và phụ kiện Vittoria chính hãng.</p></div></div>
  </section>
  <section class="brand-cat"><div class="container"><div class="grid">{items}</div></div></section>
</main>'''
    s = re.sub(r'<title>.*?</title>', '<title>Sản phẩm mới — Spinlab</title>', shell, 1, flags=re.S)
    s = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Sản phẩm mới đăng tại Spinlab: xe đạp Polygon, lốp và phụ kiện Vittoria chính hãng.">', s, 1)
    s = re.sub(r'<main id="main".*?</main>', lambda m: main_html, s, 1, flags=re.S)
    if '.p-date{' not in s:
        s = s.replace('</style>', '.p-date{display:block;margin:6px 0 2px;font-size:12px;color:var(--muted)}\n</style>', 1)
    write('san-pham-moi.html', s)

    print(f'{len(products)} sản phẩm | mới thêm: {len(added)} | đã gỡ: {len(removed)}')
    for h in added: print('  + ', h)
    for h in removed: print('  - ', h)
    print('Trang chủ:', ', '.join(p['name'] for p in newest[:args.home]))


if __name__ == '__main__':
    main()
