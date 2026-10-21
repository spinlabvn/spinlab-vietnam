"""Product cards show the product's next photo on hover (like vittoria.com).

For every product card on every page, the second image is the first photo in that product page's gallery
(ul.g-thumbs) that differs from the card's own image. It is added as <img class="alt"> inside .p-img and
cross-fades in on hover (pointer devices only). Cards whose page has no gallery are left unchanged.
Run after build_compare.py, before clean_urls.py:
    python3 tools/card_hover.py
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from clean_urls import norm  # noqa: E402

CSS = '''/* Card hover image */
.p-img>img{transition:opacity .3s}
.p-img>img.alt{position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;padding:12px;box-sizing:border-box;opacity:0;pointer-events:none}
.p-img.tire>img.alt{padding:12px 14%}
.p-img.part>img.alt{padding:12px 8%}
@media (hover:hover){.p-card:hover .p-img>img.alt{opacity:1}.p-card:hover .p-img:has(>img.alt)>img:not(.alt){opacity:0}}
'''
base = lambda u: u.split('?')[0]


def card_size(u):
    """Gallery images are 1000px wide on Vittoria's CDN; cards use 600px."""
    return re.sub(r'([?&]width=)\d+', r'\g<1>600', u) if 'cdn.shopify.com' in u else u


pages = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html')) if not f.endswith('v1-premium.html'))
gallery = {}
for f in pages:
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    m = re.search(r'<ul class="g-thumbs"[^>]*>(.*?)</ul>', s, re.S)
    if m:
        gallery[f] = re.findall(r'data-src="([^"]+)"', m.group(1))

CARD = re.compile(r'<article class="p-card"[^>]*>.*?</article>', re.S)


def add_alt(m):
    c = m.group(0)
    c = re.sub(r'<img class="alt"[^>]*>', '', c)
    h = re.search(r'class="stretch" href="([^"#]+)', c)
    first = re.search(r'(<div class="p-img[^"]*">(?:(?!</div>).)*?<img [^>]*src="([^"]+)"[^>]*>)', c, re.S)
    if not h or not first:
        return c
    alt = next((u for u in gallery.get(norm(h.group(1)), []) if base(u) != base(first.group(2))), None)
    if not alt:
        return c
    return c.replace(first.group(1), first.group(1) + f'<img class="alt" src="{card_size(alt)}" alt="" loading="lazy" aria-hidden="true">', 1)


n = cards = 0
for f in pages:
    p = os.path.join(ROOT, f)
    s = open(p, encoding='utf-8').read()
    t = CARD.sub(add_alt, s)
    t = re.sub(r'/\* Card hover image \*/\n(?:[.@][^\n]*\n)+', '', t)
    if '<img class="alt"' in t:
        t = t.replace('</style>', CSS + '</style>', 1)
    cards += t.count('<img class="alt"')
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)
        n += 1
print(f'ảnh thứ hai khi trỏ chuột: {cards} thẻ sản phẩm trên {n} trang')
