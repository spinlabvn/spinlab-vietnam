"""Emume handlebar tape & accessories — product pages + listing page day-cuon-tay-lai.html.
Data: 'Spinlab order' spreadsheet (codes, size, thickness, weight, material) — wholesale prices and supplier are NOT published.
Colour names were read from the labels printed on the spreadsheet's product images.
Usage: python3 emume.py <design-preview dir> [<folder with extracted imageN.png>]
  With the image folder, images are cropped/converted into img/emume/; without it, existing images are reused."""
import sys, os, re, html, json, subprocess
E = html.escape
D = sys.argv[1]
SRC = sys.argv[2] if len(sys.argv) > 2 else None
OUT = os.path.join(D, 'img', 'emume')
IMG = 'img/emume/'
PRICE = '980.000₫'   # default demo price requested by Spinlab
# retail prices set by Spinlab (2026-10-20), by product group
GROUP_PRICE = {'basic': '550.000₫', 'bastet': '680.000₫', 'galaxy': '880.000₫'}
price = lambda L: GROUP_PRICE.get(L['group'], PRICE)
ZALO = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg'

# crop = fraction of height kept from the top (removes the printed Chinese colour label at the bottom)
LINES = [
 dict(file='emume-basic.html', group='basic', name='Basic', series='Basic', crop=(0.03, 0.80),
      headline='Dây cuốn đục lỗ, 24 phối màu', desc='24 phối màu · 3mm · 127g',
      intro='Dòng dây cuốn tay lái cơ bản của Emume: lớp silicone kết hợp EVA, bề mặt đục lỗ thoáng khí, dày 3mm cho cảm giác êm tay trên những chặng đường dài. 24 phối màu để hợp với mọi chiếc xe road và gravel; mỗi hộp kèm nút bịt ghi đông.',
      spec=[('Kích thước', '215 x 3 cm'), ('Độ dày', '3 mm'), ('Trọng lượng (cặp)', '127 g'), ('Chất liệu', 'Silicone + EVA')],
      variants=[('EMUME001', 'Đen – Trắng', 23), ('EMUME002', 'Đen – Đỏ', 24), ('EMUME003', 'Đen – Xanh dương', 25), ('EMUME004', 'Đen – Xanh lá', 26),
                ('EMUME005', 'Đen – Hồng', 27), ('EMUME006', 'Đen – Vàng', 28), ('EMUME007', 'Trắng – Hồng đậm', 29), ('EMUME008', 'Tím – Trắng', 30),
                ('EMUME009', 'Trắng – Đen', 19), ('EMUME010', 'Nâu cà phê – Đen', 31), ('EMUME011', 'Trắng – Vàng', 32), ('EMUME012', 'Đỏ – Đen', 33),
                ('EMUME013', 'Đỏ – Trắng', 34), ('EMUME014', 'Hồng – Trắng', 36), ('EMUME015', 'Hồng – Đen', 35), ('EMUME016', 'Đen – Đen', 20),
                ('EMUME017', 'Trắng – Đỏ', 21), ('EMUME018', 'Trắng – Trắng', 37), ('EMUME019', 'Vàng – Trắng', 38), ('EMUME020', 'Xanh Bianchi', 39),
                ('EMUME021', 'Trắng – Xanh Bianchi', 40), ('EMUME022', 'Trắng – Cầu vồng', 22), ('EMUME023', 'Cam – Trắng', 41), ('EMUME024', 'Trắng – Xanh dương', 42)],
      features=[('Đục lỗ thoáng khí', 'Bề mặt đục lỗ giúp thoát mồ hôi, giữ tay khô ráo và bám chắc.'),
                ('Êm tay 3mm', 'Lớp silicone + EVA dày 3mm giảm rung từ mặt đường.'),
                ('24 phối màu', 'Dễ phối với màu khung, yên và lốp thành da.'),
                ('Kèm nút bịt ghi đông', 'Mỗi hộp có sẵn cặp nút bịt đầu ghi đông Emume.')]),
 dict(file='emume-bastet.html', group='bastet', name='Bastet', series='Bastet', crop=(0.0, 0.76),
      headline='Dây cuốn siêu nhẹ 93,5g, họa tiết dệt', desc='12 phối màu · 2.8mm · 93,5g',
      intro='Bastet là dòng dây cuốn nhẹ của Emume: chỉ 93,5g mỗi cặp, dày 2.8mm, chất liệu silicone + EVA với họa tiết dệt nổi giúp tăng độ bám. 12 phối màu từ đơn sắc đến chuyển màu ở phần đầu ghi đông.',
      spec=[('Kích thước', '215 x 3 cm'), ('Độ dày', '2.8 mm'), ('Trọng lượng (cặp)', '93.5 g'), ('Chất liệu', 'Silicone + EVA')],
      variants=[('XRBZ01', 'Trắng – Vàng kim', 1), ('XRBZ02', 'Đen – Vàng kim', 2), ('XRBZ03', 'Trắng – Đỏ thẫm', 3), ('XRBZ04', 'Đen – Bạc', 4),
                ('XRBZ05', 'Hồng – Trắng', 5), ('XRBZ06', 'Xám thiên thanh – Đen', 6), ('XRBZ07', 'Trắng – Ngũ sắc', 7), ('XRBZ08', 'Đen – Đỏ', 8),
                ('XRBZ09', 'Trắng – Bạc', 9), ('XRBZ10', 'Trắng – Đen', 10), ('XRBZ11', 'Trắng – Xanh huỳnh quang', 11), ('XRBZ12', 'Trắng – Hồng cánh sen', 12)],
      features=[('Siêu nhẹ 93,5g', 'Nhẹ hơn khoảng 25% so với dòng Basic (127g).'),
                ('Họa tiết dệt nổi', 'Bề mặt có vân giúp bám tay tốt khi đổ đèo và nước rút.'),
                ('Dày 2.8mm', 'Cân bằng giữa cảm giác lái trực tiếp và độ êm.'),
                ('Phối màu chuyển sắc', 'Nhiều mẫu chuyển màu ở phần đầu ghi đông, nổi bật trên xe.')]),
 dict(hidden=True, file='emume-bastet-ra.html', group='bastet', name='Bastet RA đổi màu', series='Bastet', crop=None,
      headline='Dây cuốn đổi màu dưới ánh nắng', desc='2 phối màu · đổi màu ngoài trời',
      intro='Phiên bản Gradient RA của dòng Bastet: họa tiết đổi màu khi ra ngoài trời dưới ánh nắng và trở lại màu gốc khi vào trong nhà. Dày 3mm, nặng 103g mỗi cặp (đã gồm nút bịt ghi đông).',
      spec=[('Kích thước', '215 x 3 cm'), ('Độ dày', '3 mm'), ('Trọng lượng (cặp)', '103 g (gồm nút bịt)'), ('Chất liệu', 'Silicone + EVA')],
      variants=[('XRBZ13', 'Đen (đổi màu ngoài trời)', 45), ('XRBZ14', 'Trắng (đổi màu ngoài trời)', 46)],
      features=[('Đổi màu dưới nắng', 'Trong nhà giữ màu gốc, ra ngoài trời họa tiết chuyển màu.'),
                ('Họa tiết chuyển sắc', 'Hiệu ứng gradient nổi bật trên ghi đông.'),
                ('Kèm nút bịt', 'Trọng lượng 103g đã bao gồm nút bịt ghi đông.')]),
 dict(hidden=True, file='emume-bastet-tricolor.html', group='bastet', name='Bastet Tricolor', series='Bastet', crop=None,
      headline='Ba màu: nền, logo và họa tiết', desc='9 phối màu · 2.8mm · 93,5g',
      intro='Bastet Tricolor phối ba màu riêng biệt cho màu nền, màu logo EMUME và màu họa tiết — dễ chọn đúng tông với khung xe. Nhẹ 93,5g mỗi cặp, dày 2.8mm.',
      spec=[('Kích thước', '215 x 3 cm'), ('Độ dày', '2.8 mm'), ('Trọng lượng (cặp)', '93.5 g'), ('Chất liệu', 'Silicone + EVA')],
      variants=[('XRBZ20', 'Nền trắng – logo đen – họa tiết hồng', 54), ('XRBZ21', 'Nền đen – logo trắng – họa tiết vàng kim', 49),
                ('XRBZ22', 'Nền đen – logo hồng – họa tiết vàng kim', 53), ('XRBZ23', 'Nền đen – logo đỏ – họa tiết bạc', 55),
                ('XRBZ24', 'Nền đen – logo hồng – họa tiết trắng', 51), ('XRBZ25', 'Nền đen – logo đỏ – họa tiết vàng kim', 52),
                ('XRBZ26', 'Nền trắng – logo hồng – họa tiết đen', 50), ('XRBZ27', 'Nền trắng – logo cam – họa tiết vàng kim', 57),
                ('XRBZ28', 'Nền đen – logo vàng – họa tiết trắng', 56)],
      features=[('Phối ba màu', 'Màu nền, màu logo và màu họa tiết riêng biệt.'),
                ('Siêu nhẹ 93,5g', 'Cùng chất liệu và trọng lượng với dòng Bastet.'),
                ('Kèm băng kết thúc & nút bịt', 'Hộp có băng dán kết thúc và cặp nút bịt logo Emume.')]),
 dict(hidden=True, file='emume-bastet-ultra-graphic.html', group='bastet', name='Bastet Ultra Graphic', series='Bastet', crop=None,
      headline='Họa tiết in đồ họa toàn thân', desc='2 mẫu · 2.8mm · 106g',
      intro='Bastet Ultra Graphic in đồ họa phủ kín cuộn dây, tạo điểm nhấn mạnh trên ghi đông. Dày 2.8mm, nặng 106g mỗi cặp.',
      spec=[('Kích thước', '215 x 3 cm'), ('Độ dày', '2.8 mm'), ('Trọng lượng (cặp)', '106 g'), ('Chất liệu', 'Silicone + EVA')],
      variants=[('XRBZ40', 'Mẫu XRBZ40', 48), ('XRBZ41', 'Mẫu XRBZ41', 47)],
      features=[('Đồ họa toàn thân', 'Họa tiết in phủ kín, nổi bật trên xe road và gravel.'),
                ('Dày 2.8mm', 'Cảm giác lái trực tiếp, vẫn đủ êm.')]),
 dict(file='emume-galaxy.html', group='galaxy', name='Galaxy', series='Galaxy', crop=(0.0, 0.70),
      headline='Dây cuốn ánh nhũ dải ngân hà', desc='5 màu · 3mm · 127g',
      intro='Galaxy có các hạt nhũ lấp lánh như dải ngân hà trên nền đục lỗ thoáng khí. Silicone + EVA, nặng 127g mỗi cặp, 5 màu lấy cảm hứng từ vũ trụ.',
      spec=[('Kích thước', '215 x 3 cm'), ('Độ dày', '3 mm'), ('Trọng lượng (cặp)', '127 g'), ('Chất liệu', 'Silicone + EVA')],
      variants=[('GALAXY-01', 'Đen sâu thẳm (Deep Black)', 13), ('GALAXY-02', 'Trắng ánh sao (Star Light White)', 14),
                ('GALAXY-03', 'Vàng bụi sao (Stellar Dust Yellow)', 15), ('GALAXY-04', 'Xanh ngọc vũ trụ (Cosmic Turquoise)', 16),
                ('GALAXY-05', 'Xanh sao (Star Blue)', 17)],
      features=[('Ánh nhũ lấp lánh', 'Hạt nhũ phản chiếu ánh sáng như bầu trời sao.'),
                ('Đục lỗ thoáng khí', 'Giữ tay khô ráo, bám chắc.'),
                ('5 màu vũ trụ', 'Đen, trắng, vàng, xanh ngọc và xanh dương.')]),
 dict(file='emume-anubis-feather.html', group='anubis', name='Anubis Feather', series='Anubis', crop=None,
      headline='Dây cuốn siêu nhẹ chỉ 42g', desc='Siêu nhẹ 42g · 2.8mm',
      intro='Anubis Feather (Lông vũ Anubis) là dây cuốn siêu nhẹ của Emume: chỉ 42g mỗi cặp, dày 2.8mm — dành cho xe đua cần tối ưu từng gram.',
      spec=[('Kích thước', '215 x 3 cm'), ('Độ dày', '2.8 mm'), ('Trọng lượng (cặp)', '42 g'), ('Chất liệu', 'Silicone + EVA')],
      variants=[('XRCQ01', 'Đen', 44)],
      features=[('Chỉ 42g', 'Nhẹ hơn một nửa so với dòng Bastet.'),
                ('Dày 2.8mm', 'Cảm giác lái trực tiếp cho xe đua.')]),
 dict(file='emume-end-tape.html', group='accessory', name='Băng keo kết thúc', series='Phụ kiện', crop=None,
      headline='Băng dán kết thúc dây cuốn', desc='2cm x 10m · 1 cuộn',
      intro='Băng keo PVC Emume dùng để cố định đầu dây cuốn tay lái: rộng 2cm, dài 10m, dày 0.13mm, in họa tiết logo Emume chìm.',
      spec=[('Kích thước', '2 cm x 10 m'), ('Độ dày', '0.13 mm'), ('Trọng lượng', '35 g'), ('Chất liệu', 'PVC')],
      variants=[('END-TAPE', 'Đen', 18)],
      features=[('Cuộn 10m', 'Đủ dùng cho nhiều lần thay dây cuốn.'), ('Họa tiết logo chìm', 'Gọn gàng, đồng bộ với dây cuốn Emume.')]),
 dict(file='emume-titanium-bar-plug.html', group='accessory', name='Nút bịt ghi đông titan', series='Phụ kiện', crop=(0.0, 0.48),
      headline='Nút bịt ghi đông hợp kim titan', desc='Hợp kim titan · 29g',
      intro='Nút bịt đầu ghi đông bằng hợp kim titan, khắc logo Emume — bền, không gỉ và sang trọng.',
      spec=[('Kích thước', '24 x 40 mm'), ('Trọng lượng', '29 g'), ('Chất liệu', 'Hợp kim titan'), ('Mã', 'MNYBD001')],
      variants=[('MNYBD001', 'Titan', 43)],
      features=[('Hợp kim titan', 'Bền, nhẹ và không gỉ.'), ('Khắc logo Emume', 'Hoàn thiện đầu ghi đông gọn đẹp.')]),
 dict(file='emume-titanium-3d-bar-plug.html', group='accessory', name='Nút bịt titan in 3D', series='Phụ kiện', crop=None,
      headline='Nút bịt titan in 3D siêu nhẹ', desc='In 3D titan · 4g',
      intro='Nút bịt ghi đông bằng hợp kim titan in 3D với họa tiết ngôi sao sáu cánh, siêu nhẹ chỉ 4g.',
      spec=[('Kích thước', '25 x 16 x 19 mm'), ('Trọng lượng', '4 g'), ('Chất liệu', 'Hợp kim titan in 3D'), ('Mã', 'BD3D001')],
      variants=[('BD3D001', 'Titan', 58)],
      features=[('In 3D siêu nhẹ', 'Chỉ 4g, tối ưu cho xe đua.'), ('Họa tiết sao sáu cánh', 'Thiết kế độc đáo cho đầu ghi đông.')]),
]
GROUPS = [('basic', 'Basic', 'Dây cuốn đục lỗ cơ bản, 24 phối màu.'),
          ('bastet', 'Bastet', 'Dòng dây cuốn nhẹ 93,5g, 12 phối màu.'),
          ('galaxy', 'Galaxy', 'Dây cuốn ánh nhũ dải ngân hà, 5 màu.'),
          ('anubis', 'Anubis Feather', 'Dây cuốn siêu nhẹ 42g.'),
          ('accessory', 'Phụ kiện', 'Băng keo kết thúc và nút bịt ghi đông titan.')]
FAQ = [('Một hộp gồm những gì?', 'Mỗi hộp dây cuốn gồm 2 cuộn cho hai bên ghi đông; đa số mẫu kèm nút bịt ghi đông và băng dán kết thúc. Liên hệ Spinlab để xác nhận phụ kiện đi kèm của từng mẫu.'),
       ('Dây cuốn dùng cho xe nào?', 'Dùng cho ghi đông drop (cong) của xe road và gravel.'),
       ('Spinlab có quấn dây giúp không?', 'Có. Đội kỹ thuật Spinlab hỗ trợ quấn dây cuốn tay lái — gọi hotline 0399 337 533 để đặt lịch.')]


def img_name(L, code):
    return f'{IMG}{L["file"][:-5]}-{code.lower()}.jpg'


def prepare_images():
    os.makedirs(OUT, exist_ok=True)
    for L in LINES:
        for code, _, n in L['variants']:
            src = os.path.join(SRC, f'image{n}.png')
            dst = os.path.join(D, img_name(L, code))
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '72', src, '--out', dst], check=True, capture_output=True)
            if L['crop']:
                w, h = [int(x) for x in re.findall(r'pixel(?:Width|Height): (\d+)', subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', dst], capture_output=True, text=True).stdout)]
                top, keep = L['crop']
                subprocess.run(['sips', '-c', str(int(h * (keep - top))), str(w), '--cropOffset', str(max(1, int(h * top))), '1', dst], check=True, capture_output=True)  # sips treats a 0 offset as 'centre'
            subprocess.run(['sips', '-Z', '900', dst], check=True, capture_output=True)


def card(L):
    first = img_name(L, L['variants'][0][0])
    return (f'<article class="p-card" data-type="{L["group"]}"><div class="p-img"><img src="{first}" alt="Emume {E(L["name"])}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">Emume · {E(L["series"])}</span><h3 class="p-name"><a class="stretch" href="{L["file"]}">{E(L["name"])}</a></h3>'
            f'<p class="p-desc">{E(L["desc"])}</p><span class="p-price">{price(L)}</span></div></article>')


def page(L, shell):
    v0 = L['variants'][0]
    multi = len(L['variants']) > 1
    thumbs = ''.join(f'<li><button aria-pressed="{"true" if i == 0 else "false"}" data-src="{img_name(L, c)}" data-alt="Emume {E(L["name"])} – {E(lab)}" data-code="{c}"><img src="{img_name(L, c)}" alt="{E(lab)}"></button></li>'
                     for i, (c, lab, _) in enumerate(L['variants']))
    opts = ''.join(f'<label><input type="radio" name="variant" value="{c}" data-label="{E(lab)}" data-img="{img_name(L, c)}"{" checked" if i == 0 else ""}><span>{E(lab)}</span></label>'
                   for i, (c, lab, _) in enumerate(L['variants']))
    pick = (f'<fieldset class="sizes"><legend>Phối màu <span class="size-meta" aria-live="polite"><span id="v-name">{E(v0[1])}</span> · Mã <span id="v-code">{v0[0]}</span></span></legend>'
            f'<div class="size-opts v-opts">{opts}</div></fieldset>') if multi else f'<p class="ver-desc">Mã sản phẩm: <b>{v0[0]}</b></p>'
    spec = ''.join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k, v in L['spec'])
    codes = ''.join(f'<tr data-code="{c}"><td>{c}</td><td>{E(lab)}</td></tr>' for c, lab, _ in L['variants'])
    feats = ''.join(f'<article><span class="num">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(x)}</p></article>' for i, (t, x) in enumerate(L['features']))
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    rel = ''.join(card(o) for o in [o for o in LINES if o is not L][:4])
    main = f'''<main id="main" class="pdp">
  <div class="container">
    <nav class="crumbs" aria-label="Đường dẫn"><ol>
      <li><a href="index.html">Trang chủ</a></li><li><a href="phu-tung.html">Phụ tùng</a></li><li><a href="day-cuon-tay-lai.html">Dây cuốn tay lái</a></li>
      <li><a class="crumb" href="day-cuon-tay-lai.html#{L["group"]}">{E(L["series"])}</a></li><li aria-current="page">{E(L["name"])}</li></ol></nav>
    <div class="pdp-top">
      <div class="gallery">
        <div class="g-main"><img id="g-main" src="{img_name(L, v0[0])}" alt="Emume {E(L["name"])} – {E(v0[1])}" width="900" height="900"></div>
        <ul class="g-thumbs" aria-label="Ảnh sản phẩm">{thumbs}</ul>
      </div>
      <div class="buy">
        <span class="p-brand">Emume · {E(L["series"])}</span>
        <h1>{E(L["name"])}</h1>
        <p class="tagline">{E(L["headline"])}</p>
        {pick}
        <div class="price-row"><span class="label">Giá bán lẻ</span><span class="p-price big">{price(L)}</span></div>
        <div class="buy-ctas">
          <a class="btn btn-zalo outline" href="https://zalo.me/0399337533" target="_blank" rel="noopener"><img src="{ZALO}" alt="" width="22" height="22">Chat Zalo</a>
          <a class="btn btn-outline" href="tel:0399337533">Gọi 0399 337 533</a>
        </div>
        <ul class="assure">
          <li><svg aria-hidden="true"><use href="#i-shield"/></svg>Hàng chính hãng Emume, phân phối bởi Spinlab</li>
          <li><svg aria-hidden="true"><use href="#i-truck"/></svg>Giao hàng toàn quốc</li>
          <li><svg aria-hidden="true"><use href="#i-chat"/></svg>Hỗ trợ quấn dây cuốn tại Spinlab</li>
        </ul>
      </div>
    </div>

    <nav class="pdp-nav" aria-label="Nội dung sản phẩm"><a href="#gioi-thieu">Giới thiệu</a><a href="#cong-nghe">Tính năng</a><a href="#ma-san-pham">Thông số</a><a href="#hoi-dap">Hỏi đáp</a></nav>

    <section class="pdp-sec intro" id="gioi-thieu">
      <div><h2>{E(L["headline"])}</h2><p>{E(L["intro"])}</p></div>
      <figure><img src="{img_name(L, L["variants"][min(1, len(L["variants"]) - 1)][0])}" alt="Emume {E(L["name"])}" loading="lazy"></figure>
    </section>

    <section class="pdp-sec" id="cong-nghe"><h2>Tính năng</h2><div class="tech">{feats}</div></section>

    <section class="pdp-sec" id="ma-san-pham"><h2>Thông số</h2><dl class="spec-list">{spec}</dl>
      <h3 class="codes-h">Mã sản phẩm &amp; phối màu</h3><div class="table-wrap"><table class="sku-table"><thead><tr><th scope="col">Mã</th><th scope="col">Phối màu</th></tr></thead><tbody>{codes}</tbody></table></div>
      <p class="geo-note">Dòng đang chọn được tô màu. Vui lòng liên hệ Spinlab để kiểm tra màu còn hàng.</p></section>

    <section class="pdp-sec" id="hoi-dap"><h2>Hỏi đáp</h2><div class="faq">{faq}</div></section>

    <section class="pdp-sec"><div class="sec-head"><h2>Sản phẩm Emume khác</h2><a class="see-all" href="day-cuon-tay-lai.html">Xem tất cả</a></div>
      <div class="grid related" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">{rel}</div></section>
  </div>
</main>'''
    js = '''// Emume product page: colour/variant selector + gallery
(() => {
  const main=document.getElementById('g-main'), t=[...document.querySelectorAll('.g-thumbs button')];
  const show=code=>{ const b=t.find(x=>x.dataset.code===code)||t[0]; main.src=b.dataset.src; main.alt=b.dataset.alt; t.forEach(x=>x.setAttribute('aria-pressed',x===b));
    document.querySelectorAll('.sku-table tbody tr').forEach(tr=>tr.classList.toggle('on',tr.dataset.code===code)); };
  const pick=code=>{ const r=document.querySelector(`input[name=variant][value="${code}"]`); if(!r) return show(code); r.checked=true;
    document.getElementById('v-name').textContent=r.dataset.label; document.getElementById('v-code').textContent=code; show(code); };
  t.forEach(b=>b.addEventListener('click',()=>pick(b.dataset.code)));
  document.querySelectorAll('input[name=variant]').forEach(r=>r.addEventListener('change',()=>pick(r.value)));
  const first=document.querySelector('input[name=variant]:checked'); show(first?first.value:(t[0]&&t[0].dataset.code));
})();
'''
    css = '''
/* Emume pages */
.v-opts label span{white-space:normal;text-align:left;line-height:1.25;padding:8px 12px;min-height:40px}
.g-thumbs{flex-wrap:wrap}
.codes-h{margin:24px 0 8px;font-size:16px}
.sku-table tr.on{background:#FFF7D6}
'''
    s = re.sub(r'<title>.*?</title>', f'<title>Emume {E(L["name"])} — Dây cuốn tay lái — Spinlab</title>', shell, 1, flags=re.S)
    s = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="Emume {E(L["name"])}: {E(L["headline"])}. Phân phối chính hãng bởi Spinlab.">', s, 1)
    s = re.sub(r'<main id="main".*?</main>', lambda m: main, s, 1, flags=re.S)
    s = re.sub(r'// Tubeless accessory page.*?\}\)\(\);\n', lambda m: js, s, 1, flags=re.S)
    assert '// Emume product page' in s
    s = s.replace('</style>', css + '</style>', 1)
    return s


ALL_LINES = list(LINES)
LINES[:] = [L for L in LINES if not L.get('hidden')]   # hidden lines (hidden=True) are kept here but not published

if SRC:
    prepare_images()
shell = open(os.path.join(D, 'vittoria-universal-sealant.html'), encoding='utf-8').read()
for L in LINES:
    open(os.path.join(D, L['file']), 'w', encoding='utf-8').write(page(L, shell))
    print(L['file'], len(L['variants']))

# listing page (shell: tubeless.html, which already carries the brand-page styles)
T = open(os.path.join(D, 'tubeless.html'), encoding='utf-8').read()
secs = ''.join(f'  <section class="brand-cat" id="{g}"><div class="container"><h2 class="bc-title">{E(t)}</h2><p class="bc-sub">{E(s_)}</p>'
               f'<div class="grid">{"".join(card(L) for L in LINES if L["group"] == g)}</div></div></section>\n' for g, t, s_ in GROUPS)
nav = ('  <nav class="brand-nav" aria-label="Dòng sản phẩm"><div class="container"><ul>' +
       ''.join(f'<li><a href="#{g}">{E(t)}<small>{sum(L["group"] == g for L in LINES)}</small></a></li>' for g, t, s_ in GROUPS) + '</ul></div></nav>')
main = f'''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li><a href="phu-tung.html">Phụ tùng</a></li><li aria-current="page">Dây cuốn tay lái</li></ol></nav></div>
  <section class="list-hero plain">
    <div class="container"><div class="lh-copy"><span class="kicker">Emume</span><h1>Dây cuốn tay lái</h1><p>Dây cuốn ghi đông và phụ kiện Emume chính hãng — Basic, Bastet, Galaxy, Anubis Feather. Phân phối bởi Spinlab.</p></div></div>
  </section>
{nav}
{secs}</main>'''
T = re.sub(r'<title>.*?</title>', '<title>Dây cuốn tay lái Emume — Spinlab</title>', T, 1, flags=re.S)
T = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Dây cuốn tay lái Emume chính hãng tại Spinlab: Basic, Bastet, Galaxy, Anubis Feather và phụ kiện nút bịt titan.">', T, 1)
T = re.sub(r'<main id="main".*?</main>', lambda m: main, T, 1, flags=re.S)
open(os.path.join(D, 'day-cuon-tay-lai.html'), 'w', encoding='utf-8').write(T)
print('day-cuon-tay-lai.html', sum(len(L['variants']) for L in LINES), 'codes')
