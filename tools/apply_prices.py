"""Retail prices.
Page prices: data/page-prices.json (page -> VND) for Polygon/Story bikes and Emume products; a bike page not in that file shows "Liên hệ".
Vittoria: Spinlab's price list (data/vittoria-stock.json, via tools/generators/stock.py).

- Product pages: the price follows the selected size/colour (the page shows the SKU in #sz-sku; a small script
  maps it to that SKU's price). Without JavaScript the page shows the lowest price ("Từ …" when sizes differ).
- Product cards on every page (listings, brand pages, homepage, related products): lowest price, "Từ …" if it varies.

Run after the generators, brands.py and build_new_products.py, and before build_compare.py:
    python3 tools/apply_prices.py
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'generators'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import stock  # noqa: E402
from clean_urls import norm  # noqa: E402

R = lambda f: open(os.path.join(ROOT, f), encoding='utf-8').read()
W = lambda f, s: open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)

JS = '''// Vittoria retail price: follows the selected SKU
(() => {
  const P = %s, el = document.querySelector('.p-price.big'), code = document.getElementById('sz-sku');
  if (!el || !code) return;
  const upd = () => { const p = P[(code.textContent || '').trim()]; if (p) el.textContent = p; };
  new MutationObserver(upd).observe(code, {childList: true, characterData: true, subtree: true});
  upd();
})();
'''

pages = [os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html')) if not f.endswith('v1-premium.html')]
labels = {}
PP = json.load(open(os.path.join(ROOT, 'data', 'page-prices.json'), encoding='utf-8'))['prices']
LINE = json.load(open(os.path.join(ROOT, 'data', 'vittoria-stock.json'), encoding='utf-8')).get('line_prices', {})
# data/settings.json: show_prices false = every price shows "Liên hệ" (temporary, switched in the admin page)
_set = os.path.join(ROOT, 'data', 'settings.json')
SHOW = json.load(open(_set, encoding='utf-8')).get('show_prices', True) if os.path.exists(_set) else True
HIDDEN_LABEL = 'Liên hệ'
# the per-SKU price script is (re)added below only where it belongs; drop copies inherited from page shells
_JSRX = re.compile(r'// Vittoria retail price: follows the selected SKU\n.*?\}\)\(\);\n', re.S)
for _f in pages:
    _s = R(_f)
    if _JSRX.search(_s):
        W(_f, _JSRX.sub('', _s))
for f in pages:
    s = R(f)
    if '<span class="p-price big">' not in s:
        continue
    main = re.search(r'<main id="main".*?</main>', s, re.S)
    skus = set(re.findall(r'data-sku="([^"]+)"', main.group(0) if main else '')) | set(re.findall(r'"sku": "([^"]+)"', s))
    if not skus or f in PP or f.startswith(('polygon-', 'story-')):   # bikes / Emume: page prices below
        continue
    skus = sorted(skus)
    # a line price (e.g. every Terreno PRO size) covers SKUs without their own price; otherwise "Liên hệ"
    base = next((v for k, v in LINE.items() if isinstance(v, int) and f.startswith(k)), None)
    price = {x: stock.price(x) or base for x in skus}
    priced = sorted({v for v in price.values() if v})
    lab = (('Từ ' if len(priced) > 1 else '') + stock.fmt(priced[0]) if priced else 'Liên hệ') if SHOW else HIDDEN_LABEL
    labels[f] = lab
    s = re.sub(r'(<span class="p-price big">)[^<]*(</span>)', lambda m: m.group(1) + lab + m.group(2), s, 1)
    s = re.sub(r'// Vittoria retail price: follows the selected SKU\n.*?\}\)\(\);\n', '', s, flags=re.S)
    if SHOW:
        i = s.rindex('</script>\n</body>')
        s = s[:i] + JS % json.dumps({x: stock.fmt(price[x]) if price[x] else 'Liên hệ' for x in skus}, ensure_ascii=False) + s[i:]
    W(f, s)

# Page prices (bikes, Emume): one retail price per product page
for f in pages:
    if not (f in PP or f.startswith(('polygon-', 'story-'))):
        continue
    s = R(f)
    if '<span class="p-price big">' not in s:
        continue
    lab = (stock.fmt(PP[f]) if f in PP else 'Liên hệ') if SHOW else HIDDEN_LABEL
    labels[f] = lab
    W(f, re.sub(r'(<span class="p-price big">)[^<]*(</span>)', lambda m: m.group(1) + lab + m.group(2), s, 1))

n = 0
card = re.compile(r'(<article class="p-card"[^>]*>(?:(?!</article>).)*?class="stretch" href="([^"#]+)"(?:(?!</article>).)*?<span class="p-price">)([^<]*)(</span>)', re.S)
for f in pages:
    s = R(f)
    if not SHOW:   # also product pages whose price is not managed here
        s = re.sub(r'(<span class="p-price big">)[^<]*(</span>)', lambda m: m.group(1) + HIDDEN_LABEL + m.group(2), s, 1)
    t = card.sub(lambda m: m.group(1) + (labels.get(norm(m.group(2)), m.group(3)) if SHOW else HIDDEN_LABEL) + m.group(4), s)
    if t != s:
        W(f, t)
        n += 1
print(('' if SHOW else 'GIÁ ĐANG ẨN (Liên hệ) — ') + f'{len(labels)} trang sản phẩm có giá; cập nhật thẻ giá trên {n} trang')
