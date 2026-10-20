"""Rebuild the product grid of lop-xe.html from the tire generators' card files (stock-filtered).
Run after vtires.py and terreno.py:  python3 tires_listing.py ../.."""
import os, re, sys
D = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, 'vittoria-json')
rd = lambda p: open(p, encoding='utf-8').read()

page = rd(os.path.join(D, 'lop-xe.html'))
grid_a = page.index('<div class="grid" id="tire-grid">') + len('<div class="grid" id="tire-grid">')
grid_z = page.index('\n    </div>', grid_a)
old = page[grid_a:grid_z]
# Corsa PRO has a hand-built page; keep its card
corsa = re.search(r'<article class="p-card"(?:(?!</article>).)*href="/?corsa-pro(?:\.html)?".*?</article>', old, re.S).group(0)
cards = [corsa] + [c for f in ('road', 'mtb', 'dirtjump') for c in re.findall(r'<article class="p-card".*?</article>', rd(os.path.join(J, f'{f}-cards.html')), re.S)]
cards += re.findall(r'<article class="p-card".*?</article>', rd(os.path.join(J, 'terreno-cards.html')), re.S)
page = page[:grid_a] + '\n' + '\n'.join(cards) + page[grid_z:]
page = page.replace('<a role="tab" href="xe-mtb.html" data-type="mtb"', '<a role="tab" href="#mtb" data-type="mtb"')
if not any('data-type="dirtjump"' in c for c in cards):   # no DirtJump tire in stock: drop the tab
    page = re.sub(r'<a role="tab" href="#dirtjump" data-type="dirtjump"[^>]*>DirtJump <span class="count"></span></a>', '', page)
open(os.path.join(D, 'lop-xe.html'), 'w', encoding='utf-8').write(page)
print('lop-xe.html', len(cards), 'lốp')
