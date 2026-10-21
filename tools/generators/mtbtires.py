"""Generate Vittoria MTB tire pages (one page per tread line, casing versions selectable).
Usage: mtbtires.py <site_dir> <json_dir>"""
import sys, os, re, json, html
D, J = sys.argv[1], sys.argv[2]
E = html.escape
shell = open(os.path.join(D, 'corsa-pro.html'), encoding='utf-8').read()
ZALO = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg'
PRICE = '1.980.000₫'
COLOR_VI = {'Brown': 'Thành nâu', 'Black': 'Đen'}
C4 = ' Hợp chất 4Compound với bốn loại cao su được đặt đúng vị trí cần thiết — kết hợp tốc độ, độ bám và độ bền.'

LINES = [
 dict(file='vittoria-terreno-xc.html', name='Terreno XC', cat='Cross Country', headline='Tên lửa trên đường cứng',
      intro='Terreno XC được thiết kế cho tốc độ tối đa trên đường mòn khô và cứng. Dải gai giữa hình vảy cá lăn cực nhanh trên đường thẳng mà vẫn giữ lực phanh và bám cua khi cần; chuyển tiếp đều từ dải giữa ra núm vai giúp mỗi khúc cua mượt mà, dễ đoán.',
      terrain=['Đường mòn cứng', 'Khô, nhanh', 'Đua XC'],
      versions=[('terreno-xc-race', 'XC Race', 'Phiên bản thi đấu cho tay đua cross country — mọi chi tiết hướng tới tốc độ và độ chính xác.'),
                ('terreno-xc-trail', 'XC Trail', 'Thân lốp Trail Case bền chắc hơn cho đường mòn cứng.' + C4)]),
 dict(file='vittoria-peyote.html', name='Peyote', cat='Cross Country', headline='Tốc độ World Cup trên nhiều địa hình',
      intro='Peyote nằm giữa Terreno và Mezcal, với dải gai giữa thấp xen kẽ giúp tăng tốc độ và độ bám. Gai xếp hình chữ V đặc trưng của Vittoria bám sâu vào đất tơi và đẩy sỏi đá sang hai bên; gai giữa thon dần ra núm vai cho cảm giác vào cua nhạy và dễ đoán.',
      terrain=['Đất tơi, sỏi mịn', 'Hỗn hợp', 'XC / Down Country'],
      versions=[('peyote-xc-race', 'XC Race', 'Phiên bản thi đấu với tốc độ đẳng cấp World Cup.'),
                ('peyote-xc-trail', 'XC Trail', 'Thân lốp Trail Case cho người vừa thích phiêu lưu vừa muốn lên podium.' + C4)]),
 dict(file='vittoria-mazza.html', name='Mazza', cat='Trail / Enduro', headline='Làm chủ đường mòn kỹ thuật',
      intro='Mazza dành cho người cần vào cua tự tin và bám đường chắc chắn trên địa hình đa dạng, nhiều kỹ thuật. Rãnh cắt lũy tiến trên núm vai cân bằng giữa cảm giác đường và độ bám khi ôm cua hay bám vách đá nghiêng; mép gai dốc giúp leo dốc tốt trên những đoạn gồ ghề.',
      terrain=['Trail kỹ thuật', 'Enduro', 'Đá, rễ cây'],
      versions=[('mazza-trail', 'Trail', 'Thân lốp Trail Case; gai thưa tự làm sạch đất và bùn.' + C4),
                ('mazza-enduro', 'Enduro', 'Bản enduro đa năng cho shuttle, gravity và những ngày đạp trên địa hình kỹ thuật — ứng dụng công nghệ đã được chứng minh ở EWS.'),
                ('mazza-enduro-race', 'Enduro Race', 'Hợp chất thi đấu tối đa độ bám, giảm rung và đàn hồi mượt — thiết kế theo yêu cầu của tay đua EWS.')]),
 dict(file='vittoria-martello.html', name='Martello', cat='Trail / Enduro', headline='Huyền thoại enduro, bám chắc mọi điều kiện',
      intro='Martello đã được chứng minh ở enduro và downhill đỉnh cao. Núm gai lấy cảm hứng từ lốp mô tô bền bỉ, hoạt động tốt trên địa hình kỹ thuật cả khô lẫn ướt; rãnh cắt lũy tiến thay đổi độ dày mép gai để cân bằng cảm giác đường và độ bám mà không mất ổn định.',
      terrain=['Cứng đến hỗn hợp', 'Enduro / DH', 'Khô và ướt'],
      versions=[('martello-trail', 'Trail', 'Lốp trail linh hoạt nhất cho đường cứng đến hỗn hợp; gai thưa tự làm sạch đất và bùn.' + C4),
                ('martello-enduro', 'Enduro', 'Cho mọi thứ từ thi đấu gravity đến khám phá — bám chắc trên mọi chướng ngại.'),
                ('martello-enduro-race', 'Enduro Race', 'Cấu trúc tinh chỉnh cho thi đấu — bám chắc, giảm rung, đàn hồi mượt trên những đoạn kỹ thuật và dốc nghiêng.')]),
]


def load(h):
    p = json.load(open(os.path.join(J, h + '.json'), encoding='utf-8'))['product']
    imgs = [i['src'].split('?')[0] for i in p['images']][:6]
    return dict(images=imgs, variants=[dict(size=v['option1'], color=v['option2'], sku=v['sku']) for v in p['variants']])


def card(L):
    v0 = load(L['versions'][0][0])
    vers = ' · '.join(v[1] for v in L['versions'])
    return (f'<article class="p-card" data-type="mtb"><div class="p-img tire"><span class="tag dark">{E(L["cat"])}</span>'
            f'<img src="{v0["images"][0]}?width=600" alt="Lốp Vittoria {E(L["name"])}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">Vittoria · MTB</span>'
            f'<h3 class="p-name"><a class="stretch" href="{L["file"]}">{E(L["name"])}</a></h3>'
            f'<p class="p-desc">{E(L["headline"])}</p><ul class="models"><li>{E(vers)}</li></ul><span class="p-price">{PRICE}</span></div></article>')


CSS = '''
/* MTB tire pages */
.opt-group{border:0;margin:8px 0 0;padding:0}
.opt-group legend{padding:0;margin-bottom:10px;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.04em;display:flex;gap:10px;flex-wrap:wrap;align-items:baseline}
.siblings{margin:16px 0 0;font-size:14px;color:var(--muted)}
.siblings b{color:var(--text)}
.geo-note{font-size:13px;color:var(--muted);margin:10px 0 0}
.ver-desc{margin:8px 0 0;font-size:14px;color:var(--muted);line-height:1.55}
.vtable td,.vtable th{vertical-align:top}
.vtable td:last-child{min-width:240px}
.sku-table tr.on{background:#FFF7D6}
'''

FAQ = [('Nên chọn phiên bản nào?', 'Bản Race tối ưu tốc độ và trọng lượng cho thi đấu. Bản Trail có thân lốp Trail Case bền chắc hơn cho đạp đường mòn hằng ngày. Bản Enduro chắc chắn hơn nữa cho địa hình gravity, đổ dốc kỹ thuật.'),
       ('Chọn kích thước lốp thế nào?', 'Chọn theo cỡ bánh (27.5" hoặc 29") và bề rộng phù hợp với vành, khoảng hở khung/phuộc của xe. Liên hệ Spinlab để được tư vấn theo xe bạn đang dùng.'),
       ('Có lắp không săm (tubeless) được không?', 'Liên hệ Spinlab để được xác nhận khả năng lắp tubeless của từng phiên bản, cũng như tư vấn vành, van và dung dịch sealant phù hợp.')]


def page(L):
    vers = [(h, lab, b, load(h)) for h, lab, b in L['versions']]
    name = L['name']
    imgs0 = vers[0][3]['images']
    thumbs = ''.join(f'<li><button aria-pressed="{"true" if k == 0 else "false"}" data-src="{u}?width=1000" data-alt="{E(name)} – ảnh {k+1}"><img src="{u}?width=160" alt="Ảnh {k+1}"></button></li>' for k, u in enumerate(imgs0))
    vopts = ''.join(f'<label><input type="radio" name="ver" value="{k}"{" checked" if k == 0 else ""}><span>{E(lab)}</span></label>' for k, (h, lab, b, d) in enumerate(vers))
    vrows = ''.join(f'<tr><th scope="row">{E(lab)}</th><td>{E(", ".join(dict.fromkeys(v["size"] for v in d["variants"])))}</td>'
                    f'<td>{E(", ".join(dict.fromkeys(COLOR_VI.get(v["color"], v["color"]) for v in d["variants"])))}</td><td>{E(b)}</td></tr>' for h, lab, b, d in vers)
    srows = ''.join(f'<tr data-sku="{v["sku"]}"><td>{E(lab)}</td><td>{E(v["size"])}</td><td>{E(COLOR_VI.get(v["color"], v["color"]))}</td><td>{v["sku"]}</td></tr>'
                    for h, lab, b, d in vers for v in d['variants'])
    related = ''.join(card(o) for o in LINES if o is not L)
    terrain = ''.join(f'<li>{E(x)}</li>' for x in L['terrain'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    fig = imgs0[2] if len(imgs0) > 2 else imgs0[-1]

    main = f'''<main id="main" class="pdp">
  <div class="container">
    <nav class="crumbs" aria-label="Đường dẫn"><ol>
      <li><a href="index.html">Trang chủ</a></li><li><a href="phu-tung.html">Phụ tùng</a></li><li><a href="lop-xe.html">Lốp xe</a></li>
      <li><a class="crumb" href="lop-xe.html#mtb">MTB</a></li><li aria-current="page">{E(name)}</li></ol></nav>
    <div class="pdp-top">
      <div class="gallery">
        <div class="g-main"><img id="g-main" src="{imgs0[0]}?width=1000" alt="Lốp Vittoria {E(name)}" width="1000" height="1000"></div>
        <ul class="g-thumbs" aria-label="Ảnh sản phẩm">{thumbs}</ul>
      </div>
      <div class="buy">
        <span class="p-brand">Vittoria · Lốp MTB · {E(L["cat"])}</span>
        <h1>{E(name)}</h1>
        <p class="tagline">{E(L["headline"])}</p>
        <fieldset class="opt-group"><legend>Phiên bản</legend><div class="size-opts">{vopts}</div><p class="ver-desc" id="ver-desc">{E(vers[0][2])}</p></fieldset>
        <fieldset class="opt-group"><legend>Màu <span class="size-meta" id="color-name"></span></legend><div class="size-opts" id="color-opts"></div></fieldset>
        <fieldset class="sizes"><legend>Kích thước <span class="size-meta" aria-live="polite">Mã <span id="sz-sku">—</span></span></legend><div class="size-opts" id="size-opts"></div></fieldset>
        <div class="price-row"><span class="label">Giá bán lẻ</span><span class="p-price big">{PRICE}</span></div>
        <div class="buy-ctas">
          <a class="btn btn-zalo outline" href="https://zalo.me/0399337533" target="_blank" rel="noopener"><img src="{ZALO}" alt="" width="22" height="22">Chat Zalo</a>
          <a class="btn btn-yellow" href="tel:0399337533">Gọi 0399 337 533</a>
        </div>
        <ul class="assure">
          <li><svg aria-hidden="true"><use href="#i-shield"/></svg>Hàng chính hãng Vittoria, phân phối bởi Spinlab</li>
          <li><svg aria-hidden="true"><use href="#i-truck"/></svg>Giao hàng toàn quốc</li>
          <li><svg aria-hidden="true"><use href="#i-chat"/></svg>Tư vấn chọn lốp miễn phí qua hotline</li>
        </ul>
      </div>
    </div>

    <nav class="pdp-nav" aria-label="Nội dung sản phẩm"><a href="#gioi-thieu">Giới thiệu</a><a href="#phien-ban">Phiên bản</a><a href="#ma-san-pham">Kích thước &amp; mã</a><a href="#hoi-dap">Hỏi đáp</a></nav>

    <section class="pdp-sec intro" id="gioi-thieu">
      <div><h2>{E(L["headline"])}</h2><p>{E(L["intro"])}</p>
        <p class="siblings"><b>Địa hình phù hợp:</b></p><ul class="fit">{terrain}</ul></div>
      <figure><img src="{fig}?width=900" alt="Lốp Vittoria {E(name)}" loading="lazy"></figure>
    </section>

    <section class="pdp-sec" id="phien-ban"><h2>Các phiên bản</h2>
      <div class="table-wrap"><table class="vtable"><thead><tr><th scope="col">Phiên bản</th><th scope="col">Kích thước</th><th scope="col">Màu</th><th scope="col">Đặc điểm</th></tr></thead><tbody>{vrows}</tbody></table></div>
    </section>

    <section class="pdp-sec" id="ma-san-pham"><h2>Kích thước &amp; mã sản phẩm</h2>
      <div class="table-wrap"><table class="sku-table"><thead><tr><th scope="col">Phiên bản</th><th scope="col">Kích thước</th><th scope="col">Màu</th><th scope="col">Mã sản phẩm</th></tr></thead><tbody>{srows}</tbody></table></div>
      <p class="geo-note">Dòng đang chọn được tô màu. Dữ liệu theo Vittoria; vui lòng liên hệ Spinlab để kiểm tra hàng có sẵn.</p>
    </section>

    <section class="pdp-sec" id="hoi-dap"><h2>Hỏi đáp</h2><div class="faq">{faq}</div></section>

    <section class="pdp-sec"><div class="sec-head"><h2>Lốp MTB khác</h2><a class="see-all" href="lop-xe.html#mtb">Xem tất cả lốp MTB</a></div>
      <div class="grid related" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">{related}</div></section>
  </div>
</main>'''

    data = [dict(label=lab, blurb=b, images=d['images'], variants=d['variants']) for h, lab, b, d in vers]
    js = '''// MTB tire page: version -> colour -> size selector, gallery
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
    const m = v.variants.find(x=>x.color===color && x.size===size); const sku = m ? m.sku : '—';
    $('sz-sku').textContent = sku;
    document.querySelectorAll('.sku-table tbody tr').forEach(tr=>tr.classList.toggle('on', tr.dataset.sku===sku));
    document.querySelectorAll('#color-opts input').forEach(r=>r.onchange=()=>{ color=r.value; render(); });
    document.querySelectorAll('#size-opts input').forEach(r=>r.onchange=()=>{ size=r.value; render(); });
  };
  const setVer = k => { ver = +k; const v = V[ver]; $('ver-desc').textContent = v.blurb;
    main.src = v.images[0] + '?width=1000';
    list.innerHTML = v.images.map((u,i)=>`<li><button aria-pressed="${i===0}" data-src="${u}?width=1000" data-alt="${v.label} – ảnh ${i+1}"><img src="${u}?width=160" alt="Ảnh ${i+1}"></button></li>`).join('');
    bindThumbs(); render(); };
  document.querySelectorAll('input[name=ver]').forEach(r=>r.addEventListener('change',()=>setVer(r.value)));
  bindThumbs(); render();
})();
''' % (json.dumps(data, ensure_ascii=False), json.dumps(COLOR_VI, ensure_ascii=False))

    p = shell
    p = re.sub(r'<title>.*?</title>', f'<title>Vittoria {E(name)} — Lốp MTB — Spinlab</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="Lốp MTB Vittoria {E(name)}: {E(L["headline"])}. Phân phối chính hãng bởi Spinlab.">', p, 1)
    p = p.replace('</style>', CSS + '</style>', 1)
    p = re.sub(r'<main id="main" class="pdp">.*?</main>', lambda m: main, p, 1, flags=re.S)
    p = re.sub(r'// Product gallery \+ size selector.*?\}\)\(\);\n', lambda m: js, p, 1, flags=re.S)
    open(os.path.join(D, L['file']), 'w', encoding='utf-8').write(p)
    return L['file']


if __name__ == '__main__':
    for L in LINES:
        print(page(L))
    open(os.path.join(J, '..', 'mtb-cards.html'), 'w', encoding='utf-8').write('\n'.join(card(L) for L in LINES))
