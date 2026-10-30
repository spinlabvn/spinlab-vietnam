"""English version of the site: en/<english-slug>.html, served as /en/<english-slug> (homepage: /en/home).
Pages with Vietnamese slugs get English ones (EN_SLUG); product pages keep their slug.

Every Vietnamese page is translated with data/en.json (see tools/i18n.py), internal links are moved under /en/,
asset paths are made absolute, and both language versions get a VI / EN switch plus hreflang links.
Run LAST, after clean_urls.py:
    python3 tools/build_en.py
Strings missing from data/en.json stay in Vietnamese and are listed in tools/en-missing.txt — add them to the
dictionary and run again.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import i18n  # noqa: E402

D = json.load(open(os.path.join(ROOT, 'data', 'en.json'), encoding='utf-8'))


def extra_pairs():
    """English text typed in the admin page: articles (data/articles.json) and product texts (data/overrides.json)."""
    out = {}
    cut = lambda t: t[:150].rsplit(' ', 1)[0] + '…'
    dv = lambda d: '/'.join(reversed(d.split('-')))
    try:
        arts = json.load(open(os.path.join(ROOT, 'data', 'articles.json'), encoding='utf-8'))['articles']
    except FileNotFoundError:
        arts = []
    for a in arts:
        en = a.get('en') or {}
        for k in ('title', 'lead', 'tag'):
            if en.get(k):
                out[i18n.norm(a[k])] = en[k]
        if en.get('title'):
            out[i18n.norm(a['title'] + ' — Spinlab')] = en['title'] + ' — Spinlab'
        if en.get('lead'):
            out[i18n.norm(cut(a['lead']))] = cut(en['lead'])
            out[i18n.norm(a['lead'][:155])] = en['lead'][:155]
        if en.get('tag'):
            out[i18n.norm(f"{a['tag']} · {dv(a['date'])}")] = f"{en['tag']} · {dv(a['date'])}"
        if en.get('body'):
            out.update(i18n.pairs(a['body'], en['body']))
    try:
        ov = json.load(open(os.path.join(ROOT, 'data', 'overrides.json'), encoding='utf-8'))['pages']
    except FileNotFoundError:
        ov = {}
    for o in ov.values():
        en = o.get('en') or {}
        for k in ('tagline', 'heading'):
            if o.get(k) and en.get(k):
                out[i18n.norm(o[k])] = en[k]
        for v, e in zip(o.get('intro') or [], en.get('intro') or []):
            out[i18n.norm(v)] = e
        for (vt, vx), (et, ex) in zip(o.get('features') or [], en.get('features') or []):
            out[i18n.norm(vt)] = et
            out[i18n.norm(vx)] = ex
    return {k: v for k, v in out.items() if k and v}


D = {**D, **extra_pairs()}
PAGES = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html')) if not f.endswith('v1-premium.html'))
NAMES = {p[:-5] for p in PAGES} | {'trangchu'}
EN_SLUG = {
    'index': 'home', 'trangchu': 'home', 'xe-dap': 'bikes', 'xe-road': 'road-bikes', 'xe-mtb': 'mountain-bikes', 'xe-gravel': 'gravel-bikes',
    'xe-city': 'city-hybrid-bikes', 'xe-trial': 'trial-bikes', 'phu-tung': 'parts', 'lop-xe': 'tyres', 'day-cuon-tay-lai': 'handlebar-tape',
    'thuong-hieu': 'brands', 'thuong-hieu-polygon': 'brand-polygon', 'thuong-hieu-vittoria': 'brand-vittoria', 'thuong-hieu-emume': 'brand-emume',
    'thuong-hieu-story-bike': 'brand-story-bike', 'dai-ly': 'dealers', 'so-sanh': 'compare', 'san-pham-moi': 'new-products', 'tin-tuc': 'news',
    'huong-dan': 'guides', 'tin-tuc-polygon-strattos-c': 'news-polygon-strattos-c',
    'huong-dan-ap-suat-lop-tubeless': 'guide-tubeless-tyre-pressure', 'huong-dan-chon-size-xe-dap': 'guide-bike-size-by-height',
}
def en_slug(name):
    """English slug: fixed table first, then new articles (tin-tuc-x -> news-x, huong-dan-x -> guide-x)."""
    if name in EN_SLUG:
        return EN_SLUG[name]
    for vi, en in (('tin-tuc-', 'news-'), ('huong-dan-', 'guide-')):
        if name.startswith(vi):
            return en + name[len(vi):]
    return name


def url(page, en):
    name = page[:-5]
    if en:
        return '/en/' + en_slug(name)
    return '/trangchu' if name == 'index' else '/' + name

SWITCH_RE = re.compile(r'<button class="lang"[^>]*>.*?</button>|<span class="lang"[^>]*>.*?>EN</a></span>(?:<a href="[^"]*" lang="en" hreflang="en"[^>]*>EN</a></span>)*', re.S)
ALT_RE = re.compile(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">')
CSS = '''/* Language switch */
.lang a{padding:4px 2px;color:var(--muted)}
.lang a[aria-current]{color:var(--text);font-weight:800}
.lang a:hover{color:var(--brand-red)}
'''


def switch(page, en):
    cur = ' aria-current="true"'
    vi_a = f'<a href="{url(page, False)}" lang="vi" hreflang="vi"{"" if en else cur}>VI</a>'
    en_a = f'<a href="{url(page, True)}" lang="en" hreflang="en"{cur if en else ""}>EN</a>'
    label = 'Language' if en else 'Ngôn ngữ'
    return f'<span class="lang" role="group" aria-label="{label}">{vi_a}<span aria-hidden="true">&nbsp;/&nbsp;</span>{en_a}</span>'


def common(s, page, en):
    s = SWITCH_RE.sub(lambda m: switch(page, en), s, 1)
    s = ALT_RE.sub('', s)
    alt = (f'\n<link rel="alternate" hreflang="vi" href="{url(page, False)}">'
           f'\n<link rel="alternate" hreflang="en" href="{url(page, True)}">')
    s = s.replace('</title>', '</title>' + alt, 1)
    s = re.sub(r'/\* Language switch \*/\n(?:\.lang[^\n]*\n)+', '', s)
    return s.replace('</style>', CSS + '</style>', 1)


def to_en(s):
    s = re.sub(r'<html lang="vi"', '<html lang="en"', s, 1)
    # internal links -> /en/...
    s = re.sub(r'(href=\\?")/([a-z0-9-]+)(?=[#?"\\])', lambda m: m.group(1) + ('/en/' + en_slug(m.group(2)) if m.group(2) in NAMES else '/' + m.group(2)), s)
    # relative assets -> absolute (pages now live one folder down)
    s = re.sub(r'((?:src|href|data-src)=\\?")(img/)', r'\1/\2', s)
    s = re.sub(r'url\((["\']?)img/', r'url(\1/img/', s)
    # scripts that build URLs / read product ids from links
    s = s.replace(".replace(/^\\//,'')", ".replace(/^\\/(?:en\\/)?/,'')")
    s = s.replace('&hl=vi&z=16&output=embed', '&hl=en&z=16&output=embed')   # footer map labels in English
    s = s.replace("'/so-sanh", "'/en/compare").replace("'/trangchu'", "'/en/home'").replace("'/'+id", "'/en/'+id")
    return s


missing = {}
os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
for page in PAGES:
    p = os.path.join(ROOT, page)
    vi = open(p, encoding='utf-8').read()
    vi2 = common(vi, page, False)
    if vi2 != vi:
        open(p, 'w', encoding='utf-8').write(vi2)
    en, miss = i18n.translate(vi2, D)
    for k in miss:
        missing.setdefault(k, page)
    en = common(to_en(en), page, True)
    open(os.path.join(ROOT, 'en', en_slug(page[:-5]) + '.html'), 'w', encoding='utf-8').write(en)
# English pages whose Vietnamese page no longer exists (or that were renamed)
keep = {en_slug(p[:-5]) + '.html' for p in PAGES}
for f in glob.glob(os.path.join(ROOT, 'en', '*.html')):
    if os.path.basename(f) not in keep:
        os.remove(f)
with open(os.path.join(ROOT, 'tools', 'en-missing.txt'), 'w', encoding='utf-8') as fh:
    for k, page in missing.items():
        fh.write(f'{page}\t{k}\n')
print(f'{len(PAGES)} trang tiếng Anh trong en/; {len(missing)} câu chưa có bản dịch (tools/en-missing.txt)')
