"""Build lop-xe.html (tire listing page) from corsa-pro.html shell."""
import sys, re, os
D = sys.argv[1]
C = 'https://cdn.shopify.com/s/files/1/0800/0549/7120/files'
shell = open(os.path.join(D, 'corsa-pro.html'), encoding='utf-8').read()

TIRES = [
    # (type, name, image, desc, chips, tag, link)
    ('road', 'Corsa PRO', 'corsa-pro-tlr-01.webp', 'Lốp đua cao cấp · Bám đường cả khi khô lẫn ướt', ['Tubeless-ready', '28–32mm'], ('Bán chạy', ''), 'corsa-pro.html'),
    ('road', 'Corsa PRO Speed', 'corsa-pro-speed-size30-01-HPNEW.webp', 'Lốp đua tính giờ & triathlon · Tối ưu tốc độ', ['Tubeless-ready', '24–30mm'], ('TT / Tri', 'dark'), ''),
    ('road', 'Corsa N.Ext', 'corsa-next-tlr-01.webp', 'Thi đấu & tập luyện dài ngày · Bền, chống thủng', ['Tubeless-ready', '24–34mm'], None, ''),
    ('road', 'Rubino', 'Rubino_1.webp', 'Lốp tập luyện hằng ngày · Tốc độ, bám đường, bền', ['Tubeless-ready', 'Có bản dùng săm', '26–34mm'], None, ''),
    ('mtb', 'Mezcal XC Race', 'mezcal-mtb-cross-country-race-1_2724a060-7d95-4efc-8ac6-1b67b1ff2160.webp', 'Lốp MTB · Cross-country', [], None, ''),
    ('gravel', 'Terreno PRO T30', 'terreno-PRO-T30-fineloose-gravel-01.webp', 'Lốp gravel · Sỏi mịn, đất tơi', [], ('Mới', ''), ''),
]
TYPES = [('all', 'Tất cả'), ('road', 'Road'), ('mtb', 'MTB'), ('gravel', 'Gravel'), ('dirtjump', 'DirtJump')]
INTRO = {
    'all': 'Lốp xe đạp Vittoria chính hãng cho mọi cung đường — từ đường đua road, đường mòn MTB đến sỏi đá gravel.',
    'road': 'Lốp road Vittoria: từ lốp đua Corsa PRO đến lốp tập luyện hằng ngày Rubino.',
    'mtb': 'Lốp MTB Vittoria cho cross country, trail và enduro.',
    'gravel': 'Lốp gravel Vittoria dòng Terreno cho đường sỏi, đất và địa hình hỗn hợp.',
    'dirtjump': 'Lốp DirtJump cho dirt jump, pump track và street.',
}

cards = ''
for t, name, img, desc, chips, tag, link in TIRES:
    tag_html = f'<span class="tag {tag[1]}">{tag[0]}</span>' if tag else ''
    chip_html = '<ul class="models">' + ''.join(f'<li>{c}</li>' for c in chips) + '</ul>' if chips else ''
    title = f'<a class="stretch" href="{link}">{name}</a>' if link else name
    cards += f'''
        <article class="p-card" data-type="{t}">
          <div class="p-img tire">{tag_html}<img src="{C}/{img}?width=600" alt="Lốp Vittoria {name}" loading="lazy"></div>
          <div class="p-body"><span class="p-brand">Vittoria · {dict(TYPES)[t]}</span><h3 class="p-name">{title}</h3><p class="p-desc">{desc}</p>{chip_html}<span class="p-price">1.980.000₫</span></div>
        </article>'''

tabs = ''.join(f'<a role="tab" href="#{k}" data-type="{k}" aria-selected="{"true" if k == "all" else "false"}">{v} <span class="count"></span></a>' for k, v in TYPES)

main = f'''<main id="main" class="pdp listing">
  <div class="container">
    <nav class="crumbs" aria-label="Đường dẫn"><ol>
      <li><a href="index.html">Trang chủ</a></li><li><a href="index.html#hot">Phụ tùng</a></li><li aria-current="page">Lốp xe</li></ol></nav>
  </div>

  <section class="list-hero">
    <img src="https://vittoria.com/cdn/shop/files/Banner_HERO_Horizontal_3_69510693-5265-4d5e-95ae-4706d0cb7fdd.webp?width=1920" alt="Nhóm người đạp xe gravel trên đường đất">
    <div class="container"><div class="lh-copy">
      <span class="kicker">Vittoria Tires</span>
      <h1>Lốp xe đạp</h1>
      <p>Lốp xe đạp Vittoria chính hãng — thương hiệu lốp đến từ Ý, phân phối bởi Spinlab.</p>
    </div></div>
  </section>

  <div class="container">
    <div class="list-bar">
      <div class="mtb-tabs list-tabs" role="tablist" aria-label="Loại lốp">{tabs}</div>
    </div>
    <p class="list-intro" id="list-intro" aria-live="polite">{INTRO["all"]}</p>
    <div class="grid" id="tire-grid">{cards}
    </div>
    <div class="empty" id="tire-empty" hidden><p><b>Lốp DirtJump đang được cập nhật.</b> Liên hệ Spinlab để được tư vấn mẫu lốp phù hợp.</p><a class="btn btn-outline" href="tel:0399337533">Gọi 0399 337 533</a></div>

    <section class="pdp-sec">
      <div class="help">
        <div><h2>Chưa biết chọn lốp nào?</h2><p>Gửi cho Spinlab loại xe, cỡ vành và cung đường bạn hay đi — chúng tôi sẽ tư vấn mẫu lốp và kích thước phù hợp.</p></div>
        <div class="actions"><a class="btn btn-yellow" href="tel:0399337533">Gọi 0399 337 533</a><a class="btn btn-zalo" href="https://zalo.me/0900000000" target="_blank" rel="noopener"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg" alt="" width="22" height="22">Chat Zalo</a></div>
      </div>
    </section>
  </div>
</main>'''

css = '''
/* Tire listing page */
.list-hero{position:relative;min-height:300px;display:flex;align-items:flex-end;color:#fff;overflow:hidden;margin-bottom:8px}
.list-hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:60% 50%}
.list-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.65),rgba(0,0,0,.15) 70%)}
.list-hero .container{position:relative;z-index:1;width:100%}
.lh-copy{padding:48px 0 40px;max-width:560px}
.lh-copy .kicker{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em}
.lh-copy h1{margin:8px 0 10px;font-size:clamp(34px,5vw,56px);font-weight:800;text-transform:uppercase;line-height:1}
.lh-copy p{margin:0;font-size:17px}
.list-bar{position:sticky;top:115px;z-index:20;background:#fff;padding-top:16px}
@media (min-width:1024px){.list-bar{top:129px}}
.list-tabs{margin-bottom:0}
.list-tabs a{flex:none;display:flex;align-items:center;gap:6px;min-height:48px;padding:0 18px;border-bottom:3px solid transparent;font-weight:700;font-size:15px;text-transform:uppercase;letter-spacing:.02em;color:var(--muted);margin-bottom:-1px}
.list-tabs a:hover{color:var(--text)}
.list-tabs a[aria-selected=true]{color:var(--brand-red);border-bottom-color:var(--brand-red)}
.list-tabs .count{font-size:12px;font-weight:600;color:var(--muted)}
.list-intro{margin:20px 0;color:var(--muted)}
#tire-grid .p-card[hidden]{display:none}
'''

js = '''// Tire listing: filter by type, synced with URL hash (#road, #mtb, #gravel, #dirtjump)
(() => {
  const intro = %s;
  const tabs=[...document.querySelectorAll('.list-tabs [role=tab]')], cards=[...document.querySelectorAll('#tire-grid .p-card')];
  tabs.forEach(t=>{ const k=t.dataset.type; t.querySelector('.count').textContent='('+cards.filter(c=>k==='all'||c.dataset.type===k).length+')'; });
  const show=k=>{ if(!intro[k]) k='all';
    tabs.forEach(t=>t.setAttribute('aria-selected',t.dataset.type===k));
    let n=0; cards.forEach(c=>{ const on=k==='all'||c.dataset.type===k; c.hidden=!on; n+=on; });
    document.getElementById('tire-empty').hidden=n>0; document.getElementById('list-intro').textContent=intro[k]; };
  tabs.forEach(t=>t.addEventListener('click',e=>{ e.preventDefault(); const k=t.dataset.type; show(k); try{ history.replaceState(null,'',k==='all'?location.pathname+location.search:'#'+k); }catch(_){} }));
  window.addEventListener('hashchange',()=>show(location.hash.slice(1)));
  show(location.hash.slice(1));
})();
''' % repr(INTRO).replace("'", '"')

p = shell
p = re.sub(r'<title>.*?</title>', '<title>Lốp xe đạp Vittoria — Spinlab</title>', p, 1, flags=re.S)
p = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Lốp xe đạp Vittoria chính hãng: lốp Road, MTB, Gravel, DirtJump. Phân phối bởi Spinlab.">', p, 1)
p = p.replace('</style>', css + '</style>', 1)
p = re.sub(r'<main id="main" class="pdp">.*?</main>', lambda m: main, p, 1, flags=re.S)
p = re.sub(r'// Product gallery \+ size selector.*?\}\)\(\);\n', lambda m: js, p, 1, flags=re.S)
open(os.path.join(D, 'lop-xe.html'), 'w', encoding='utf-8').write(p)
print(len(p), p.count('data-type="road"'), 'Tire listing' in p)
