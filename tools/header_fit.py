"""Header on narrow phones: menu button + logo + đại lý/hotline icons + VI/EN switch must fit without
horizontal scrolling (they need ~383px at the default spacing). Idempotent; run before clean_urls.py:
    python3 tools/header_fit.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = '''/* Header fit */
@media (max-width:419px){.h-main{gap:8px}.h-main .logo{width:104px}.h-tools{gap:0}.lang{padding:0 6px}}
@media (max-width:359px){.header .container{padding:0 12px}.h-main .logo{width:92px}}
'''
CSS_RX = re.compile(r'/\* Header fit \*/\n(?:@media[^\n]*\n)+')

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f, encoding='utf-8').read()
    if 'class="h-tools"' not in s:
        continue
    t = CSS_RX.sub('', s).replace('</style>', CSS + '</style>', 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        n += 1
print(f'đầu trang trên màn hình hẹp: cập nhật {n} trang')
