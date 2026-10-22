"""Hide / show products (data/hidden.json, edited from the admin page) — fully reversible.

For a hidden product page:
  - the page file moves to tools/hidden-pages/ (the URL stops working; tools/ is not public),
  - every product card linking to it is replaced by an HTML comment holding the card (<!--hidden-card:...-->),
  - other links to it become <span data-hidden-href="..."> (e.g. "Các phiên bản trong dòng ...").
Showing it again moves the page back and restores the cards and links. Run after build_articles.py /
apply_overrides.py and before build_new_products.py:
    python3 tools/apply_hidden.py
"""
import base64, glob, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from clean_urls import norm  # noqa: E402

STORE = os.path.join(ROOT, 'tools', 'hidden-pages')
CARD = re.compile(r'<article class="p-card"[^>]*>.*?</article>', re.S)
HID_CARD = re.compile(r'<!--hidden-card:([A-Za-z0-9+/=]+)-->')
LINK = re.compile(r'<a ([^>]*?)href="(/?[a-z0-9-]+(?:\.html)?)"([^>]*)>(.*?)</a>', re.S)
HID_LINK = re.compile(r'<span data-hidden-href="([^"]+)"( data-a="[^"]*")?>(.*?)</span><!--/h-->', re.S)


def load():
    p = os.path.join(ROOT, 'data', 'hidden.json')
    return set(json.load(open(p, encoding='utf-8'))['pages']) if os.path.exists(p) else set()


def card_target(c):
    m = re.search(r'class="stretch" href="([^"#?]+)', c)
    return norm(m.group(1)) if m else None


def run():
    hidden = load()
    os.makedirs(STORE, exist_ok=True)
    moved = []
    # pages: hide -> move to store, show -> move back
    for page in hidden:
        src = os.path.join(ROOT, page)
        if os.path.exists(src):
            shutil.move(src, os.path.join(STORE, page))
            moved.append('- ' + page)
    for f in glob.glob(os.path.join(STORE, '*.html')):
        page = os.path.basename(f)
        if page not in hidden and not os.path.exists(os.path.join(ROOT, page)):
            shutil.move(f, os.path.join(ROOT, page))
            moved.append('+ ' + page)
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        s = open(f, encoding='utf-8').read()
        t = HID_CARD.sub(lambda m: base64.b64decode(m.group(1)).decode('utf-8'), s)
        t = HID_LINK.sub(lambda m: f'<a {base64.b64decode(m.group(2)[9:-1]).decode() if m.group(2) else ""}href="{m.group(1)}">{m.group(3)}</a>', t)
        t = CARD.sub(lambda m: f'<!--hidden-card:{base64.b64encode(m.group(0).encode()).decode()}-->'
                     if card_target(m.group(0)) in hidden else m.group(0), t)

        def link(m):
            if norm(m.group(2)) not in hidden:
                return m.group(0)
            attrs = (m.group(1) + m.group(3)).strip()
            extra = f' data-a="{base64.b64encode((attrs + " ").encode()).decode()}"' if attrs else ''
            return f'<span data-hidden-href="{m.group(2)}"{extra}>{m.group(4)}</span><!--/h-->'
        t = LINK.sub(link, t)
        if t != s:
            open(f, 'w', encoding='utf-8').write(t)
            n += 1
    print(f'sản phẩm ẩn: {len(hidden)}; chuyển trang: {", ".join(moved) or "không"}; cập nhật {n} trang')


if __name__ == '__main__':
    run()
