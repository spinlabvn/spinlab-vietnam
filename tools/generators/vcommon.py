"""Shared helpers for Vittoria tire pages: Vietnamese technology copy, spec table (size/ETRTO/colour/weight/SKU)."""
import json, os, html
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
TECH = json.load(open(os.path.join(HERE, 'vtech.json'), encoding='utf-8'))

# Sizes Spinlab does not sell, per Vittoria product handle (hidden from selectors and spec charts)
EXCLUDE_SIZES = {'corsa-pro-speed-tubeless-ready': {'700x24c', '700x26c'}}

COLOR_VI = {'Brown': 'Thành nâu', 'Black': 'Đen', 'Para': 'Thành da (Para)', 'Tan': 'Thành nâu nhạt (Tan)',
            'Blue': 'Xanh dương', 'Red': 'Đỏ', 'Pink': 'Hồng', 'White': 'Trắng', 'Yellow': 'Vàng'}

# Vietnamese technology names/descriptions keyed by lower-cased Vittoria title
TECH_VI = {
 '1c compound': ('Hợp chất 1C', 'Hỗn hợp cao su vừa bám dính vừa bền — sinh ra cho những buổi chơi thả ga.'),
 '120-tpi nylon casing': ('Thân lốp nylon 120 TPI', 'Thân lốp nylon mềm, chống mài mòn; TPI cao giảm lực cản lăn và giữ độ bám nhạy với địa hình — bền và đáng tin cậy hơn.'),
 '100 tpi nylon casing': ('Thân lốp nylon 100 TPI', 'Bền bỉ, lâu dài, đáng tin cậy — thân lốp chống thủng cho cả thi đấu lẫn những buổi tập dài, sợi dày hơn chịu được cường độ tập luyện hằng ngày.'),
 '320 tpi cotton-corespun casing': ('Thân lốp Cotton-Corespun 320 TPI', 'Sợi cotton nhẹ quấn cùng sợi aramid bền chắc: cảm giác mặt đường mềm mại, tự nhiên của cotton kết hợp khả năng chống thủng của aramid.'),
 '4compound formulation powered by graphene': ('Hợp chất 4Compound tăng cường Graphene', '4 loại cao su tối ưu được đặt đúng vị trí cần thiết, kết hợp tốc độ, độ bám và độ bền vượt trội.'),
 'anti-puncture belt': ('Đai chống thủng', 'Lớp đai bổ sung tăng khả năng chống thủng, giúp hành trình liền mạch, không gián đoạn.'),
 'bead shield': ('Bead Shield', 'Lớp bảo vệ bổ sung ở vùng tanh lốp.'),
 'bead-to-bead protection layer': ('Lớp bảo vệ toàn thân (bead-to-bead)', 'Lớp chống thủng bằng nylon mềm dẻo phủ từ tanh này sang tanh kia.'),
 'eco race casing': ('Thân lốp Eco Race', 'Thân lốp cotton hữu cơ nhiều lớp gia cường bằng latex tự nhiên, kèm lớp bảo vệ thành và đai chống thủng bằng nylon tái chế — giảm mỏi, tăng tốc độ và độ tin cậy ngày thi đấu.'),
 'eco race formulation': ('Hợp chất Eco Race', 'Hợp chất thế hệ mới dành riêng cho đua gravel, tốc độ và độ bám vượt trội trên nhiều địa hình. Thành phần tái tạo và tái chế gồm cao su thiên nhiên chứng nhận Fair-Rubber, dầu đậu nành và silica từ tro vỏ trấu.'),
 'endurance casing': ('Thân lốp Endurance', 'Thân lốp nylon 100 TPI chịu được điều kiện khắc nghiệt của gravel; sợi bền giảm lực cản lăn, giữ cảm giác nhạy và hấp thụ rung động cho những chuyến đi dài.'),
 'endurance formulation graphene': ('Hợp chất Endurance tăng cường Graphene', 'Tin cậy, bền bỉ và hiệu năng cao cho những chặng đường dài, trong mọi điều kiện thời tiết.'),
 'endurance formulation powered by graphene': ('Hợp chất Endurance tăng cường Graphene', 'Hợp chất cao su bổ sung Graphene cho độ bền, độ bám và tuổi thọ tối đa — bám đường ổn định và hiệu quả trong mọi điều kiện thời tiết, trên những chặng đường dài.'),
 'enduro casing': ('Thân lốp Enduro', 'Thân lốp nylon 2 lớp chống mài mòn và chống thủng, thiết kế cho enduro và những lượt đổ dốc liên tục.'),
 'graphene + silica': ('Hợp chất Graphene + Silica', 'Cao su bổ sung Graphene và Silica, tối ưu cho quãng đường dài, chống thủng, bám tốt và nhanh khi đạp hằng ngày.'),
 'inner shield': ('Inner Shield', 'Lớp bảo vệ bổ sung bên trong, yên tâm trên mọi cung đường.'),
 'natural brown color': ('Màu nâu tự nhiên', 'Sản phẩm làm từ vật liệu tự nhiên nên màu sắc có thể khác nhau đôi chút giữa các lốp; hiệu năng không thay đổi.'),
 'organic cotton casing': ('Thân lốp cotton hữu cơ', 'Thân lốp cotton hữu cơ nhiều lớp gia cường bằng latex tự nhiên — cảm giác đạp mềm mại hơn, giảm ô nhiễm nông nghiệp.'),
 'race casing': ('Thân lốp Race', 'Cấu trúc nylon nhiều lớp mềm mại và đáng tin cậy — giảm mỏi, tăng độ tin cậy ngày thi đấu.'),
 'race formulation graphene + silica': ('Hợp chất Race Graphene + Silica', 'Hợp chất bền, tối ưu cho độ bám lâu dài và lực cản lăn thấp, tuổi thọ cao.'),
 'race formulation powered by graphene + silica': ('Hợp chất Race Graphene + Silica', 'Hợp chất thi đấu tối ưu cho địa hình nhanh và kỹ thuật, cân bằng giữa tốc độ và khả năng kiểm soát.'),
 'race formulation powered by graphene and silica': ('Hợp chất Race Graphene + Silica', 'Tốc độ và độ bám không thỏa hiệp — lựa chọn nhanh nhất từ điểm A đến điểm B.'),
 'recycled nylon anti-puncture belt': ('Đai chống thủng nylon tái chế', 'Tăng khả năng chống thủng; làm từ nylon tái chế Seawastex® từ lưới đánh cá đã qua sử dụng.'),
 'recycled nylon sidewall protection': ('Bảo vệ thành lốp nylon tái chế', 'Lớp nylon tái chế Seawastex® gia cường, tăng bảo vệ và độ ổn định bên hông lốp.'),
 'sidewall protection': ('Bảo vệ thành lốp', 'Lớp nylon gia cường tăng bảo vệ và độ ổn định bên hông lốp.'),
 'sidewall stability insert': ('Lớp chèn ổn định thành lốp', 'Lớp cao su công nghệ cao chống va đập vành và hỗ trợ thành lốp.'),
 'trail casing': ('Thân lốp Trail', 'Thân lốp nylon 60 TPI bền chắc cho những chuyến khám phá — chống mài mòn và chống thủng, độ mềm vừa phải để vẫn cảm nhận rõ đường mòn.'),
}
WIDE_RIM_VI = ('Tối ưu cho vành rộng (29c WR)', 'Lốp có bề ngang 29mm trên vành lòng trong 25mm; hình dạng thân và mặt lốp tối ưu cho vành rộng hiện đại, cải thiện khí động học, chống thủng và độ bám khi vào cua ở góc nghiêng lớn.')

CSS = '''
/* Vittoria technology + spec chart */
.tech-v[hidden]{display:none}
.tech{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr))}
@media (min-width:1024px){.tech{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
@media (max-width:479px){.tech{grid-template-columns:1fr}}
.tech article{padding:20px;border:1px solid var(--line);border-radius:var(--radius);background:#fff}
.tech .num{display:inline-block;font-weight:800;color:var(--brand-red);font-size:14px;margin-bottom:8px}
.tech h3{margin:0 0 8px;font-size:16px;line-height:1.3}
.tech p{margin:0;font-size:14px;color:var(--muted);line-height:1.6}
.tech-of{margin:0 0 14px;font-size:14px;color:var(--muted)}
.spec-table td,.spec-table th{white-space:nowrap}
.spec-table td:nth-child(5){font-variant-numeric:tabular-nums;font-weight:600}
.spec-table tr.on{background:#FFF7D6}
'''


def tech_section(vers):
    """vers: list of (handle, label). Renders one technology block per version (toggled by data-tech)."""
    blocks = ''
    for k, (h, lab) in enumerate(vers):
        d = TECH.get(h, {})
        items = []
        for f in d.get('features', []):
            vi = TECH_VI.get(f['title'].lower())
            items.append(vi if vi else (f['title'], f['text']))
        if d.get('wide_rim'):
            items.append(WIDE_RIM_VI)
        if not items:
            continue
        arts = ''.join(f'<article><span class="num">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(x)}</p></article>' for i, (t, x) in enumerate(items))
        of = f'<p class="tech-of">Phiên bản <b>{E(lab)}</b></p>' if len(vers) > 1 else ''
        blocks += f'<div class="tech-v" data-tech="{k}"{" hidden" if k else ""}>{of}<div class="tech">{arts}</div></div>'
    if not blocks:
        return ''
    return f'<section class="pdp-sec" id="cong-nghe"><h2>Công nghệ</h2>{blocks}</section>'


def spec_section(vers, variants_of):
    """Spec chart from Vittoria (size, ETRTO, colour, weight) joined with SKUs. variants_of(handle) -> list of {size,color,sku}."""
    rows = ''
    multi = len(vers) > 1
    for k, (h, lab) in enumerate(vers):
        sku = {(v['size'], v['color']): v['sku'] for v in variants_of(h)}
        chart = TECH.get(h, {}).get('chart') or [{'Size': v['size'], 'Color': v['color']} for v in variants_of(h)]
        chart = [r for r in chart if r.get('Size', '') not in EXCLUDE_SIZES.get(h, ())]
        for r in chart:
            s, c = r.get('Size', ''), r.get('Color', '')
            code = sku.get((s, c), '')
            rows += (f'<tr data-sku="{code}" data-key="{E(s)}|{E(c)}">' + (f'<td>{E(lab)}</td>' if multi else '') +
                     f'<td>{E(s)}</td><td>{E(r.get("ETRTO", "—"))}</td><td>{E(COLOR_VI.get(c, c))}</td><td>{E(r.get("Weight", "—"))}</td><td>{code or "—"}</td></tr>')
    head = ('<th scope="col">Phiên bản</th>' if multi else '') + '<th scope="col">Kích thước</th><th scope="col">ETRTO</th><th scope="col">Màu</th><th scope="col">Trọng lượng</th><th scope="col">Mã sản phẩm</th>'
    return (f'<section class="pdp-sec" id="ma-san-pham"><h2>Bảng kỹ thuật</h2>'
            f'<div class="table-wrap"><table class="sku-table spec-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="geo-note">Dòng đang chọn được tô màu. Trọng lượng và ETRTO theo công bố của Vittoria; vui lòng liên hệ Spinlab để kiểm tra hàng có sẵn.</p></section>')


TECH_JS = "document.querySelectorAll('[data-tech]').forEach(el=>el.hidden=el.dataset.tech!=String(ver));"
