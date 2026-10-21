"""Generate Vittoria MTB tire pages (one page per tread line, casing versions selectable).
Usage: mtbtires.py <site_dir> <json_dir>"""
import sys, os, re, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vcommon
D, J = sys.argv[1], sys.argv[2]
E = html.escape
shell = open(os.path.join(D, 'corsa-pro.html'), encoding='utf-8').read()
ZALO = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg'
PRICE = '1.980.000₫'
COLOR_VI = vcommon.COLOR_VI
C4 = ' Hợp chất 4Compound với bốn loại cao su được đặt đúng vị trí cần thiết — kết hợp tốc độ, độ bám và độ bền.'

LINES = [
 dict(type='mtb', file='vittoria-terreno-xc.html', name='Terreno XC', cat='Cross Country', headline='Tên lửa trên đường cứng',
      intro='Terreno XC được thiết kế cho tốc độ tối đa trên đường mòn khô và cứng. Dải gai giữa hình vảy cá lăn cực nhanh trên đường thẳng mà vẫn giữ lực phanh và bám cua khi cần; chuyển tiếp đều từ dải giữa ra núm vai giúp mỗi khúc cua mượt mà, dễ đoán.',
      terrain=['Đường mòn cứng', 'Khô, nhanh', 'Đua XC'],
      versions=[('terreno-xc-race', 'XC Race', 'Phiên bản thi đấu cho tay đua cross country — mọi chi tiết hướng tới tốc độ và độ chính xác.'),
                ('terreno-xc-trail', 'XC Trail', 'Thân lốp Trail Case bền chắc hơn cho đường mòn cứng.' + C4)]),
 dict(type='mtb', file='vittoria-peyote.html', name='Peyote', cat='Cross Country', headline='Tốc độ World Cup trên nhiều địa hình',
      intro='Peyote nằm giữa Terreno và Mezcal, với dải gai giữa thấp xen kẽ giúp tăng tốc độ và độ bám. Gai xếp hình chữ V đặc trưng của Vittoria bám sâu vào đất tơi và đẩy sỏi đá sang hai bên; gai giữa thon dần ra núm vai cho cảm giác vào cua nhạy và dễ đoán.',
      terrain=['Đất tơi, sỏi mịn', 'Hỗn hợp', 'XC / Down Country'],
      versions=[('peyote-xc-race', 'XC Race', 'Phiên bản thi đấu với tốc độ đẳng cấp World Cup.'),
                ('peyote-xc-trail', 'XC Trail', 'Thân lốp Trail Case cho người vừa thích phiêu lưu vừa muốn lên podium.' + C4)]),
 dict(type='mtb', file='vittoria-mazza.html', name='Mazza', cat='Trail / Enduro', headline='Làm chủ đường mòn kỹ thuật',
      intro='Mazza dành cho người cần vào cua tự tin và bám đường chắc chắn trên địa hình đa dạng, nhiều kỹ thuật. Rãnh cắt lũy tiến trên núm vai cân bằng giữa cảm giác đường và độ bám khi ôm cua hay bám vách đá nghiêng; mép gai dốc giúp leo dốc tốt trên những đoạn gồ ghề.',
      terrain=['Trail kỹ thuật', 'Enduro', 'Đá, rễ cây'],
      versions=[('mazza-trail', 'Trail', 'Thân lốp Trail Case; gai thưa tự làm sạch đất và bùn.' + C4),
                ('mazza-enduro', 'Enduro', 'Bản enduro đa năng cho shuttle, gravity và những ngày đạp trên địa hình kỹ thuật — ứng dụng công nghệ đã được chứng minh ở EWS.'),
                ('mazza-enduro-race', 'Enduro Race', 'Hợp chất thi đấu tối đa độ bám, giảm rung và đàn hồi mượt — thiết kế theo yêu cầu của tay đua EWS.')]),
 dict(type='mtb', file='vittoria-martello.html', name='Martello', cat='Trail / Enduro', headline='Huyền thoại enduro, bám chắc mọi điều kiện',
      intro='Martello đã được chứng minh ở enduro và downhill đỉnh cao. Núm gai lấy cảm hứng từ lốp mô tô bền bỉ, hoạt động tốt trên địa hình kỹ thuật cả khô lẫn ướt; rãnh cắt lũy tiến thay đổi độ dày mép gai để cân bằng cảm giác đường và độ bám mà không mất ổn định.',
      terrain=['Cứng đến hỗn hợp', 'Enduro / DH', 'Khô và ướt'],
      versions=[('martello-trail', 'Trail', 'Lốp trail linh hoạt nhất cho đường cứng đến hỗn hợp; gai thưa tự làm sạch đất và bùn.' + C4),
                ('martello-enduro', 'Enduro', 'Cho mọi thứ từ thi đấu gravity đến khám phá — bám chắc trên mọi chướng ngại.'),
                ('martello-enduro-race', 'Enduro Race', 'Cấu trúc tinh chỉnh cho thi đấu — bám chắc, giảm rung, đàn hồi mượt trên những đoạn kỹ thuật và dốc nghiêng.')]),
 dict(type='mtb', file='vittoria-mezcal.html', name='Mezcal', cat='Cross Country', headline='Tốc độ XC thuần khiết, nhiều lần vô địch',
      intro='Mezcal được thiết kế cho tốc độ cross country thuần túy và đã được chứng minh qua nhiều chức vô địch thế giới UCI và vô địch châu Âu XCO. Mẫu gai lăn nhanh, bám chắc khi vào cua — lựa chọn quen thuộc của các tay đua XC.',
      terrain=['Đua XC', 'Đường mòn hỗn hợp', 'Khô và ẩm'],
      versions=[('mezcal-xc-race', 'XC Race', 'Hợp chất Race Graphene + Silica cho tốc độ và độ bám không thỏa hiệp; thân lốp nylon 60 TPI mềm mại, đáng tin cậy, giảm mỏi khi thi đấu.'),
                ('mezcal-xc-trail', 'XC Trail', 'Thân lốp Trail Case bền chắc cho đạp đường mòn hằng ngày.' + C4)]),
 dict(type='road', file='vittoria-corsa-pro-speed.html', name='Corsa PRO Speed', cat='Time Trial / Triathlon', headline='Lốp nhanh nhất cho đua tính giờ & triathlon',
      intro='Được thiết kế riêng cho đua tính giờ và triathlon, Corsa PRO Speed giúp tay đua chuyên nghiệp lẫn nghiệp dư đạt thành tích tốt nhất. Mặt gai thon liền vào thành lốp, hợp chất Graphene + Silica, thân lốp Corespun cotton 320 TPI — loại tốt nhất của Vittoria — cùng mẫu gai mới, tất cả được lưu hóa bằng điện để giảm tối đa lực cản lăn. Theo thử nghiệm nội bộ của Vittoria, hiệu quả lăn tăng 5% và trọng lượng giảm 2%.',
      terrain=['Đua tính giờ (TT)', 'Triathlon', 'Đường nhựa tốt'],
      versions=[('corsa-pro-speed-tubeless-ready', 'Tubeless-Ready', 'Bản không săm (tubeless-ready) chuyên cho thi đấu tốc độ.')]),
 dict(type='road', file='vittoria-corsa-next.html', name='Corsa N.Ext', cat='Thi đấu & tập luyện', headline='Tốc độ đua, độ bền tập luyện hằng ngày',
      intro='Ngày đua, bài tập interval, những chuyến leo nhiều đèo hay những buổi đạp dài một mình — Corsa N.Ext kết hợp độ bám vào cua cao, lực cản lăn thấp với cấu trúc siêu bền của một chiếc lốp tập luyện hằng ngày. Hợp chất Graphene + Silica đã được kiểm chứng ở WorldTour cùng thân lốp nylon bền lâu.',
      terrain=['Thi đấu', 'Tập luyện dài', 'Đèo dốc'],
      versions=[('corsa-n-ext-tubeless-ready', 'Tubeless-Ready', 'Bản không săm, thêm lớp Inner Shield bảo vệ; tương thích vành TSS/hookless từ cỡ 28mm trở lên.'),
                ('corsa-n-ext-tube-type', 'Dùng săm', 'Bản dùng săm (clincher) truyền thống, tiện lợi và dễ thay thế.')]),
 dict(type='road', file='vittoria-rubino.html', name='Rubino', cat='Tập luyện hằng ngày', headline='Lốp tập luyện hằng ngày, được tái sinh',
      intro='Rubino — dòng lốp hiệu năng hằng ngày ở trung tâm dải sản phẩm Vittoria — nay được thiết kế lại hoàn toàn. Lốp quen thuộc cho những buổi đạp trưa, những pha nước rút và những chuyến đi không hồi kết, nay nhanh hơn, bám hơn, bền hơn và nhẹ hơn.',
      terrain=['Tập luyện hằng ngày', 'Đi làm, đạp phố', 'Đường dài'],
      versions=[('rubino-tubeless-ready', 'Tubeless-Ready', 'Có lớp Inner Shield. Theo Vittoria, so với thế hệ trước: lăn hiệu quả hơn 18%, bám hơn 5%, chống thủng tốt hơn 21%, êm hơn 13%, bền hơn 37% và nhẹ hơn 10%.'),
                ('rubino-tube-type', 'Dùng săm', 'Bản dùng săm với nhiều màu thành lốp: đen, nâu nhạt, xanh dương, đỏ, trắng, vàng.')]),
 dict(type='road', file='vittoria-corsa-pro-limited.html', name='Corsa PRO Limited Edition', cat='Phiên bản giới hạn', headline='Corsa PRO, khoác màu mới',
      intro='Phiên bản đặc biệt của Corsa PRO — một trong những lốp road giành nhiều chiến thắng nhất — với thành lốp màu hồng hoặc đen toàn phần. Theo Vittoria, hiệu năng giống hệt Corsa PRO tiêu chuẩn: thân lốp cotton 320 TPI, hợp chất Graphene + Silica và mặt gai được lưu hóa liền vào thân lốp. Có cỡ 700x28c và 700x30c.',
      terrain=['Đua road', 'Gran Fondo', 'Phong cách riêng'],
      versions=[('corsa-pro-limited', 'Tubeless-Ready', 'Phiên bản giới hạn, số lượng có hạn. Hiệu năng như Corsa PRO tiêu chuẩn, khác biệt ở màu thành lốp.')]),

 dict(type='road', file='vittoria-corsa-pro-tube-type.html', name='Corsa PRO Tube-Type', cat='Thi đấu · Dùng săm', headline='Corsa PRO cho người dùng săm',
      intro='Corsa PRO Tube-Type mang công nghệ của lốp đua thành công nhất thế giới lên nền lốp dùng săm (clincher) quen thuộc: bám vào cua tuyệt vời cả khi khô lẫn ướt, chống thủng được gia cường và thân lốp mềm mại giúp mặt đường xấu êm như đường mới trải nhựa. Theo Vittoria, so với Corsa Tube-Type thế hệ trước: lăn hiệu quả hơn 12%, chống thủng tốt hơn 18% và nhẹ hơn 9%.',
      terrain=['Đua road', 'Tập luyện cường độ cao', 'Đèo dốc'],
      versions=[('corsa-pro-tube-type', 'Dùng săm', 'Thân lốp cotton 320 TPI, hợp chất Graphene + Silica, thành lốp màu da (Para).')]),
 dict(type='road', file='vittoria-corsa-pro-tubular.html', name='Corsa PRO Tubular', cat='Thi đấu · Lốp ống', headline='Lốp ống (tubular) đua đỉnh cao',
      intro='Không loại lốp nào phản hồi như lốp ống, và không lốp ống nào có cảm giác như Corsa PRO: bám vào cua cao cả khi khô lẫn ướt, lực cản lăn thấp và thân lốp mềm mại ôm mặt đường. Corsa PRO Tubular còn cực nhẹ — theo Vittoria, mỗi cặp nhẹ hơn 190g so với Corsa PRO tubeless-ready dùng keo hoặc săm latex.',
      terrain=['Đua road', 'Leo đèo', 'Vành dùng lốp ống'],
      versions=[('corsa-pro-tubular', 'Lốp ống', 'Thân lốp cotton-corespun 320 TPI, hợp chất Graphene + Silica, đai chống thủng; dùng cho vành lốp ống (tubular).')]),
 dict(type='road', file='vittoria-juniores-tubular.html', name='Juniores Tubular', cat='Lốp ống cho tay đua trẻ', headline='Lốp ống cho thế hệ tay đua kế tiếp',
      intro='Juniores Tubular đưa lốp ống — công nghệ gắn với mọi thế hệ tay đua huyền thoại — đến với các tay đua trẻ. Cấu trúc tương tự lốp Rally nhưng thu nhỏ cho bánh xe cỡ nhỏ; thân lốp cotton giữ cảm giác mặt đường mềm mại đặc trưng của lốp ống, hợp chất ưu tiên độ bền và chống thủng.',
      terrain=['Xe đua trẻ em / thiếu niên', 'Tập luyện', 'Vành lốp ống 24"'],
      versions=[('juniores-tubular', 'Lốp ống 24"', 'Cỡ 21-24, thành lốp màu da (Para); hợp chất 1C, thân lốp cotton 220 TPI.')]),
 dict(type='road', file='vittoria-zaffiro.html', name='Zaffiro V', cat='Tập luyện · Đi phố', headline='Lốp road tập luyện bền bỉ',
      intro='Zaffiro là dòng lốp road tập luyện mọi điều kiện của Vittoria: bền, chống thủng tốt và ổn định cho những chặng đường dài, tập luyện đầu mùa hay đi làm hằng ngày. Bản Spinlab đang có là Zaffiro V 700x25c, tanh cứng (rigid), màu đen toàn phần.',
      terrain=['Tập luyện', 'Đi làm, đạp phố', 'Mọi thời tiết'],
      versions=[('zaffiro-v', 'Tanh cứng', 'Zaffiro V 25-622, tanh cứng, đen toàn phần. Ảnh minh họa dòng Zaffiro.')]),
 dict(type='road', file='vittoria-combo-corsa-n-ext.html', name='Combo 2 lốp Corsa N.Ext TLR + keo 80ml', cat='Combo tiết kiệm', headline='Trọn bộ lên tubeless cho xe road',
      intro='Combo gồm 2 lốp Corsa N.Ext 700x28c tubeless-ready màu đen kèm 1 chai keo tự vá 80ml — đủ để chuyển cả hai bánh sang tubeless. Corsa N.Ext kết hợp độ bám vào cua cao, lực cản lăn thấp với độ bền của lốp tập luyện.',
      terrain=['Thi đấu', 'Tập luyện dài', 'Lên tubeless'],
      versions=[('combo-corsa-n-ext-tlr', 'Combo', '2 lốp Corsa N.Ext 28-622 TLR đen + keo 80ml.')]),
 dict(type='road', file='vittoria-combo-rubino.html', name='Combo 2 lốp Rubino + 2 săm', cat='Combo tiết kiệm', headline='Trọn bộ lốp tập luyện kèm săm',
      intro='Combo gồm 2 lốp Rubino V 700x28c gấp được (fold) màu đen kèm 2 săm — bộ lốp tập luyện hằng ngày đầy đủ cho cả hai bánh.',
      terrain=['Tập luyện hằng ngày', 'Đi làm, đạp phố', 'Đường dài'],
      versions=[('combo-rubino', 'Combo', '2 lốp Rubino V 28-622 fold đen + 2 săm.')]),
 dict(type='mtb', file='vittoria-barzo.html', name='Barzo', cat='Cross Country', headline='Biến địa hình hỗn loạn thành kiểm soát',
      intro='Barzo có mẫu gai đã giành chức vô địch thế giới cho địa hình sỏi to, đất rời, nay trên cấu trúc XC Race thế hệ mới. Gai giữa xen kẽ lăn nhanh trên mặt đường gồ ghề mà vẫn bám khi leo dốc; núm vai lấy cảm hứng từ lốp mô tô bám sâu khi vào cua mạnh; rãnh cắt toàn bộ và khoảng cách gai rộng giúp bám tốt và tự làm sạch.',
      terrain=['Sỏi to, đất rời', 'Đá, gồ ghề', 'Đua XC'],
      versions=[('barzo-xc-race', 'XC Race', 'Theo Vittoria, cấu trúc XC Race mới nhanh hơn 20%, bám hơn 8%, chống thủng tốt hơn 44% và êm hơn 9%.')]),

 dict(type='dirtjump', file='vittoria-tattoo.html', name='Tattoo', cat='Dirt Jump · Street', headline='Bám dính trên mọi bề mặt',
      intro='Mặt gai siêu mịn như giũa kim cương cùng đặc tính mềm, bám của công nghệ Vittoria giúp Tattoo tăng độ bám, khả năng kiểm soát và độ bền cho mọi buổi chơi — pump track, freestyle park, ramp hay đường phố. Gai phủ kín từ tanh này sang tanh kia, bảo vệ lốp trên mọi bề mặt và luôn bám tốt khi lướt trên rail hay ramp.',
      terrain=['Dirt jump', 'Pump track', 'Street / Park'],
      versions=[('tattoo', 'Tattoo BMX', 'Cỡ 26x2.3 cho xe dirt jump / street.')]),
]


TYPE = {'mtb': ('MTB', 'lop-xe.html#mtb', 'Lốp MTB'), 'road': ('Road', 'lop-xe.html#road', 'Lốp Road'), 'dirtjump': ('DirtJump', 'lop-xe.html#dirtjump', 'Lốp DirtJump')}


# versions sold by Spinlab that Vittoria's shop data does not list: images/tech from a base handle, variants given here
CUSTOM = {
    'zaffiro-v': dict(base='zaffiro-evo', variants=[dict(size='700x25c', color='Black', sku='11A00304')]),
    'combo-corsa-n-ext-tlr': dict(base='corsa-n-ext-tubeless-ready', variants=[dict(size='2 x 700x28c + keo 80ml', color='Black', sku='11P00084')]),
    'combo-rubino': dict(base='rubino-tube-type', variants=[dict(size='2 x 700x28c + 2 săm', color='Black', sku='11P00089')]),
}
for _h, _c in CUSTOM.items():   # share the base product's technology section (not its size chart)
    if _c['base'] in vcommon.TECH:
        vcommon.TECH.setdefault(_h, dict(vcommon.TECH[_c['base']], chart=[]))


def load(h):
    c = CUSTOM.get(h)
    p = json.load(open(os.path.join(J, (c['base'] if c else h) + '.json'), encoding='utf-8'))['product']
    imgs = [i['src'].split('?')[0] for i in p['images']][:6]
    raw = c['variants'] if c else [dict(size=v['option1'], color=v['option2'], sku=v['sku']) for v in p['variants']]
    return dict(images=imgs, cimg=p.get('color_images', {}), variants=vcommon.in_stock(h, raw))


def live(L):
    """Versions of line L with at least one in-stock variant."""
    return [v for v in L['versions'] if load(v[0])['variants']]


def card(L):
    lv = live(L) or L['versions']
    v0 = load(lv[0][0])
    vers = ' · '.join(v[1] for v in lv)
    return (f'<article class="p-card" data-type="{L["type"]}"><div class="p-img tire"><span class="tag dark">{E(L["cat"])}</span>'
            f'<img src="{v0["images"][0]}?width=600" alt="Lốp Vittoria {E(L["name"])}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">Vittoria · {TYPE[L["type"]][0]}</span>'
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

FAQ_MTB = [('Nên chọn phiên bản nào?', 'Bản Race tối ưu tốc độ và trọng lượng cho thi đấu. Bản Trail có thân lốp Trail Case bền chắc hơn cho đạp đường mòn hằng ngày. Bản Enduro chắc chắn hơn nữa cho địa hình gravity, đổ dốc kỹ thuật.'),
       ('Chọn kích thước lốp thế nào?', 'Chọn theo cỡ bánh (27.5" hoặc 29") và bề rộng phù hợp với vành, khoảng hở khung/phuộc của xe. Liên hệ Spinlab để được tư vấn theo xe bạn đang dùng.'),
       ('Có lắp không săm (tubeless) được không?', 'Liên hệ Spinlab để được xác nhận khả năng lắp tubeless của từng phiên bản, cũng như tư vấn vành, van và dung dịch sealant phù hợp.')]

FAQ_ROAD = [('Nên chọn bản Tubeless-Ready hay dùng săm?', 'Bản Tubeless-Ready có thể lắp không săm với sealant để giảm nguy cơ thủng và chạy áp suất thấp hơn, êm hơn; vẫn có thể dùng với săm. Bản dùng săm đơn giản, dễ thay thế ở mọi nơi.'),
            ('Chọn kích thước lốp road thế nào?', 'Chọn theo bề rộng lòng trong của vành và khoảng hở khung xe. Xem cột ETRTO trong Bảng kỹ thuật và liên hệ Spinlab để được tư vấn theo bánh xe bạn đang dùng.'),
            ('Có lắp được trên vành hookless không?', 'Tùy kích thước và phiên bản. Liên hệ Spinlab để được kiểm tra khả năng tương thích với vành của bạn trước khi lắp.')]

FAQ_DJ = [('Chọn cỡ lốp nào?', 'Spinlab hiện có cỡ 26x2.3 cho xe dirt jump / street bánh 26 inch. Liên hệ Spinlab nếu bạn chưa chắc cỡ bánh xe của mình.'),
          ('Nên bơm áp suất bao nhiêu?', 'Áp suất phụ thuộc cân nặng, kiểu chơi (park, street, pump track) và cỡ lốp. Đội kỹ thuật Spinlab sẽ tư vấn mức phù hợp cho bạn.')]


def page(L):
    vers = [(h, lab, b, load(h)) for h, lab, b in live(L)]
    if not vers:
        return None
    name = L['name']
    imgs0 = vers[0][3]['images']
    thumbs = ''.join(f'<li><button aria-pressed="{"true" if k == 0 else "false"}" data-src="{u}?width=1000" data-alt="{E(name)} – ảnh {k+1}"><img src="{u}?width=160" alt="Ảnh {k+1}"></button></li>' for k, u in enumerate(imgs0))
    vopts = ''.join(f'<label><input type="radio" name="ver" value="{k}"{" checked" if k == 0 else ""}><span>{E(lab)}</span></label>' for k, (h, lab, b, d) in enumerate(vers))
    vrows = ''.join(f'<tr><th scope="row">{E(lab)}</th><td>{E(", ".join(dict.fromkeys(v["size"] for v in d["variants"])))}</td>'
                    f'<td>{E(", ".join(dict.fromkeys(COLOR_VI.get(v["color"], v["color"]) for v in d["variants"])))}</td><td>{E(b)}</td></tr>' for h, lab, b, d in vers)
    srows = ''.join(f'<tr data-sku="{v["sku"]}"><td>{E(lab)}</td><td>{E(v["size"])}</td><td>{E(COLOR_VI.get(v["color"], v["color"]))}</td><td>{v["sku"]}</td></tr>'
                    for h, lab, b, d in vers for v in d['variants'])
    same = [o for o in LIVE if o is not L and o['type'] == L['type']]
    RT = TYPE[L['type']] if same else TYPE['mtb']
    related = ''.join(card(o) for o in (same or [o for o in LIVE if o['type'] == 'mtb']))
    TL = TYPE[L['type']]
    tech_html = vcommon.tech_section([(h, lab) for h, lab, b, d in vers])
    spec_html = vcommon.spec_section([(h, lab) for h, lab, b, d in vers], lambda h: load(h)['variants'])
    vfield = (f'<fieldset class="opt-group"><legend>Phiên bản</legend><div class="size-opts">{vopts}</div><p class="ver-desc" id="ver-desc">{E(vers[0][2])}</p></fieldset>' if len(vers) > 1 else f'<p class="ver-desc" id="ver-desc"><b>{E(vers[0][1])}</b> — {E(vers[0][2])}</p>')
    terrain = ''.join(f'<li>{E(x)}</li>' for x in L['terrain'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in {'road': FAQ_ROAD, 'dirtjump': FAQ_DJ}.get(L['type'], FAQ_MTB))
    fig = imgs0[2] if len(imgs0) > 2 else imgs0[-1]
    vtable_open, vtable_close = ('', '') if len(vers) > 1 else ('<!--', '-->')

    main = f'''<main id="main" class="pdp">
  <div class="container">
    <nav class="crumbs" aria-label="Đường dẫn"><ol>
      <li><a href="index.html">Trang chủ</a></li><li><a href="phu-tung.html">Phụ tùng</a></li><li><a href="lop-xe.html">Lốp xe</a></li>
      <li><a class="crumb" href="{TL[1]}">{TL[0]}</a></li><li aria-current="page">{E(name)}</li></ol></nav>
    <div class="pdp-top">
      <div class="gallery">
        <div class="g-main"><img id="g-main" src="{imgs0[0]}?width=1000" alt="Lốp Vittoria {E(name)}" width="1000" height="1000"></div>
        <ul class="g-thumbs" aria-label="Ảnh sản phẩm">{thumbs}</ul>
      </div>
      <div class="buy">
        <span class="p-brand">Vittoria · {TL[2]} · {E(L["cat"])}</span>
        <h1>{E(name)}</h1>
        <p class="tagline">{E(L["headline"])}</p>
        {vfield}
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

    <nav class="pdp-nav" aria-label="Nội dung sản phẩm"><a href="#gioi-thieu">Giới thiệu</a>{'<a href="#phien-ban">Phiên bản</a>' if len(vers) > 1 else ''}<a href="#cong-nghe">Công nghệ</a><a href="#ma-san-pham">Bảng kỹ thuật</a><a href="#hoi-dap">Hỏi đáp</a></nav>

    <section class="pdp-sec intro" id="gioi-thieu">
      <div><h2>{E(L["headline"])}</h2><p>{E(L["intro"])}</p>
        <p class="siblings"><b>Địa hình phù hợp:</b></p><ul class="fit">{terrain}</ul></div>
      <figure><img src="{fig}?width=900" alt="Lốp Vittoria {E(name)}" loading="lazy"></figure>
    </section>

    {vtable_open}<section class="pdp-sec" id="phien-ban"><h2>Các phiên bản</h2>
      <div class="table-wrap"><table class="vtable"><thead><tr><th scope="col">Phiên bản</th><th scope="col">Kích thước</th><th scope="col">Màu</th><th scope="col">Đặc điểm</th></tr></thead><tbody>{vrows}</tbody></table></div>
    </section>{vtable_close}

    {tech_html}

    {spec_html}

    <section class="pdp-sec" id="hoi-dap"><h2>Hỏi đáp</h2><div class="faq">{faq}</div></section>

    <section class="pdp-sec"><div class="sec-head"><h2>{RT[2] + (" khác" if same else "")}</h2><a class="see-all" href="{RT[1]}">Xem tất cả {RT[2].lower()}</a></div>
      <div class="grid related" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">{related}</div></section>
  </div>
</main>'''

    data = [dict(label=lab, blurb=b, images=d['images'], cimg=d.get('cimg', {}), variants=d['variants']) for h, lab, b, d in vers]
    js = '''// MTB tire page: version -> colour -> size selector, gallery
(() => {
  const V = %s, CV = %s;
  const $ = id => document.getElementById(id), main = $('g-main'), list = document.querySelector('.g-thumbs');
  let ver = 0, color = null, size = null;
  const radios = (box, name, items, cur) => { box.innerHTML = items.map(x => `<label><input type="radio" name="${name}" value="${x}"${x===cur?' checked':''}><span>${CV[x]||x}</span></label>`).join(''); };
  const bindThumbs = () => { const t=[...list.querySelectorAll('button')]; t.forEach(b=>b.onclick=()=>{ main.src=b.dataset.src; main.alt=b.dataset.alt; t.forEach(x=>x.setAttribute('aria-pressed',x===b)); }); };
  const setImgs = (imgs, label) => { main.src = imgs[0] + '?width=1000';
    list.innerHTML = imgs.map((u,i)=>`<li><button aria-pressed="${i===0}" data-src="${u}?width=1000" data-alt="${label} – ảnh ${i+1}"><img src="${u}?width=160" alt="Ảnh ${i+1}"></button></li>`).join(''); bindThumbs(); };
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
    document.querySelectorAll('#color-opts input').forEach(r=>r.onchange=()=>{ color=r.value; const ci=(V[ver].cimg||{})[color]; if(ci&&ci.length) setImgs(ci, (CV[color]||color)); render(); });
    document.querySelectorAll('#size-opts input').forEach(r=>r.onchange=()=>{ size=r.value; render(); });
  };
  const setVer = k => { ver = +k; const v = V[ver]; $('ver-desc').textContent = v.blurb; document.querySelectorAll('[data-tech]').forEach(el=>el.hidden=el.dataset.tech!=String(ver));
    main.src = v.images[0] + '?width=1000';
    list.innerHTML = v.images.map((u,i)=>`<li><button aria-pressed="${i===0}" data-src="${u}?width=1000" data-alt="${v.label} – ảnh ${i+1}"><img src="${u}?width=160" alt="Ảnh ${i+1}"></button></li>`).join('');
    bindThumbs(); render(); };
  document.querySelectorAll('input[name=ver]').forEach(r=>r.addEventListener('change',()=>setVer(r.value)));
  bindThumbs(); render();
})();
''' % (json.dumps(data, ensure_ascii=False), json.dumps(COLOR_VI, ensure_ascii=False))

    p = shell
    p = re.sub(r'<title>.*?</title>', f'<title>Vittoria {E(name)} — {TL[2]} — Spinlab</title>', p, 1, flags=re.S)
    p = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{TL[2]} Vittoria {E(name)}: {E(L["headline"])}. Phân phối chính hãng bởi Spinlab.">', p, 1)
    p = p.replace('</style>', CSS + vcommon.CSS + '</style>', 1)
    p = re.sub(r'<main id="main" class="pdp">.*?</main>', lambda m: main, p, 1, flags=re.S)
    p = re.sub(r'// Product gallery \+ size selector.*?\}\)\(\);\n', lambda m: js, p, 1, flags=re.S)
    open(os.path.join(D, L['file']), 'w', encoding='utf-8').write(p)
    return L['file']


LIVE = [L for L in LINES if live(L)]

if __name__ == '__main__':
    for L in LINES:
        f = page(L)
        print(f or f'-- hết hàng, không tạo trang: {L["file"]}')
    for ty in ('mtb', 'road', 'dirtjump'):
        open(os.path.join(J, '..', f'{ty}-cards.html'), 'w', encoding='utf-8').write('\n'.join(card(L) for L in LIVE if L['type'] == ty))
