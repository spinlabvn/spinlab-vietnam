"""Christmas look for every page: snowflake pattern on the page background, a string of lights under the header,
falling snow over the homepage slider and listing banners, and a snow edge on the footer.
Switched on/off by "christmas" in data/settings.json (admin page: Sản phẩm → Giao diện Giáng sinh).
Idempotent; run before clean_urls.py:
    python3 tools/season.py
"""
import glob, json, math, os, random, re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ON = json.load(open(os.path.join(ROOT, 'data', 'settings.json'), encoding='utf-8')).get('christmas', False)


def svg(w, h, body):
    return 'url("data:image/svg+xml,' + quote(f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'>{body}</svg>", safe="/:=' ") + '")'


def flake(x, y, r, color, op):
    """six-armed snowflake: three crossing strokes, each arm with a small V branch"""
    d = ''
    for k in range(6):
        a = math.radians(60 * k)
        ex, ey = x + r * math.cos(a), y + r * math.sin(a)
        d += f'M{x:.1f} {y:.1f}L{ex:.1f} {ey:.1f}'
        bx, by = x + r * .6 * math.cos(a), y + r * .6 * math.sin(a)
        for s in (-1, 1):
            b = a + s * math.radians(40)
            d += f'M{bx:.1f} {by:.1f}L{bx + r * .32 * math.cos(b):.1f} {by + r * .32 * math.sin(b):.1f}'
    return f"<path d='{d}' stroke='{color}' stroke-opacity='{op}' stroke-width='1.3' stroke-linecap='round' fill='none'/>"


def star(x, y, r, color, op):
    """four-point sparkle"""
    q = r * .28
    return (f"<path d='M{x} {y - r}Q{x + q} {y - q} {x + r} {y}Q{x + q} {y + q} {x} {y + r}Q{x - q} {y + q} {x - r} {y}Q{x - q} {y - q} {x} {y - r}Z'"
            f" fill='{color}' fill-opacity='{op}'/>")


RED, GOLD = '#8E210A', '#C9961E'
PATTERN = svg(220, 220, flake(42, 48, 13, RED, .09) + flake(150, 34, 7, GOLD, .32) + flake(118, 128, 16, RED, .07)
              + flake(34, 168, 8, GOLD, .3) + flake(190, 178, 11, RED, .08) + star(92, 70, 5, GOLD, .35)
              + star(178, 98, 3.5, GOLD, .3) + star(70, 200, 4, GOLD, .3) + star(12, 104, 3, RED, .12))


def snow(size, n, rmin, rmax, omin, omax, seed):
    rnd = random.Random(seed)
    return svg(size, size, ''.join(
        f"<circle cx='{rnd.uniform(0, size):.0f}' cy='{rnd.uniform(0, size):.0f}' r='{rnd.uniform(rmin, rmax):.1f}' fill='#fff' fill-opacity='{rnd.uniform(omin, omax):.2f}'/>"
        for _ in range(n)))


NEAR = snow(300, 26, 1.6, 3.4, .6, .95, 7)
FAR = snow(200, 34, .8, 1.8, .35, .7, 11)
# garland: dark-green wire with red, gold and green bulbs; the glow layer pulses under every other bulb
WIRE = "<path d='M0 3Q18 11 36 3Q54 11 72 3' stroke='#25472F' stroke-width='1.4' fill='none'/>"
BULB = lambda x, y, c: f"<rect x='{x - 1.6}' y='{y - 1}' width='3.2' height='3' rx='.6' fill='#25472F'/><ellipse cx='{x}' cy='{y + 5}' rx='3.2' ry='4.4' fill='{c}'/><ellipse cx='{x - 1}' cy='{y + 3.6}' rx='.9' ry='1.4' fill='#fff' fill-opacity='.55'/>"
LIGHTS = svg(72, 18, WIRE + BULB(18, 7, '#D7263D') + BULB(36, 3, '#F4B400') + BULB(54, 7, '#2E9E4F'))
GLOW = svg(144, 18, "<defs><radialGradient id='g'><stop offset='0' stop-color='#fff3b0' stop-opacity='.95'/><stop offset='1' stop-color='#fff3b0' stop-opacity='0'/></radialGradient></defs>"
           "<circle cx='18' cy='12' r='8' fill='url(#g)'/><circle cx='108' cy='8' r='8' fill='url(#g)'/>")
DRIFT = svg(160, 18, "<path d='M0 0H160V7Q146 15 128 8Q112 2 96 9Q80 16 62 8Q46 1 30 9Q14 16 0 8Z' fill='#fff'/>")

CSS = f'''/* Christmas */
body{{background-color:#FFFBF4;background-image:{PATTERN};background-size:220px 220px}}
.header::before,.header::after{{content:"";position:absolute;left:0;right:0;bottom:-18px;height:22px;pointer-events:none}}
.header::after{{background:{LIGHTS} 0 0/88px 22px repeat-x}}
.header::before{{background:{GLOW} 0 0/176px 22px repeat-x;animation:xglow 1.8s ease-in-out infinite alternate}}
.hero::after,.list-hero::before{{content:"";position:absolute;inset:0;z-index:4;pointer-events:none;background-image:{NEAR},{FAR};background-size:300px 300px,200px 200px;animation:xsnow 16s linear infinite}}
.list-hero::before{{z-index:1}}
.footer{{position:relative;background-image:{FAR};background-size:200px 200px;animation:xfall 40s linear infinite}}
.footer::before{{content:"";position:absolute;left:0;right:0;top:-1px;height:18px;background:{DRIFT} 0 0/160px 18px repeat-x;pointer-events:none}}
@keyframes xsnow{{to{{background-position:60px 300px,-40px 200px}}}}
@keyframes xfall{{to{{background-position:0 200px}}}}
@keyframes xglow{{from{{opacity:.15}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.header::before,.hero::after,.list-hero::before,.footer{{animation:none}}}}
'''
CSS_RX = re.compile(r'/\* Christmas \*/\n.*?@media \(prefers-reduced-motion:reduce\)\{[^\n]*\n', re.S)

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f, encoding='utf-8').read()
    if 'class="header"' not in s:
        continue
    t = CSS_RX.sub('', s)
    if ON:
        t = t.replace('</style>', CSS + '</style>', 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        n += 1
print(f'giao diện Giáng sinh {"BẬT" if ON else "TẮT"}: cập nhật {n} trang')
