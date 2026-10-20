"""Clean URLs: every internal link drops '.html' and the homepage becomes /trangchu.
    index.html          -> /trangchu
    xe-road.html#road   -> /xe-road#road
Files on disk keep their .html names; the web server maps /xe-road to xe-road.html
(.htaccess on Hostinger, tools/serve.py locally). Run LAST, after every other build step:
    python3 tools/clean_urls.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html'))}


def url(page):
    """'index.html' -> '/trangchu', 'xe-road.html' -> '/xe-road'."""
    return '/trangchu' if page == 'index.html' else '/' + page[:-5]


def norm(href):
    """Inverse for tools: '/xe-road#x' or 'xe-road.html' -> 'xe-road.html'."""
    h = href.split('#')[0].split('?')[0].lstrip('/')
    if h in ('', 'trangchu'):
        return 'index.html'
    return h if h.endswith('.html') else h + '.html'


LINK = re.compile(r'href="([a-z0-9-]+\.html)((?:[#?][^"]*)?)"')


def clean(s):
    return LINK.sub(lambda m: f'href="{url(m.group(1))}{m.group(2)}"' if m.group(1) in PAGES else m.group(0), s)


if __name__ == '__main__':
    n = 0
    for f in sorted(PAGES):
        if f == 'v1-premium.html':
            continue
        p = os.path.join(ROOT, f)
        s = open(p, encoding='utf-8').read()
        t = clean(s)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
    print(f'đường dẫn gọn trên {n} trang')
