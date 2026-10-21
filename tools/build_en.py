"""English version of the site: en/<page>.html, served as /en/<page> (and /en/trangchu for the homepage).

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
PAGES = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html')) if not f.endswith('v1-premium.html'))
NAMES = {p[:-5] for p in PAGES} | {'trangchu'}
url = lambda page, en: ('/en' if en else '') + ('/trangchu' if page == 'index.html' else '/' + page[:-5])

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
    s = re.sub(r'(href=\\?")/([a-z0-9-]+)(?=[#?"\\])', lambda m: m.group(1) + ('/en/' if m.group(2) in NAMES else '/') + m.group(2), s)
    # relative assets -> absolute (pages now live one folder down)
    s = re.sub(r'((?:src|href|data-src)=\\?")(img/)', r'\1/\2', s)
    s = re.sub(r'url\((["\']?)img/', r'url(\1/img/', s)
    # scripts that build URLs / read product ids from links
    s = s.replace(".replace(/^\\//,'')", ".replace(/^\\/(?:en\\/)?/,'')")
    s = s.replace("'/so-sanh", "'/en/so-sanh").replace("'/trangchu'", "'/en/trangchu'").replace("'/'+id", "'/en/'+id")
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
    open(os.path.join(ROOT, 'en', page), 'w', encoding='utf-8').write(en)
# English pages whose Vietnamese page no longer exists
for f in glob.glob(os.path.join(ROOT, 'en', '*.html')):
    if os.path.basename(f) not in PAGES:
        os.remove(f)
with open(os.path.join(ROOT, 'tools', 'en-missing.txt'), 'w', encoding='utf-8') as fh:
    for k, page in missing.items():
        fh.write(f'{page}\t{k}\n')
print(f'{len(PAGES)} trang tiếng Anh trong en/; {len(missing)} câu chưa có bản dịch (tools/en-missing.txt)')
