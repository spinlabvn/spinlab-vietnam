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
for f in pages:
    s = R(f)
    if '<span class="p-price big">' not in s:
        continue
    main = re.search(r'<main id="main".*?</main>', s, re.S)
    skus = set(re.findall(r'data-sku="([^"]+)"', main.group(0) if main else '')) | set(re.findall(r'"sku": "([^"]+)"', s))
    skus = sorted(x for x in skus if stock.ok(x))
    if not skus:
        continue
    lab = stock.label(skus)
    labels[f] = lab
    s = re.sub(r'(<span class="p-price big">)[^<]*(</span>)', lambda m: m.group(1) + lab + m.group(2), s, 1)
    s = re.sub(r'// Vittoria retail price: follows the selected SKU\n.*?\}\)\(\);\n', '', s, flags=re.S)
    i = s.rindex('</script>\n</body>')
    s = s[:i] + JS % json.dumps({x: stock.fmt(stock.price(x)) if stock.price(x) else 'Liên hệ' for x in skus}, ensure_ascii=False) + s[i:]
    W(f, s)

# Page prices (bikes, Emume): one retail price per product page
PP = json.load(open(os.path.join(ROOT, 'data', 'page-prices.json'), encoding='utf-8'))['prices']
for f in pages:
    if not (f in PP or f.startswith(('polygon-', 'story-'))):
        continue
    s = R(f)
    if '<span class="p-price big">' not in s:
        continue
    lab = stock.fmt(PP[f]) if f in PP else 'Liên hệ'
    labels[f] = lab
    W(f, re.sub(r'(<span class="p-price big">)[^<]*(</span>)', lambda m: m.group(1) + lab + m.group(2), s, 1))

n = 0
card = re.compile(r'(<article class="p-card"[^>]*>(?:(?!</article>).)*?class="stretch" href="([^"#]+)"(?:(?!</article>).)*?<span class="p-price">)([^<]*)(</span>)', re.S)
for f in pages:
    s = R(f)
    t = card.sub(lambda m: m.group(1) + labels.get(norm(m.group(2)), m.group(3)) + m.group(4), s)
    if t != s:
        W(f, t)
        n += 1
print(f'{len(labels)} trang sản phẩm có giá (Vittoria theo mã, Polygon theo mẫu); cập nhật thẻ giá trên {n} trang')
