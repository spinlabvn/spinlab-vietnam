"""Product comparison (like BikesOnline): compare toggles on product cards, a compare tray, and so-sanh.html.

What it does
- Reads every product page listed in data/catalog.json and extracts name, image, price, category and specs
  (spec lists, spec tables, technology/feature titles, sizes).
- Writes so-sanh.html with that data embedded (works without a server).
- Injects the shared compare CSS + script into every page, and a <meta name="product-id"> into product pages
  (always rewritten, so pages generated from a shell never keep the shell's id).

Run after build_new_products.py:
    python3 tools/build_compare.py
"""
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda f: open(os.path.join(ROOT, f), encoding='utf-8').read()
W = lambda f, s: open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)
T = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('\u200b', '')).strip()
MAX = 4


def uniq(xs):
    out = []
    for x in xs:
        if x and x not in out:
            out.append(x)
    return out


def weight_range(vals):
    nums = [float(m.group(1)) for v in vals for m in [re.search(r'(\d+(?:\.\d+)?)\s*g', v)] if m]
    if not nums:
        return ', '.join(uniq(vals))
    lo, hi = min(nums), max(nums)
    f = lambda n: f'{n:g} g'
    return f(lo) if lo == hi else f'{f(lo)} – {f(hi)}'


def extract(fname):
    s = R(fname)
    m = re.search(r'<main id="main".*?</main>', s, re.S).group(0)
    g = lambda pat: (re.search(pat, m, re.S) or [None, ''])[1]
    d = {'id': fname, 'name': T(g(r'<h1>(.*?)</h1>')), 'img': (re.search(r'src="([^"]+)"', g(r'(<img[^>]*id="g-main"[^>]*>)')) or [None, ''])[1],
         'price': T(g(r'<span class="p-price big">(.*?)</span>')), 'cat': T(g(r'<div class="buy">\s*<span class="p-brand">(.*?)</span>')),
         'tagline': T(g(r'<p class="tagline">(.*?)</p>')), 'specs': []}
    add = lambda grp, k, v: v and d['specs'].append([grp, k, v])
    add('Tổng quan', 'Danh mục', d['cat'])
    add('Tổng quan', 'Mô tả ngắn', d['tagline'])
    # sizes / variants offered on the page
    sizes = uniq(T(x) for x in re.findall(r'<input type="radio" name="size"[^>]*><span>(.*?)</span>', m))
    if sizes:
        add('Tổng quan', 'Kích thước / size', ', '.join(sizes))
    colors = uniq(T(x) for x in re.findall(r'<input type="radio" name="color"[^>]*><span>(.*?)</span>', m))
    if colors:
        add('Tổng quan', 'Màu', ', '.join(colors))
    variants = re.findall(r'<input type="radio" name="variant"', m)
    if variants:
        add('Tổng quan', 'Phối màu', f'{len(variants)} lựa chọn')
    # spec lists, grouped by the <h3> right before them
    for grp, body in re.findall(r'(?:<h3>([^<]*)</h3>)?\s*<dl class="spec-list">(.*?)</dl>', m, re.S):
        for k, v in re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', body, re.S):
            add(T(grp) or 'Thông số', T(k), T(v))
    # spec tables (tires, tubeless): summarise each column
    for tb in re.findall(r'<table class="[^"]*spec-table[^"]*">(.*?)</table>', m, re.S):
        heads = [T(h) for h in re.findall(r'<th scope="col">(.*?)</th>', tb)]
        rows = [[T(c) for c in re.findall(r'<td>(.*?)</td>', r)] for r in re.findall(r'<tr[^>]*>(.*?)</tr>', re.search(r'<tbody>(.*?)</tbody>', tb, re.S).group(1), re.S)]
        for i, h in enumerate(heads):
            if h in ('Mã sản phẩm', 'Phiên bản'):
                continue
            vals = [r[i] for r in rows if i < len(r) and r[i] not in ('—', '')]
            add('Bảng kỹ thuật', h, weight_range(vals) if h.startswith('Trọng lượng') else ', '.join(uniq(vals)))
    # Corsa PRO style page: sizes table with weights in <th> rows
    if not d['specs'] or not any(s[1].startswith('Trọng lượng') for s in d['specs']):
        ws = re.findall(r'data-w="(\d+)"', m)
        if ws:
            add('Bảng kỹ thuật', 'Trọng lượng', weight_range([w + ' g' for w in ws]))
    # versions table
    vers = uniq(T(x) for x in re.findall(r'<table class="vtable">.*?<tbody>(.*?)</tbody>', m, re.S) for x in re.findall(r'<th scope="row">(.*?)</th>', x))
    if vers:
        add('Tổng quan', 'Phiên bản', ', '.join(vers))
    # technology / features (first block only)
    sec = re.search(r'<section class="pdp-sec" id="(?:cong-nghe|tinh-nang)">(.*?)</section>', m, re.S)
    if sec:
        first = re.search(r'<div class="tech-v" data-tech="0">(.*?)</div></div>', sec.group(1), re.S)
        titles = uniq(T(x) for x in re.findall(r'<h3>(.*?)</h3>', first.group(1) if first else sec.group(1)))
        if titles:
            add('Tổng quan', 'Công nghệ / tính năng', ' · '.join(titles))
    return d


cat = json.load(open(os.path.join(ROOT, 'data', 'catalog.json'), encoding='utf-8'))
ids = [p['href'] for p in cat['products'] if os.path.exists(os.path.join(ROOT, p['href']))]
DATA = {i: extract(i) for i in ids}

CSS = '''/* Compare */
.cmp-toggle{position:absolute;top:10px;right:10px;z-index:3;display:inline-flex;align-items:center;gap:6px;min-height:32px;padding:0 10px;border-radius:999px;background:rgba(255,255,255,.92);border:1px solid var(--line);font-size:12px;font-weight:600;cursor:pointer;user-select:none}
.cmp-toggle input{width:16px;height:16px;margin:0;accent-color:var(--brand-red)}
.cmp-toggle:has(input:checked){border-color:var(--brand-red);color:var(--brand-red)}
.cmp-add{margin-top:10px}
.cmp-add[aria-pressed="true"]{border-color:var(--brand-red);color:var(--brand-red)}
.cmp-tray{position:fixed;left:0;right:0;bottom:0;z-index:70;background:#fff;border-top:1px solid var(--line);box-shadow:0 -8px 24px rgba(0,0,0,.08);transform:translateY(110%);transition:transform .25s ease}
.cmp-tray.on{transform:none}
.cmp-tray .container{display:flex;align-items:center;gap:12px;padding-top:10px;padding-bottom:10px}
.cmp-items{display:flex;gap:8px;flex:1;min-width:0;overflow-x:auto;list-style:none;margin:0;padding:0}
.cmp-items li{position:relative;flex:0 0 auto;width:64px;height:64px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);display:grid;place-items:center}
.cmp-items li.empty{border-style:dashed;font-size:11px;color:var(--muted);text-align:center;padding:4px}
.cmp-items img{max-width:56px;max-height:56px;object-fit:contain;mix-blend-mode:multiply}
.cmp-items button{position:absolute;top:-8px;right:-8px;width:24px;height:24px;border-radius:50%;border:1px solid var(--line);background:#fff;font-size:14px;line-height:1;display:grid;place-items:center}
.cmp-actions{display:flex;gap:8px;align-items:center;flex:0 0 auto}
.cmp-actions .btn{min-height:44px;padding:0 16px;font-size:13px}
.cmp-actions .btn[aria-disabled="true"]{opacity:.45;pointer-events:none}
.cmp-clear{border:0;background:none;font-size:13px;text-decoration:underline;color:var(--muted);min-height:44px}
body.cmp-open .zalo-fab{bottom:96px}
body.cmp-open .ribbon{bottom:96px}
@media (max-width:600px){.cmp-items li{width:52px;height:52px}.cmp-items img{max-width:44px;max-height:44px}.cmp-clear{display:none}}
'''

JS = '''// Compare products: toggles on cards / product page, tray, link to so-sanh.html (max %d)
(() => {
  const MAX=%d, KEY='spinlab-compare';
  const norm=h=>{ h=(h||'').split('#')[0].split('?')[0].replace(/^\//,''); if(h===''||h==='trangchu') h='index'; return /\.html$/.test(h)?h:h+'.html'; };
  let mem=[];
  const load=()=>{ try{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ return mem; } };
  const save=l=>{ mem=l; try{ localStorage.setItem(KEY,JSON.stringify(l)); }catch(e){} render(); };
  const has=id=>load().some(x=>x.id===id);
  const toggle=item=>{ let l=load(); if(l.some(x=>x.id===item.id)) l=l.filter(x=>x.id!==item.id);
    else { if(l.length>=MAX){ alert('Chỉ so sánh tối đa '+MAX+' sản phẩm. Bỏ bớt một sản phẩm để thêm.'); render(); return; } l.push(item); }
    save(l); };
  const home=document.querySelector('meta[name="page"][content="home"]'), compare=document.querySelector('meta[name="page"][content="compare"]');
  // card toggles (listing pages; not on the homepage or in "related" strips)
  if(!home && !compare) document.querySelectorAll('.p-card').forEach(c=>{
    if(c.closest('.related')) return;
    const a=c.querySelector('a.stretch'), box=c.querySelector('.p-img'); if(!a||!box) return;
    const id=norm(a.getAttribute('href')), img=box.querySelector('img');
    const lab=document.createElement('label'); lab.className='cmp-toggle';
    lab.innerHTML='<input type="checkbox"> So sánh';
    const inp=lab.querySelector('input'); inp.dataset.cmp=id;
    inp.addEventListener('change',()=>toggle({id,name:a.textContent.trim(),img:img?img.getAttribute('src'):'',price:(c.querySelector('.p-price')||{}).textContent||''}));
    box.appendChild(lab);
  });
  // product page button
  const pid=document.querySelector('meta[name="product-id"]'), buy=document.querySelector('.buy .price-row');
  if(pid && buy){ const id=pid.content, b=document.createElement('button'); b.type='button'; b.className='btn btn-outline cmp-add'; b.dataset.cmp=id;
    b.addEventListener('click',()=>toggle({id,name:(document.querySelector('.buy h1')||{}).textContent||id,img:(document.getElementById('g-main')||{}).getAttribute?.('src')||'',price:(document.querySelector('.p-price.big')||{}).textContent||''}));
    buy.after(b); }
  // tray
  const tray=document.createElement('div'); tray.className='cmp-tray'; tray.setAttribute('role','region'); tray.setAttribute('aria-label','Sản phẩm so sánh');
  tray.innerHTML='<div class="container"><ul class="cmp-items"></ul><div class="cmp-actions"><button type="button" class="cmp-clear">Xoá hết</button><a class="btn btn-primary cmp-go" href="/so-sanh">So sánh</a></div></div>';
  if(!compare) document.body.appendChild(tray);
  tray.querySelector('.cmp-clear').addEventListener('click',()=>save([]));
  function render(){
    const l=load();
    document.querySelectorAll('input[data-cmp]').forEach(i=>i.checked=l.some(x=>x.id===i.dataset.cmp));
    document.querySelectorAll('button.cmp-add').forEach(b=>{ const on=l.some(x=>x.id===b.dataset.cmp); b.setAttribute('aria-pressed',on); b.textContent=on?'✓ Đã thêm vào so sánh':'+ Thêm vào so sánh'; });
    const ul=tray.querySelector('.cmp-items');
    ul.innerHTML=l.map(x=>`<li title="${x.name}"><img src="${x.img}" alt="${x.name}"><button type="button" aria-label="Bỏ ${x.name} khỏi so sánh" data-rm="${x.id}">×</button></li>`).join('')+
      Array.from({length:MAX-l.length},()=>'<li class="empty">Thêm sản phẩm</li>').join('');
    ul.querySelectorAll('[data-rm]').forEach(b=>b.addEventListener('click',()=>save(load().filter(x=>x.id!==b.dataset.rm))));
    const go=tray.querySelector('.cmp-go'); go.textContent='So sánh ('+l.length+')';
    go.href='/so-sanh?ids='+l.map(x=>encodeURIComponent(x.id.replace(/\.html$/,''))).join(',');
    go.setAttribute('aria-disabled',l.length<2);
    const on=l.length>0 && !compare; tray.classList.toggle('on',on); document.body.classList.toggle('cmp-open',on);
  }
  window.spinlabCompare={load,save,render};
  render();
})();
''' % (MAX, MAX)

PAGE_CSS = '''/* Compare page */
.cmp-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:12px;margin:8px 0 16px}
.cmp-head h1{margin:0;font-size:clamp(26px,3.4vw,40px);font-weight:800;text-transform:uppercase}
.cmp-diff{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:14px;min-height:44px}
.cmp-diff input{width:18px;height:18px;accent-color:var(--brand-red)}
.cmp-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);margin-bottom:56px}
.cmp-table{border-collapse:separate;border-spacing:0;width:100%;min-width:640px;font-size:14px}
.cmp-table th,.cmp-table td{padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
.cmp-table tbody th{position:sticky;left:0;background:#fff;width:180px;min-width:140px;font-weight:600;color:var(--muted);z-index:1}
.cmp-table thead th{background:#fff;vertical-align:bottom}
.cmp-table thead th:first-child{position:sticky;left:0;z-index:2}
.cmp-table td{min-width:200px}
.cmp-table tr.grp th{background:var(--surface);color:var(--text);text-transform:uppercase;letter-spacing:.04em;font-size:12px}
.cmp-table tr.grp td{background:var(--surface)}
.cmp-table tr.same.hide{display:none}
.cmp-card{display:grid;gap:8px}
.cmp-card .ci{aspect-ratio:1/1;background:var(--surface);border-radius:var(--radius);display:grid;place-items:center;padding:8px}
.cmp-card .ci img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.cmp-card a.nm{font-weight:700;line-height:1.3}
.cmp-card a.nm:hover{color:var(--brand-red);text-decoration:underline}
.cmp-card .pr{color:var(--brand-red);font-weight:800}
.cmp-card .rm{justify-self:start;border:0;background:none;color:var(--muted);text-decoration:underline;font-size:13px;min-height:32px;padding:0}
@media (max-width:600px){.cmp-table{min-width:0;font-size:13px}.cmp-table tbody th{width:96px;min-width:96px;padding:8px 10px}.cmp-table td{min-width:150px;padding:8px 10px}.cmp-table thead th{padding:8px 10px}}
.cmp-empty{margin:24px 0 56px;padding:40px 24px;border:1px dashed var(--line);border-radius:var(--radius);text-align:center}
.cmp-empty p{color:var(--muted);margin:8px auto 20px;max-width:52ch}
.cmp-empty .links{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
'''

PAGE_JS = '''// Compare page: render the table from embedded data
(() => {
  const DATA = %s;
  const E=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const U=id=>id==='index.html'?'/trangchu':'/'+id.replace(/\.html$/,'');
  const C=window.spinlabCompare;
  const q=new URLSearchParams(location.search).get('ids');
  if(q){ const l=q.split(',').map(id=>/\.html$/.test(id)?id:id+'.html').filter(id=>DATA[id]).slice(0,%d).map(id=>({id,name:DATA[id].name,img:DATA[id].img,price:DATA[id].price})); C.save(l); }
  const root=document.getElementById('cmp-root'), diff=document.getElementById('cmp-diff');
  const draw=()=>{
    const items=C.load().map(x=>DATA[x.id]).filter(Boolean);
    if(items.length<2){ root.innerHTML='<div class="cmp-empty"><h2>'+(items.length?'Thêm ít nhất một sản phẩm nữa để so sánh':'Chưa có sản phẩm nào để so sánh')+'</h2><p>Bấm nút “So sánh” trên thẻ sản phẩm ở các trang danh mục, hoặc “Thêm vào so sánh” trong trang sản phẩm. Có thể so sánh tối đa %d sản phẩm.</p><div class="links"><a class="btn btn-outline" href="xe-road.html">Xe Road</a><a class="btn btn-outline" href="xe-mtb.html">Xe MTB</a><a class="btn btn-outline" href="xe-gravel.html">Xe Gravel</a><a class="btn btn-outline" href="lop-xe.html">Lốp xe</a><a class="btn btn-outline" href="day-cuon-tay-lai.html">Dây cuốn</a></div></div>'; diff.closest('label').hidden=true; return; }
    diff.closest('label').hidden=false;
    const groups=[]; const rows={};
    items.forEach(p=>p.specs.forEach(([g,k])=>{ if(!rows[g]){ rows[g]=[]; groups.push(g); } if(!rows[g].includes(k)) rows[g].push(k); }));
    const val=(p,g,k)=>{ const r=p.specs.find(s=>s[0]===g&&s[1]===k); return r?r[2]:'—'; };
    let h='<div class="cmp-wrap"><table class="cmp-table"><thead><tr><th scope="col"><span class="sr-only">Thông số</span></th>'+
      items.map(p=>`<th scope="col"><div class="cmp-card"><a class="ci" href="${E(U(p.id))}"><img src="${E(p.img)}" alt="${E(p.name)}"></a><a class="nm" href="${E(U(p.id))}">${E(p.name)}</a><span class="pr">${E(p.price)}</span><button type="button" class="rm" data-rm="${E(p.id)}">Bỏ khỏi so sánh</button></div></th>`).join('')+'</tr></thead><tbody>';
    groups.forEach(g=>{ h+=`<tr class="grp"><th scope="rowgroup">${E(g)}</th>${items.map(()=>'<td></td>').join('')}</tr>`;
      rows[g].forEach(k=>{ const vs=items.map(p=>val(p,g,k)); const same=vs.every(v=>v===vs[0]);
        h+=`<tr class="${same?'same':''}"><th scope="row">${E(k)}</th>${vs.map(v=>`<td>${E(v)}</td>`).join('')}</tr>`; }); });
    root.innerHTML=h+'</tbody></table></div>';
    root.querySelectorAll('[data-rm]').forEach(b=>b.addEventListener('click',()=>{ C.save(C.load().filter(x=>x.id!==b.dataset.rm)); draw(); }));
    apply();
  };
  const apply=()=>root.querySelectorAll('tr.same').forEach(tr=>tr.classList.toggle('hide',diff.checked));
  diff.addEventListener('change',apply);
  draw();
})();
'''


def inject(s, is_product, fname):
    if '/* Compare */' not in s:
        s = s.replace('</style>', CSS + '</style>', 1)
    else:
        s = re.sub(r'/\* Compare \*/.*?(?=</style>|/\* [A-Z])', lambda m: CSS, s, 1, flags=re.S)
    s = re.sub(r'// Compare products:.*?\}\)\(\);\n', '', s, flags=re.S)
    i = s.rindex('</script>\n</body>')
    s = s[:i] + JS + s[i:]
    s = re.sub(r'\s*<meta name="product-id"[^>]*>', '', s)
    if is_product:
        s = s.replace('<meta name="viewport"', f'<meta name="product-id" content="{fname}">\n<meta name="viewport"', 1)
    return s


# compare page (shell: xe-road.html)
shell = R('xe-road.html')
main = '''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li aria-current="page">So sánh sản phẩm</li></ol></nav>
    <div class="cmp-head"><h1>So sánh sản phẩm</h1><label class="cmp-diff"><input type="checkbox" id="cmp-diff"> Chỉ hiện điểm khác nhau</label></div>
    <div id="cmp-root"></div>
  </div>
</main>'''
p = re.sub(r'<title>.*?</title>', '<title>So sánh sản phẩm — Spinlab</title>', shell, 1, flags=re.S)
p = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="So sánh thông số các mẫu xe đạp, lốp và phụ kiện tại Spinlab.">', p, 1)
p = re.sub(r'<main id="main".*?</main>', lambda m: main, p, 1, flags=re.S)
p = re.sub(r'\s*<meta name="page"[^>]*>', '', p)
p = p.replace('<meta name="viewport"', '<meta name="page" content="compare">\n<meta name="viewport"', 1)
p = re.sub(r'/\* Compare page \*/.*?(?=</style>)', '', p, flags=re.S).replace('</style>', PAGE_CSS + '</style>', 1)
p = re.sub(r'// Compare page: render.*?\}\)\(\);\n', '', p, flags=re.S)
W('so-sanh.html', p)

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    b = os.path.basename(f)
    if b == 'v1-premium.html':
        continue
    s = R(b)
    if '</script>\n</body>' not in s:
        continue
    s = inject(s, b in DATA, b)
    if b == 'index.html' and 'name="page" content="home"' not in s:
        s = s.replace('<meta name="viewport"', '<meta name="page" content="home">\n<meta name="viewport"', 1)
    if b == 'so-sanh.html':
        i = s.rindex('</script>\n</body>')
        s = s[:i] + PAGE_JS % (json.dumps(DATA, ensure_ascii=False), MAX, MAX) + s[i:]
    W(b, s)
    n += 1
print(f'{len(DATA)} sản phẩm có dữ liệu so sánh; đã cập nhật {n} trang')
thin = [k for k, v in DATA.items() if len(v['specs']) < 5]
if thin:
    print('Ít thông số:', ', '.join(thin))
