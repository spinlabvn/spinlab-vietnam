"""Product cards show only the brand above the product name ("Polygon", not "Polygon · Collosus N"):
the series / category after the brand mostly repeats the product name. Product detail pages keep their full line.
Idempotent; run after card_hover.py and before build_en.py:
    python3 tools/card_brand.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD = re.compile(r'<article class="p-card"[^>]*>.*?</article>', re.S)
BRAND = re.compile(r'(<span class="p-brand">)([^<·]*?)\s*·[^<]*(</span>)')

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f, encoding='utf-8').read()
    t = CARD.sub(lambda m: BRAND.sub(r'\1\2\3', m.group(0)), s)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        n += 1
print(f'thẻ sản phẩm chỉ ghi tên hãng: cập nhật {n} trang')
