"""Category filter on listing pages with section pills (tubeless, phụ kiện, brand pages):
a menu link or pill with #category shows only that category's products; the "Tất cả" pill, or opening the page
without a #category (e.g. "Xem tất cả…" or the brand menu), shows every product of the page.
(lop-xe.html and xe-mtb.html have their own type tabs.) Idempotent; run before clean_urls.py:
    python3 tools/cat_filter.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'dai-ly.html'}
PILL = '<li><a href="#" data-all>Tất cả</a></li>'
CSS = '''/* Category filter */
.brand-nav a.on{background:var(--text);border-color:var(--text);color:#fff}
.brand-nav a.on small{color:rgba(255,255,255,.7)}
'''
JS = '''// Category filter: #category shows only that category; "Tất cả" or the page without a hash shows everything
(() => {
  const secs=[...document.querySelectorAll('section.brand-cat[id]')], pills=[...document.querySelectorAll('.brand-nav a')], bar=document.querySelector('.brand-nav');
  const apply=scroll=>{ const k=decodeURIComponent(location.hash.slice(1)), one=secs.some(s=>s.id===k);
    secs.forEach(s=>s.hidden=one&&s.id!==k);
    pills.forEach(a=>{ const on=one?a.getAttribute('href')==='#'+k:a.hasAttribute('data-all'); a.classList.toggle('on',on); on?a.setAttribute('aria-current','true'):a.removeAttribute('aria-current'); });
    document.querySelectorAll('.nav-top[aria-expanded="true"]').forEach(b=>b.setAttribute('aria-expanded','false'));
    if(scroll&&bar){ const head=document.querySelector('.header'); window.scrollTo({top:bar.getBoundingClientRect().top+scrollY-(head?head.getBoundingClientRect().height:0)-12, behavior:'smooth'}); } };
  pills.filter(a=>a.hasAttribute('data-all')).forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); history.pushState(null,'',location.pathname+location.search); apply(true); }));
  addEventListener('hashchange',()=>apply(true)); addEventListener('popstate',()=>apply(false));
  apply(false); if(secs.some(s=>s.id===decodeURIComponent(location.hash.slice(1)))) requestAnimationFrame(()=>apply(true));
})();
'''
CSS_RX = re.compile(r'/\* Category filter \*/\n(?:\.brand-nav[^\n]*\n)+')
JS_RX = re.compile(r'// Category filter:.*?\}\)\(\);\n', re.S)
OLD_RX = re.compile(r'<script>\n// Category filter:.*?</script>\n', re.S)  # earlier version: own <script> tag
NAV_RX = re.compile(r'(<nav class="brand-nav"[^>]*><div class="container"><ul>)')

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f, encoding='utf-8').read()
    t = CSS_RX.sub('', JS_RX.sub('', OLD_RX.sub('', s.replace(PILL, ''))))
    if os.path.basename(f) not in SKIP and 'class="brand-nav"' in t and len(re.findall(r'<section class="brand-cat" id=', t)) > 1:
        t = NAV_RX.sub(lambda m: m.group(1) + PILL, t, 1)
        t = t.replace('</style>', CSS + '</style>', 1)
        i = t.rindex('</script>\n</body>')  # inside the page's main script, like the other page scripts
        t = t[:i] + JS + t[i:]
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        n += 1

# MTB bikes (xe-mtb.html): a "Tất cả" tab, selected when the page opens without a #discipline ("Xem tất cả xe địa hình")
MTB_CSS = '''/* MTB all tab */
.mtb-all .mtb-panel::before{content:attr(data-title);display:block;margin:28px 0 4px;font-size:clamp(22px,2.6vw,30px);font-weight:800;text-transform:uppercase}
.mtb-all .mtb-tabs+.mtb-panel::before{margin-top:8px}
'''
MTB_JS = '''// MTB all tab: "Tất cả" shows every discipline, each under its own heading
(() => {
  const all=document.getElementById('tab-all'); if(!all) return;
  const box=all.closest('.section'), panels=[...box.querySelectorAll('.mtb-panel')];
  const sync=()=>{ const on=all.getAttribute('aria-selected')==='true'; box.classList.toggle('mtb-all',on); if(on) panels.forEach(p=>p.hidden=false); };
  box.querySelectorAll('[role=tab]').forEach(t=>t.addEventListener('click',()=>{ sync(); const k=t.id.slice(4);
    try{ history.replaceState(null,'',t===all?location.pathname+location.search:'#'+k); }catch(_){} }));
  sync();
})();
'''
MTB_CSS_RX = re.compile(r'/\* MTB all tab \*/\n(?:\.mtb-all[^\n]*\n)+')
MTB_JS_RX = re.compile(r'// MTB all tab:.*?\}\)\(\);\n', re.S)
f = os.path.join(ROOT, 'xe-mtb.html')
s = open(f, encoding='utf-8').read()
t = MTB_JS_RX.sub('', MTB_CSS_RX.sub('', s))
t = re.sub(r'\n\s*<button role="tab" id="tab-all"[^>]*>[^<]*</button>', '', t)
tabs = re.findall(r'<button role="tab" id="tab-([a-z]+)"[^>]*>([^<]+)</button>', t)
for k, label in tabs:
    t = re.sub(r'<button role="tab" id="tab-%s"[^>]*>' % k, f'<button role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="false" tabindex="-1">', t, 1)
    t = re.sub(r'<div class="mtb-panel" role="tabpanel" id="panel-%s"[^>]*>' % k, f'<div class="mtb-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" data-title="{label}">', t, 1)
t = t.replace('<div class="mtb-tabs" role="tablist" aria-label="Loại xe địa hình">',
              '<div class="mtb-tabs" role="tablist" aria-label="Loại xe địa hình">\n        <button role="tab" id="tab-all" aria-selected="true">Tất cả</button>', 1)
t = t.replace('</style>', MTB_CSS + '</style>', 1)
i = t.rindex('</script>\n</body>')
t = t[:i] + MTB_JS + t[i:]
if t != s:
    open(f, 'w', encoding='utf-8').write(t)
    n += 1
print(f'lọc theo danh mục: cập nhật {n} trang')
