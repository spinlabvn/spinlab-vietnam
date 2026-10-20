"""Brand logos with equal visual weight on every page: homepage tiles, the "Thương hiệu" menu and the
/thuong-hieu hub (build_hubs.py copies the homepage tiles).

All logos are horizontal and tightly cropped (img/brands/*, Vittoria's own SVG). Each one gets a width so
that every logo covers about the same area: width = --lh * sqrt(5 * aspect) * optical factor, i.e. a 5:1 logo is exactly
--lh tall, a longer wordmark is a little lower and a squarer one a little taller.
Run before build_hubs.py:
    python3 tools/brand_logos.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (slug, name, src, aspect width/height, optical factor: >1 for logos whose wordmark is small next to an icon)
LOGOS = [
    ('polygon', 'Polygon', 'img/brands/polygon.png', 480 / 96, 1.3),
    ('vittoria', 'Vittoria', 'https://vittoria.com/cdn/shop/files/Vittoria_logo_black.svg?v=1696407669', 131 / 26, 1),
    ('emume', 'Emume', 'img/brands/emume.png', 397 / 88, 1.2),
    ('story-bike', 'Story Bike', 'img/brands/story.png', 378 / 47, .95),
]
wf = lambda ar, k: round((5 * ar) ** .5 * k, 3)


def img(src, ar, k, alt):
    return f'<img class="brand-logo" style="--wf:{wf(ar, k)}" src="{src}" alt="{alt}" width="{round(ar * 40)}" height="40" loading="lazy">'


WMAX = max(wf(ar, k) for *_, ar, k in LOGOS)
CSS = '''/* Brand logos */
.brand-logo{display:block;height:auto;width:min(calc(var(--lh,30px) * var(--wf,5)),calc(100cqi * var(--wf,5) / %s))}
.brand-tile,.brand-menu a,.hub-logo .hi{container-type:inline-size}
.brand-tile{--lh:30px}
.brand-menu{--lh:20px}
.hub-logo{--lh:40px}
''' % WMAX

MENU = '<ul class="brand-menu">\n' + ''.join(
    f'              <li><a href="/thuong-hieu-{s}" aria-label="{n}">{img(src, ar, k, "")}</a></li>\n' for s, n, src, ar, k in LOGOS
) + '            </ul>'

TILES = '\n'.join(
    f'        <a class="brand-tile" href="/thuong-hieu-{s}" aria-label="Sản phẩm {n}"><span class="bt-inner">{img(src, ar, k, n)}</span></a>'
    for s, n, src, ar, k in LOGOS)

OLD_CSS = [r'\.brand-tile img\{[^}]*\}\n', r'\.brand-tile img\.wide\{[^}]*\}\n', r'\.logo-crop\{[^}]*\}\n',
           r'\.brand-menu img\{[^}]*\}\n', r'\.brand-menu img\.wide\{[^}]*\}\n', r'\.brand-menu \.logo-crop\{[^}]*\}\n',
           r'/\* Brand logos \*/\n(?:\.[^\n]*\n){4,5}']

n = 0
for p in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    if p.endswith('v1-premium.html'):
        continue
    s = open(p, encoding='utf-8').read()
    t = s
    for rx in OLD_CSS:
        t = re.sub(rx, '', t)
    if '<style>' in t:
        t = t.replace('</style>', CSS + '</style>', 1)
    t = re.sub(r'<ul class="brand-menu">.*?</ul>', lambda m: MENU, t, flags=re.S)
    t = re.sub(r'(?:[ \t]*<a class="brand-tile" href=.*?</a>\n?)+',
               lambda m: TILES + ('\n' if m.group(0).endswith('\n') else ''), t, count=1, flags=re.S)
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)
        n += 1
print(f'logo thương hiệu đồng bộ trên {n} trang')
