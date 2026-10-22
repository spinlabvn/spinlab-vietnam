"""Product texts edited in the admin page (data/overrides.json), applied on top of the generated product pages.

Editable on every product page (same markup for bikes, tyres, accessories and Emume):
  tagline   <p class="tagline"> under the product name
  heading   the <h2> of the "Giới thiệu" section (#gioi-thieu)
  intro     the plain paragraphs of that section
  features  the feature list (#tinh-nang / #cong-nghe), only when the page has a single list
Run after the generators and build_articles.py, before build_compare.py:
    python3 tools/apply_overrides.py
"""
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda s: html.escape(s, quote=False)
text = lambda s: ' '.join(html.unescape(re.sub(r'<[^>]+>', '', s)).split())

TAGLINE = re.compile(r'(<p class="tagline">)(.*?)(</p>)', re.S)
INTRO = re.compile(r'(<section class="pdp-sec intro" id="gioi-thieu">\s*<div>\s*<h2>)(.*?)(</h2>)((?:\s*<p>.*?</p>)*)', re.S)
FEAT_SEC = re.compile(r'<section class="pdp-sec" id="(?:tinh-nang|cong-nghe)">.*?</section>', re.S)
TECH = re.compile(r'(<div class="tech">)(.*?)(</div>)', re.S)
ART = re.compile(r'<article><span class="num">\d+</span><h3>(.*?)</h3><p>(.*?)</p></article>', re.S)


def product_pages():
    return sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html'))
                  if '<span class="p-price big">' in open(f, encoding='utf-8').read())


def extract(s):
    """Current texts of a product page (what the admin page shows before an override exists)."""
    out = {'tagline': '', 'heading': '', 'intro': [], 'features': [], 'features_editable': False}
    m = TAGLINE.search(s)
    if m:
        out['tagline'] = text(m.group(2))
    m = INTRO.search(s)
    if m:
        out['heading'] = text(m.group(2))
        out['intro'] = [text(p) for p in re.findall(r'<p>(.*?)</p>', m.group(4), re.S)]
    sec = FEAT_SEC.search(s)
    if sec and len(TECH.findall(sec.group(0))) == 1:
        out['features'] = [[text(a), text(b)] for a, b in ART.findall(sec.group(0))]
        out['features_editable'] = True
    return out


def apply(s, o):
    if o.get('tagline'):
        s = TAGLINE.sub(lambda m: m.group(1) + E(o['tagline']) + m.group(3), s, 1)
    if o.get('heading') or o.get('intro'):
        def intro(m):
            head = E(o['heading']) if o.get('heading') else m.group(2)
            paras = ''.join(f'<p>{E(p)}</p>' for p in o['intro']) if o.get('intro') else m.group(4)
            return m.group(1) + head + m.group(3) + paras
        s = INTRO.sub(intro, s, 1)
    if o.get('features'):
        def feats(sec):
            if len(TECH.findall(sec.group(0))) != 1:
                return sec.group(0)
            arts = ''.join(f'<article><span class="num">{i:02d}</span><h3>{E(t)}</h3><p>{E(x)}</p></article>'
                           for i, (t, x) in enumerate(o['features'], 1))
            return TECH.sub(lambda m: m.group(1) + arts + m.group(3), sec.group(0), 1)
        s = FEAT_SEC.sub(feats, s, 1)
    return s


def load():
    p = os.path.join(ROOT, 'data', 'overrides.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'pages': {}}


if __name__ == '__main__':
    n = 0
    for page, o in load()['pages'].items():
        p = os.path.join(ROOT, page)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        t = apply(s, o)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
    print(f'mô tả sản phẩm đã sửa: {n} trang')
