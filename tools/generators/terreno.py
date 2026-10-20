"""Generate Vittoria Terreno T10–T90 gravel tire pages (terreno-tXX.html) from Vittoria product JSON.
Usage: terreno.py <site_dir> <json_dir>"""
import sys, os, re, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vcommon
D, J = sys.argv[1], sys.argv[2]
E = html.escape
shell = open(os.path.join(D, 'corsa-pro.html'), encoding='utf-8').read()
ZALO = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg'

PRO = 'Phiên bản thi đấu cao cấp nhất. Dòng Terreno PRO được làm từ 92% vật liệu tái tạo và tái chế — lốp bền vững nhất Vittoria từng sản xuất.'
PRO_STATS = ' Theo Vittoria, so với mức trung bình của đối thủ: nhanh hơn 7%, bám hơn 9% và chống thủng tốt hơn 34%.'
END = 'Phiên bản bền bỉ cho tập luyện và đạp đường dài, nhiều kích thước và hai màu thành lốp.'
END_G = ' Hợp chất Endurance Formulation tăng cường Graphene.'
SPORT = 'Phiên bản phổ thông với hợp chất và thân lốp Sport — cân bằng hiệu năng, độ bền và giá trị cho người đạp giải trí.'

# (handle, version label, blurb)
LINES = [
 dict(t=10, en='Hardpack', vi='Đường cứng, đất nén', aka='Tên cũ: Terreno Zero', headline='Lốp gravel lăn nhanh nhất',
      intro='T10 dành cho người đạp phần lớn trên đường nhựa hoặc gravel đất nén nhưng vẫn muốn tự tin khi rẽ vào những đoạn đường xấu. Gai lốp tối ưu cho mặt đường cứng giúp xe lăn nhẹ nhàng mà vẫn đủ bám cho gravel thực tế — lý tưởng cho các giải đạp có nhiều đoạn hỗn hợp và những chuyến endurance tốc độ cao.',
      terrain=['Đường nhựa', 'Đất nén', 'Gravel cứng'],
      versions=[('terreno-pro-t10-hardpack-gravel-race', 'PRO Race', PRO + ' Dải giữa trơn lấy cảm hứng từ lốp Corsa, vai lốp hình vảy cá từ T30 cho độ bám khi vào cua và trên mặt ướt.' + PRO_STATS),
                ('terreno-t10-hardpack-gravel-endurance', 'Endurance', END + ' Mẫu lăn hiệu quả nhất trên đường trong dòng Gravel Endurance.'),
                ('terreno-t10-hardpack-gravel-sport', 'Sport', SPORT)]),
 dict(t=30, en='Fine Loose', vi='Sỏi mịn, đất tơi', aka='Tên cũ: Terreno Dry', headline='Chuyên gia sỏi mịn',
      intro='T30 dành cho người ưu tiên tốc độ trên sỏi mịn nhưng vẫn cần độ bám và sự linh hoạt khi địa hình trở nên kỹ thuật. Dải giữa hình vảy cá giảm lực cản lăn mà vẫn giữ độ bám khi phanh và vào cua; núm vai có rãnh bám chắc ở những đoạn nghiêng, chuyển tiếp mượt mà khi ôm cua.',
      terrain=['Sỏi mịn', 'Đất tơi', 'Đường khô, nhanh'],
      versions=[('terreno-pro-t30-fine-loose-gravel-race', 'PRO Race', PRO + PRO_STATS),
                ('terreno-t30-gravel-endurance', 'Endurance', END + END_G),
                ('terreno-t30-fine-loose-gravel-sport', 'Sport', SPORT)]),
 dict(t=50, en='Mixed', vi='Địa hình hỗn hợp', aka='Nằm giữa T30 và T70', headline='Một bộ lốp cho mọi cung đường',
      intro='T50 cân bằng hoàn hảo giữa hiệu quả trên đường nhựa và khả năng off-road. Gai lốp với rãnh định hướng kết hợp núm vai vào cua chắc chắn và dải giữa hiệu quả — tự tin trên đường nhựa, đất nén lẫn sỏi hỗn hợp.',
      terrain=['Đường nhựa', 'Đất nén', 'Sỏi hỗn hợp'],
      versions=[('terreno-pro-t50-mixed-gravel-race', 'PRO Race', PRO),
                ('terreno-t50-tubeless-ready', 'Endurance', END + END_G),
                ('terreno-t50-mixed-gravel-sport-rigid', 'Sport (tanh cứng)', SPORT)]),
 dict(t=60, en='Mixed', vi='Hỗn hợp, gồ ghề', aka='', headline='Cho địa hình hỗn hợp khắc nghiệt',
      intro='T60 dành cho người chinh phục địa hình hỗn hợp gồ ghề và khó đoán. Gai xếp hình chữ V cùng biên dạng đều giúp vào cua tự tin, xử lý ổn định trên mọi bề mặt — từ đất nén, sỏi to đến lớp sỏi rời trên nền cứng.',
      terrain=['Hỗn hợp gồ ghề', 'Sỏi to', 'Sỏi rời trên nền cứng'],
      versions=[('terreno-pro-t60-tubeless-ready', 'PRO Race', PRO),
                ('terreno-t60-gravel-endurance', 'Endurance', END + END_G)]),
 dict(t=70, en='Coarse Loose', vi='Sỏi to, đất rời', aka='Gai lốp từ Mezcal XC', headline='Công nghệ MTB vô địch thế giới cho gravel',
      intro='T70 mang thiết kế gai của lốp Mezcal XC — công nghệ MTB từng giành chức vô địch thế giới — vào xe gravel. Dành cho người mê những cung đường sỏi to, rời và khó đoán, T70 có tốc độ và độ bám chuẩn đua XC, nay được tối ưu cho gravel.',
      terrain=['Sỏi to', 'Đất rời', 'Đường khó đoán'],
      versions=[('terreno-t70-gravel-endurance', 'Endurance', END + END_G)]),
]
COLOR_VI = vcommon.COLOR_VI


PRODUCTS = []
for _L in LINES:
    for _h, _lab, _blurb in _L['versions']:
        if _lab.startswith('Sport'):
            continue
        _pro = _lab.startswith('PRO')
        PRODUCTS.append(dict(_L, fam='pro' if _pro else 'end', versions=[(_h, 'PRO Race' if _pro else 'Endurance', _blurb)],
            file=(f'terreno-pro-t{_L["t"]}.html' if _pro else f'terreno-t{_L["t"]}.html'),
            name=(f'Terreno PRO T{_L["t"]} {_L["en"]}' if _pro else f'Terreno T{_L["t"]} {_L["en"]} Endurance'),
            short=(f'Terreno PRO T{_L["t"]}' if _pro else f'Terreno T{_L["t"]} Endurance')))


def load(h):
    p = json.load(open(os.path.join(J, h + '.json'), encoding='utf-8'))['product']
    imgs = [i['src'].split('?')[0] for i in p['images']]
    imgs = [u for u in imgs if not re.search(r'-08(_[0-9a-f-]+)?\.(webp|jpg)$', u)][:6]   # drop carbon-neutral graphics
    variants = vcommon.in_stock(h, [dict(size=v['option1'], color=v['option2'], sku=v['sku']) for v in p['variants']])
    return dict(title=p['title'], url=f'https://vittoria.com/products/{h}', images=imgs, variants=variants)


ALL_PRODUCTS = list(PRODUCTS)
PRODUCTS[:] = [P for P in PRODUCTS if load(P['versions'][0][0])['variants']]   # only lines with in-stock sizes


def meter(P):
    fam = [q for q in PRODUCTS if q['fam'] == P['fam']]
    lo, hi = fam[0]['t'], fam[-1]['t']
    ticks = ''
    for q in fam:
        pos = (q['t'] - lo) / (hi - lo) * 100
        on = ' aria-current="page"' if q['t'] == P['t'] else ''
        ticks += f'<a href="{q["file"]}" style="left:{pos:.1f}%"{on} title="{E(q["short"])} — {E(q["vi"])}"><span>T{q["t"]}</span></a>'
    return f'''<div class="tscore" aria-label="Thang T-score của Vittoria">
      <div class="ts-track">{ticks}</div>
      <div class="ts-ends"><span>Nhanh · đường cứng</span><span>Bám · sỏi to, rời</span></div></div>'''


def card(P, prefix=''):
    v0 = load(P['versions'][0][0])
    tag = '<span class="tag">PRO</span>' if P['fam'] == 'pro' else f'<span class="tag dark">T{P["t"]}</span>'
    chip = 'PRO Race · Thi đấu' if P['fam'] == 'pro' else 'Endurance · Tập luyện, đường dài'
    return (f'<article class="p-card" data-type="gravel"><div class="p-img tire">{tag}'
            f'<img src="{v0["images"][0]}?width=600" alt="Lốp Vittoria {E(P["name"])}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">Vittoria · Gravel</span>'
            f'<h3 class="p-name"><a class="stretch" href="{prefix}{P["file"]}">{E(P["name"])}</a></h3>'
            f'<p class="p-desc">{E(P["vi"])}</p><ul class="models"><li>{chip}</li></ul><span class="p-price">1.980.000₫</span></div>'
            f'</article>')


CSS = '''
/* Terreno pages */
.opt-group{border:0;margin:8px 0 0;padding:0}
.opt-group legend{padding:0;margin-bottom:10px;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.04em;display:flex;gap:10px;flex-wrap:wrap;align-items:baseline}
.siblings{margin:16px 0 0;font-size:14px;color:var(--muted)}
.siblings b{color:var(--text)}
.geo-note{font-size:13px;color:var(--muted);margin:10px 0 0}
.tscore{margin:4px 0 6px}
.ts-track{position:relative;height:40px;margin:0 14px;border-radius:999px;background:linear-gradient(90deg,#C9C3B6,#8B6B47 55%,#4B3621)}
.ts-track a{position:absolute;top:50%;transform:translate(-50%,-50%);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#fff;color:var(--text);font-size:11px;font-weight:800;box-shadow:0 1px 3px rgba(0,0,0,.25);transition:transform .15s}
.ts-track a:hover{transform:translate(-50%,-50%) scale(1.08)}
.ts-track a[aria-current]{background:var(--brand-red);color:#fff;width:40px;height:40px;box-shadow:0 0 0 3px var(--brand-yellow)}
.ts-ends{display:flex;justify-content:space-between;margin-top:8px;font-size:12px;color:var(--muted)}
.ver-desc{margin:8px 0 0;font-size:14px;color:var(--muted);line-height:1.55}
.aka{font-size:13px;color:var(--muted)}
.vtable td,.vtable th{vertical-align:top}
.vtable td:last-child{min-width:240px}
.sku-table td:nth-child(3){font-variant-numeric:tabular-nums}
.sku-table tr.on{background:#FFF7D6}
'''

FAQ = [('Nên chọn T-score nào?', 'T-score càng thấp, lốp càng lăn nhanh trên mặt đường cứng; càng cao, lốp càng bám trên sỏi to và rời. Nếu bạn đạp nhiều đường nhựa và đất nén, hãy chọn T10–T30; đường hỗn hợp chọn T50–T60; sỏi to, rời chọn T70.'),
       ('Terreno PRO và Terreno Endurance khác nhau thế nào?', 'Terreno PRO là dòng thi đấu cao cấp nhất, làm từ 92% vật liệu tái tạo và tái chế, có các mẫu T10–T60. Terreno Endurance bền bỉ cho tập luyện và đạp đường dài, có nhiều kích thước hơn, hai màu thành lốp và các mẫu T10–T70.'),
       ('Có lắp không săm (tubeless) được không?', 'Liên hệ Spinlab để được xác nhận khả năng lắp tubeless của từng phiên bản và kích thước, cũng như tư vấn vành, van và dung dịch sealant phù hợp.')]


def page(P):
    L = P
    vers = [(h, label, blurb, load(h)) for h, label, blurb in L['versions']]
    name = P['name']
    imgs0 = vers[0][3]['images']
    thumbs = ''.join(f'<li><button aria-pressed="{"true" if k == 0 else "false"}" data-src="{u}?width=1000" data-alt="{E(name)} – ảnh {k+1}"><img src="{u}?width=160" alt="Ảnh {k+1}"></button></li>' for k, u in enumerate(imgs0))
    vopts = ''.join(f'<label><input type="radio" name="ver" value="{k}"{" checked" if k == 0 else ""}><span>{E(lab)}</span></label>' for k, (h, lab, b, d) in enumerate(vers))
    vfield = (f'<fieldset class="opt-group"><legend>Phiên bản</legend><div class="size-opts">{vopts}</div><p class="ver-desc" id="ver-desc">{E(vers[0][2])}</p></fieldset>'
              if len(vers) > 1 else f'<p class="ver-desc"><b>{E(vers[0][1])}</b> — {E(vers[0][2])}</p>')
    # version comparison table
    vrows = ''
    for h, lab, b, d in vers:
        sizes = list(dict.fromkeys(v['size'] for v in d['variants']))
        colors = list(dict.fromkeys(COLOR_VI.get(v['color'], v['color']) for v in d['variants']))
        vrows += f'<tr><th scope="row">{E(lab)}</th><td>{E(", ".join(sizes))}</td><td>{E(", ".join(colors))}</td><td>{E(b)}</td></tr>'
    # full SKU table
    srows = ''
    for k, (h, lab, b, d) in enumerate(vers):
        for v in d['variants']:
            srows += f'<tr data-ver="{k}" data-sku="{v["sku"]}"><td>{E(v["size"])}</td><td>{E(COLOR_VI.get(v["color"], v["color"]))}</td><td>{v["sku"]}</td></tr>'
    related = ''.join(card(o) for o in PRODUCTS if o['fam'] == P['fam'] and o['t'] != P['t'])
    twin = [o for o in PRODUCTS if o['t'] == P['t'] and o['fam'] != P['fam']]
    twin_html = ('<section class="pdp-sec" id="phien-ban"><h2>Phiên bản khác của T' + str(P['t']) + '</h2><div class="grid related" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">' + ''.join(card(o) for o in twin) + '</div></section>') if twin else ''
    fam_label = 'Terreno PRO' if P['fam'] == 'pro' else 'Terreno Endurance'
    terrain = ''.join(f'<li>{E(x)}</li>' for x in L['terrain'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    aka = f' <span class="aka">· {E(L["aka"])}</span>' if L['aka'] else ''

    main = f'''<main id="main" class="pdp">
  <div class="container">
    <nav class="crumbs" aria-label="Đường dẫn"><ol>
      <li><a href="index.html">Trang chủ</a></li><li><a href="index.html#hot">Phụ tùng</a></li><li><a href="lop-xe.html">Lốp xe</a></li>
      <li><a class="crumb" href="lop-xe.html#gravel">Gravel</a></li><li aria-current="page">{E(P["short"])}</li></ol></nav>
    <div class="pdp-top">
      <div class="gallery">
        <div class="g-main"><img id="g-main" src="{imgs0[0]}?width=1000" alt="Lốp Vittoria {E(name)}" width="1000" height="1000"></div>
        <ul class="g-thumbs" aria-label="Ảnh sản phẩm">{thumbs}</ul>
      </div>
      <div class="buy">
        <span class="p-brand">Vittoria · Lốp Gravel</span>
        <h1>{E(name)}</h1>
        <p class="tagline">{E(L["headline"])} — {E(L["vi"].lower())}.{aka}</p>
        {meter(P)}
        {vfield}
        <fieldset class="opt-group" id="color-field"><legend>Màu <span class="size-meta" id="color-name"></span></legend><div class="size-opts" id="color-opts"></div></fieldset>
        <fieldset class="sizes"><legend>Kích thước <span class="size-meta" aria-live="polite">Mã <span id="sz-sku">—</span></span></legend><div class="size-opts" id="size-opts"></div></fieldset>
        <div class="price-row"><span class="label">Giá bán lẻ</span><span class="p-price big">1.980.000₫</span></div>
        <div class="buy-ctas">
          <a class="btn btn-zalo outline" href="https://zalo.me/0399337533" target="_blank" rel="noopener"><img src="{ZALO}" alt="" width="22" height="22">Chat Zalo</a>
          <a class="btn btn-outline" href="tel:0399337533">Gọi 0399 337 533</a>
        </div>
        <ul class="assure">
          <li><svg aria-hidden="true"><use href="#i-shield"/></svg>Hàng chính hãng Vittoria, phân phối bởi Spinlab</li>
          <li><svg aria-hidden="true"><use href="#i-truck"/></svg>Giao hàng toàn quốc</li>
          <li><svg aria-hidden="true"><use href="#i-chat"/></svg>Tư vấn chọn lốp miễn phí qua hotline</li>
        </ul>
      </div>
    </div>

    <nav class="pdp-nav" aria-label="Nội dung sản phẩm"><a href="#gioi-thieu">Giới thiệu</a>{'<a href="#phien-ban">Phiên bản khác</a>' if twin else ''}<a href="#cong-nghe">Công nghệ</a><a href="#ma-san-pham">Bảng kỹ thuật</a><a href="#hoi-dap">Hỏi đáp</a></nav>

    <section class="pdp-sec intro" id="gioi-thieu">
      <div><h2>{E(L["headline"])}</h2><p>{E(L["intro"])}</p>
        <p class="siblings"><b>Địa hình phù hợp:</b></p><ul class="fit">{terrain}</ul></div>
      <figure><img src="{(imgs0[3] if len(imgs0) > 3 else imgs0[-1])}?width=900" alt="Lốp Terreno T{L["t"]} khi sử dụng" loading="lazy"></figure>
    </section>

    {twin_html}

    {vcommon.tech_section([(h, lab) for h, lab, b, d in vers])}

    {vcommon.spec_section([(h, lab) for h, lab, b, d in vers], lambda hh: load(hh)["variants"])}

    <section class="pdp-sec" id="hoi-dap"><h2>Hỏi đáp</h2><div class="faq">{faq}</div></section>

    <section class="pdp-sec"><div class="sec-head"><h2>Các mẫu {fam_label} khác</h2><a class="see-all" href="lop-xe.html#gravel">Xem tất cả lốp gravel</a></div>
      <div class="grid related" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">{related}</div></section>
  </div>
</main>'''

    data = [dict(label=lab, blurb=b, images=d['images'], variants=d['variants']) for h, lab, b, d in vers]
    js = '''// Terreno page: version -> colour -> size selector, gallery
(() => {
  const V = %s, CV = %s;
  const $ = id => document.getElementById(id), main = $('g-main'), list = document.querySelector('.g-thumbs');
  let ver = 0, color = null, size = null;
  const radios = (box, name, items, cur) => { box.innerHTML = items.map(x => `<label><input type="radio" name="${name}" value="${x}"${x===cur?' checked':''}><span>${CV[x]||x}</span></label>`).join(''); };
  const bindThumbs = () => { const t=[...list.querySelectorAll('button')]; t.forEach(b=>b.onclick=()=>{ main.src=b.dataset.src; main.alt=b.dataset.alt; t.forEach(x=>x.setAttribute('aria-pressed',x===b)); }); };
  const render = () => {
    const v = V[ver], colors = [...new Set(v.variants.map(x=>x.color))];
    if (!colors.includes(color)) color = colors[0];
    const sizes = v.variants.filter(x=>x.color===color).map(x=>x.size);
    if (!sizes.includes(size)) size = sizes[0];
    radios($('color-opts'), 'color', colors, color); $('color-name').textContent = CV[color]||color;
    radios($('size-opts'), 'size', sizes, size);
    const m = v.variants.find(x=>x.color===color && x.size===size); const sku = (m && m.sku) ? m.sku : '—';
    $('sz-sku').textContent = sku;
    document.querySelectorAll('.sku-table tbody tr').forEach(tr=>tr.classList.toggle('on', tr.dataset.key ? tr.dataset.key===size+'|'+color && (!tr.closest('[data-ver]') ) && (tr.dataset.ver===undefined || +tr.dataset.ver===ver) && (V.length===1 || tr.cells[0].textContent===V[ver].label) : tr.dataset.sku===sku));
    document.querySelectorAll('#color-opts input').forEach(r=>r.onchange=()=>{ color=r.value; render(); });
    document.querySelectorAll('#size-opts input').forEach(r=>r.onchange=()=>{ size=r.value; render(); });
  };
  const setVer = k => { ver = +k; const v = V[ver]; if ($('ver-desc')) $('ver-desc').textContent = v.blurb;
    main.src = v.images[0] + '?width=1000';
    list.innerHTML = v.images.map((u,i)=>`<li><button aria-pressed="${i===0}" data-src="${u}?width=1000" data-alt="${v.label} – ảnh ${i+1}"><img src="${u}?width=160" alt="Ảnh ${i+1}"></button></li>`).join('');
    bindThumbs(); render(); };
  document.querySelectorAll('input[name=ver]').forEach(r=>r.addEventListener('change',()=>setVer(r.value)));
  bindThumbs(); render();
})();
''' % (json.dumps(data, ensure_ascii=False), json.dumps(COLOR_VI, ensure_ascii=False))

    p = shell
    p = re.sub(r'<title>.*?</title>', f'<title>Vittoria {E(name)} — Lốp gravel — Spinlab</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="Lốp gravel Vittoria {E(name)}: {E(L["headline"])}. Phân phối chính hãng bởi Spinlab.">', p, 1)
    p = p.replace('</style>', CSS + vcommon.CSS + '</style>', 1)
    p = re.sub(r'<main id="main" class="pdp">.*?</main>', lambda m: main, p, 1, flags=re.S)
    p = re.sub(r'// Product gallery \+ size selector.*?\}\)\(\);\n', lambda m: js, p, 1, flags=re.S)
    out = P['file']
    open(os.path.join(D, out), 'w', encoding='utf-8').write(p)
    return out


if __name__ == '__main__':
    for P in PRODUCTS:
        print(page(P))
    for P in ALL_PRODUCTS:
        if P not in PRODUCTS:
            print('-- hết hàng, không tạo trang:', P['file'])
    # cards HTML for listing pages
    open(os.path.join(J, '..', 'terreno-cards.html'), 'w', encoding='utf-8').write('\n'.join(card(P) for P in sorted(PRODUCTS, key=lambda q: (q['fam'] != 'pro', q['t']))))
