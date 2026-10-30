"""Footer "Liên hệ" column on every page: showroom address, hotline and a small Google Map of the showroom
(the "Công Ty TNHH Spinlab Việt Nam" place on Google Maps). Idempotent; run before clean_urls.py:
    python3 tools/footer.py
"""
import glob, os, re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACE = 'Công Ty TNHH Spinlab Việt Nam'
EMBED = f'https://maps.google.com/maps?q={quote(PLACE)}&hl=vi&z=16&output=embed'
LINK = f'https://www.google.com/maps/search/?api=1&query={quote(PLACE)}'
COL = ('<div class="f-contact"><h4>Liên hệ</h4><ul><li>Showroom: 13 đường 14, khu phố 4, phường An Khánh, TP. Hồ Chí Minh</li>'
       '<li><a href="tel:0399337533">0399 337 533</a></li></ul>'
       f'<iframe class="f-map" src="{EMBED}" title="Bản đồ showroom Spinlab" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
       f'<a class="f-dir" href="{LINK}" target="_blank" rel="noopener">Xem đường đi trên Google Maps</a></div>')
CSS = '''/* Footer map */
.footer .f-map{display:block;width:100%;max-width:340px;height:160px;margin-top:14px;border:0;border-radius:8px;background:#2a2a2a}
.footer .f-dir{display:inline-block;margin-top:10px;color:var(--brand-yellow);font-weight:600;text-decoration:underline;text-underline-offset:3px}
.footer .f-dir:hover{color:#fff}
'''
OLD = re.compile(r'<div(?: class="f-contact")?><h4>Liên hệ</h4>.*?</ul>(?:<iframe class="f-map".*?</a>)?</div>', re.S)
CSS_RX = re.compile(r'/\* Footer map \*/\n(?:\.footer \.f-[^\n]*\n)+')

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f, encoding='utf-8').read()
    foot = s.find('<footer class="footer">')
    if foot < 0:
        continue
    t = s[:foot] + OLD.sub(lambda m: COL, s[foot:], 1)
    t = CSS_RX.sub('', t).replace('</style>', CSS + '</style>', 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        n += 1
print(f'chân trang (bản đồ showroom): cập nhật {n} trang')
