"""Polygon Cascade 3 / 4 / 5 (Leisure MTB hardtail), read from polygonbikes.com/us on 2026-10-21:
Cascade 4 and 5 are MY26; Cascade 3 is the newest Cascade 3 Polygon lists (MY22 photos, 27.5" S/M).
Merges the bikes into bikes.json and (re)builds the "Leisure" tab of xe-mtb.html.
    python3 cascade.py ../..
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..')
M = 'https://media.polygonbikes.com/wp-content/uploads/'
E = lambda s: html.escape(s, quote=True)

BASE = dict(headline='CASCADE: Lightweight & Durable Entry-Level Hardtail', bike_type='LEISURE',
            tagline='Leisure MTB | 100mm Travel | ALX Alloy | 29" or 27.5" Wheels',
            intro="The CASCADE is built for the rider who doesn't want to be limited by the pavement: lightweight alloy frame, 100mm suspension fork and disc brakes.",
            feature_images=[M + '2025/07/30121040/H1-Cascade-803x488.jpg'],
            features=[{'title': 'ALX frame', 'text': "Lightweight hydroformed ALX frame, manufactured in-house at Polygon's factory."}])
WS = [('27-5-xtra-small-us', 'XS (27.5″)'), ('27-5-small-us', 'S (27.5″)'), ('27-5-medium-us', 'M (27.5″)'), ('27-5-large-us', 'L (27.5″)'),
      ('29-small-us', 'S (29″)'), ('29-medium-us', 'M (29″)'), ('29-large-us', 'L (29″)'), ('29-xtra-large-us', 'XL (29″)')]
SIZES2 = [{'id': i, 'label': l} for i, l in WS]
COCKPIT45 = [['Saddle', 'BLACK STEEL ø7mm'], None, ['Handlebar', 'POLYGON SPORT W: 700MM, B: 31.8MM, R/D: 20MM'],
             ['Handlestem', 'POLYGON SPORT E: 40MM, B: 31.8MM, R/D: 7'], ['Headset', 'ZERO STACK W/ SEALED BEARING, ZS 44/28.6 | ZS 44/30']]
BRAKE45 = [['Brake Lever', 'SHIMANO MT200'], ['Brake Caliper', 'SHIMANO MT200 HYDRAULIC DISC'], ['Rotor', 'SHIMANO SM-RT10, 160mm']]


def geo(sizes, image, rows):
    labels = ['Height', 'Seat Tube Length (A)', 'Seat Tube Angle (B)', 'Effective Seat Tube Angle (C)', 'Head Tube Length (D)', 'Head Tube Angle (E)',
              'Effective Top Tube (F)', 'Bb Height (G)', 'Bb Offset (H)', 'Chainstay Length (I)', 'Wheelbase (J)', 'Frame Reach (K)', 'Frame Stack (L)', 'Standover Height (M)']
    return dict(sizes=sizes, image=image, rows=[{'label': l, 'unit': 'cm' if l == 'Height' else '', 'values': v.split()} for l, v in zip(labels, rows)])


GEO_IMG = M + '2025/07/31151317/GEOMETRY-DRAWING-CASCADE-FA-01-1024x724.png'
BIKES = [
    dict(BASE, slug='cascade-3', source='https://www.polygonbikes.com/us/cascade-3/', name='CASCADE 3',
         tagline='Leisure MTB | 100mm Travel | AL6 Alloy | 27.5" Wheels',
         colors=[{'id': 'red-black-us', 'label': 'Red Black', 'images': [M + '2022/09/24143203/PJ-MY-CASCADE-THREE-P.png', M + '2022/09/13150550/MY22-CASCADE-THREE-RF.png',
                                                                       M + '2022/09/13150548/MY22-CASCADE-THREE-RR.png', M + '2022/09/13150554/MY22-CASCADE-THREE-LF.png']},
                 {'id': 'blue-us', 'label': 'Blue', 'images': [M + '2022/09/13150552/MY22-CASCADE-THREE-P.png', M + '2022/09/13150554/MY22-CASCADE-THREE-LF.png',
                                                             M + '2022/09/13150548/MY22-CASCADE-THREE-RR.png']}],
         sizes=[{'id': 's-us', 'label': 'S'}, {'id': 'm-us', 'label': 'M'}],
         skus={'red-black-us|s-us': '502874004', 'red-black-us|m-us': '502874005', 'blue-us|s-us': '502874002', 'blue-us|m-us': '502874001'},
         specs=[{'group': 'Frameset', 'rows': [['Frameset', 'AL6 XC SPORT FRAME'], ['Fork', 'SUNTOUR XCE28 100mm TRAVEL'], ['Size', 'S, M'], ['Frame Color', 'RED BLACK / INDIGO BLUE'], ['Decal Color', 'CHARCOAL - BLACK']]},
                {'group': 'Drivetrain', 'rows': [['Shifter', 'SHIMANO ST-EF41, 3x7 SPEED TRIGGER'], ['Crank', 'STEEL CRANK 42x34x24T'], ['Cassette', 'SHIMANO MF-TZ500 7-SPEED 14-28T FREEWHEEL'],
                                                 ['Rear Derailleur', 'SHIMANO RD-TY300 6/7-SPEED DIRECT ATTACH'],
                                                 ['BB', 'CARTRIDGE BEARING W/ CAGED BEARING & 119mm SQUARE AXLE'], ['Chain', 'KMC HV-500'], ['Pedal', 'PP CAGE W/ REFLECTOR']]},
                {'group': 'Cockpit', 'rows': [['Saddle', 'MTB SADDLE, STEEL ø7mm'], ['Seatpost', 'ENTITY, 27.2x350mm'], ['Handlebar', 'STEEL, W: 680MM, B: 31.8MM, R/D: 40MM'],
                                              ['Handlestem', 'ENTITY ALLOY, E: 45MM, B: 31.8MM, R/D: 0'], ['Headset', 'ZERO STACK (ZS) THREADLESS, ZS 44/28.6 | 44/30']]},
                {'group': 'Wheel & Tire', 'rows': [['Wheel Set', 'ALLOY DOUBLE WALL'], ['Wheel Size', '27.5"'], ['Tire', '27.5"x2.1" 584x54'],
                                                   ['Rim', 'ALLOY DOUBLE WALL AV H: 20 584x20 32H FOR TIRE 584-28/62 DISC'],
                                                   ['Hub', 'F: ALLOY DISC BRAKE QR9x100mm 32H 6B / R: ALLOY DISC BRAKE QR9x135mm 32H 6B FOR FREEWHEEL'],
                                                   ['Spokes', 'STEEL 14G NDS:270 & DS:272 W/ UCP BRASS']]},
                {'group': 'Brake', 'rows': [['Brake Lever', 'SHIMANO ST-EF41'], ['Brake Caliper', 'TEKTRO MD-M280 MECHANICAL DISC'], ['Rotor', 'TEKTRO TR160-24 160mm 6-BOLTS']]}],
         geometry=geo(['S', 'M'], 'https://www.polygonbikes.com/wp-content/themes/polygon2021/assets/images/heist-x7-geo.png',
                      ['152-165 162-175', '406 456', '73 73', '73 73', '100 105', '69 69', '565 585', '303 303', '47 47', '430 429', '1065.7 1086.1', '383.7 402.2', '593.1 597.8', '700 742'])),
    dict(BASE, slug='cascade-4', source='https://www.polygonbikes.com/us/cascade-4-2/', name='CASCADE 4',
         colors=[{'id': 'green-latte-us', 'label': 'Green Latte', 'images': [M + '2025/10/24131851/MY25-CASCADE-FOUR-G2-P.png', M + '2025/07/30093430/MY26-CASCADE-FOUR-DECAL-RIMS-RR.png',
                                                                           M + '2025/07/30093219/MY26-CASCADE-FOUR-DECAL-RIMS-RF.png', M + '2025/07/30093137/MY26-CASCADE-FOUR-DECAL-RIMS-LF.png']},
                 {'id': 'charcoal', 'label': 'Charcoal', 'images': [M + '2025/07/30091822/MY26-CASCADE-FOUR-DECAL-RIMS-P.png', M + '2025/07/30093219/MY26-CASCADE-FOUR-DECAL-RIMS-RF.png']}],
         sizes=SIZES2,
         skus=dict(**{f'green-latte-us|{i}': s for (i, _), s in zip(WS, ['503670001', '503670002-en', '503670003-en', '503670004-en', '503671001', '503671002', '503671003', '503671004'])},
                   **{f'charcoal|{i}': s for (i, _), s in zip(WS, ['503441001', '503441002', '503441003', '503441004', '503442001', '503442002', '503442003', '503442004'])}),
         specs=[{'group': 'Frameset', 'rows': [['Frameset', 'ALX XC SPORT FRAME'], ['Fork', 'SUNTOUR XCM 32 100MM TRAVEL'], ['Size', 'XS, S, M, L (27.5") / S, M, L, XL (29")'],
                                               ['Frame Color', 'GREEN LATTE / CHARCOAL CHROME'], ['Decal Color', 'WHITE - BLACK']]},
                {'group': 'Drivetrain', 'rows': [['Shifter', 'SHIMANO CUES SL-U4010, 1x9 RAPID FIRE'], ['Crank', 'PROWHEEL C10Y-NW, 36T'], ['Cassette', 'SHIMANO CUES CS-LG300, 11-46T'],
                                                 ['Rear Derailleur', 'SHIMANO CUES RD-U4000GS'], ['BB', 'SQUARE BB, 68mm'], ['Chain', 'KMC X-GLIDE'], ['Pedal', 'ONE PIECE PP BODY']]},
                {'group': 'Cockpit', 'rows': [r if r else ['Seatpost', 'POLYGON SPORT 27.2 x 350mm'] for r in COCKPIT45]},
                {'group': 'Wheel & Tire', 'rows': [['Wheel Set', 'ALLOY DOUBLE WALL'], ['Wheel Size', '27.5" / 29"'], ['Tire', '27.5" / 29" x 2.25"'], ['Rim', 'ALLOY DOUBLE WALL'],
                                                   ['Hub', 'F: ALLOY, 100mm 32H QR / R: ALLOY, 135mm 32H QR'],
                                                   ['Spokes', '27.5": 14G STAINLESS NDS:270mm / DS:272mm · 29": 14G STAINLESS NDS:290mm / DS:292mm, 12mm NIPPLE BRASS']]},
                {'group': 'Brake', 'rows': BRAKE45}],
         geometry=geo(['XS (27.5″)', 'S (27.5″)', 'M (27.5″)', 'L (27.5″)', 'S (29″)', 'M (29″)', 'L (29″)'], GEO_IMG,
                      ['145-155 155-165 165-175 175-185 155-165 165-175 175-185', '360 390 430 460 390 430 460', '75 75 75 75 75 75 75', '75 74 74 74 75 75 74',
                       '110 115 120 125 90 95 100', '68 67 68 68 67 68 68', '538 561 582 603 566 585 604', '310 310 310 310 304 303 303', '-45 -45 -45 -45 -69 -69 -69',
                       '440 439 439 439 455 454 454', '1085 1108 1129 1151 1122 1142 1161', '380 400 420 440 400 420 440', '596 601 606 610 620 624 629', '684 703 734 755 709 736 759'])),
    dict(BASE, slug='cascade-5', source='https://www.polygonbikes.com/us/2026-cascade-5-mountain-bike/', name='CASCADE 5',
         colors=[{'id': 'brown-us', 'label': 'Brown', 'images': [M + '2025/07/29154405/MY26-CASCADE-FIVE-P.png', M + '2025/07/29154635/MY26-CASCADE-FIVE-RF.png',
                                                               M + '2025/07/29154510/MY26-CASCADE-FIVE-LF.png', M + '2025/07/29155848/MY26-CASCADE-FIVE-RR.png']},
                 {'id': 'white-us', 'label': 'White', 'images': [M + '2025/11/14130258/MY26-CASCADE-FIVE-G2-P.png', M + '2025/11/14130215/MY26-CASCADE-FIVE-G2-RF.png',
                                                               M + '2025/11/14130342/MY26-CASCADE-FIVE-G2-LF.png']}],
         sizes=SIZES2,
         skus=dict(**{f'brown-us|{i}': s for (i, _), s in zip(WS, ['503443001', '503443002', '503443003', '503443004', '503444001', '503444002', '503444003', '503444004'])},
                   **{f'white-us|{i}': s for (i, _), s in zip(WS, ['503672001', '503665001', '503665002', '503665003', '503673001', '503673002', '503673003', '503673004'])}),
         specs=[{'group': 'Frameset', 'rows': [['Frameset', 'ALX XC SPORT FRAME'], ['Fork', 'SUNTOUR XCM 32 100MM TRAVEL'], ['Size', 'XS, S, M, L (27.5") / S, M, L, XL (29")'],
                                               ['Frame Color', 'BROWN METALLIC / WHITE'], ['Decal Color', 'WHITE - BLACK']]},
                {'group': 'Drivetrain', 'rows': [['Shifter', 'SHIMANO CUES SL-U6000, 1x10 RAPID FIRE'], ['Crank', 'PROWHEEL CHARM, 36T'], ['Cassette', 'SHIMANO CUES CS-LG300, 11-48T'],
                                                 ['Rear Derailleur', 'SHIMANO CUES RD-U6000GS'], ['BB', 'PROWHEEL TWO PIECE BB'], ['Chain', 'KMC X-GLIDE'], ['Pedal', 'ONE PIECE PP BODY']]},
                {'group': 'Cockpit', 'rows': [r if r else ['Seatpost', 'ALLOY SEATPOST 27.2x350mm'] for r in COCKPIT45]},
                {'group': 'Wheel & Tire', 'rows': [['Wheel Set', 'ALLOY DOUBLE WALL'], ['Wheel Size', '27.5" / 29"'], ['Tire', 'DELI 27.5" / 29" x 2.25"'],
                                                   ['Rim', 'ALLOY DOUBLE WALL H: 20mm W: 21mm 32H'], ['Hub', 'F: ALLOY, 100mm 32H QR / R: ALLOY, 135mm 32H QR'],
                                                   ['Spokes', '14G STAINLESS, 12mm NIPPLE BRASS']]},
                {'group': 'Brake', 'rows': BRAKE45}],
         geometry=geo([l for _, l in WS], GEO_IMG,
                      ['145-155 155-165 165-175 175-185 155-165 165-175 175-185 185-195', '360 390 430 460 390 430 460 491', '75 75 75 75 75 75 75 75', '75 75 74 75 73 74 75 75',
                       '110 115 120 125 90 95 99 110', '69 70 68 69 68 69 68 68', '539 561 581 603 565 585 604 624', '310 310 309 310 304 303 303 304',
                       '-45 -45 -45 -45 -69 -69 -69 -69', '440 440 440 440 455 455 454 455', '1085 1108 1129 1151 1122 1142 1161 1182', '380 400 420 440 400 420 440 453',
                       '596 601 606 610 620 624 629 638', '646 704 734 756 709 736 759 780'])),
]

p = os.path.join(HERE, 'bikes.json')
b = json.load(open(p, encoding='utf-8'))
b = [x for x in b if x['slug'] not in {o['slug'] for o in BIKES}] + BIKES
json.dump(b, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- Leisure tab on xe-mtb.html ----
sys.path.insert(0, HERE)
from vi import VI  # noqa: E402
DESC = {'cascade-5': 'Shimano CUES 1x10 · Phanh đĩa dầu', 'cascade-4': 'Shimano CUES 1x9 · Phanh đĩa dầu', 'cascade-3': 'Shimano 3x7 · Bánh 27.5"'}
cards = ''
for o in sorted(BIKES, key=lambda o: o['slug'], reverse=True):
    if o['slug'] in VI:
        cards += (f'<article class="p-card"><div class="p-img"><img src="{E(o["colors"][0]["images"][0])}" alt="Polygon {E(o["name"])}" loading="lazy"></div>'
                  f'<div class="p-body"><span class="p-brand">Polygon · Cascade</span><h3 class="p-name"><a class="stretch" href="{VI[o["slug"]]["file"]}.html">{E(o["name"])}</a></h3>'
                  f'<p class="p-desc">{E(DESC[o["slug"]])}</p><span class="p-price">1.980.000₫</span></div></article>')
TAB = '        <button role="tab" id="tab-leisure" aria-controls="panel-leisure" aria-selected="false" tabindex="-1">Leisure</button>\n'
PANEL = (f'      <div class="mtb-panel" role="tabpanel" id="panel-leisure" aria-labelledby="tab-leisure" hidden>\n'
         f'        <p class="mtb-intro">Xe địa hình phổ thông: đi phố hằng ngày, dạo đường mòn cuối tuần — dễ làm quen, bền bỉ.</p>\n'
         f'        <section class="road-group"><div class="rg-head"><div><h2>Cascade</h2><p class="rg-sub">Leisure MTB · Hardtail nhôm · Phuộc 100mm</p></div>'
         f'<p class="rg-desc">Hardtail nhập môn nhẹ và bền, phuộc nhún 100mm, phanh đĩa, bánh 27.5" hoặc 29" theo chiều cao người đạp.</p></div>'
         f'<div class="grid">{cards}</div></section>\n      </div>\n')
f = os.path.join(D, 'xe-mtb.html')
s = open(f, encoding='utf-8').read()
s = s.replace(TAB, '')
s = re.sub(r'      <div class="mtb-panel" role="tabpanel" id="panel-leisure".*?\n      </div>\n', '', s, flags=re.S)
if cards:
    s = s.replace('Dirt Jump</button>\n', 'Dirt Jump</button>\n' + TAB, 1)
    i = s.index('<div class="mtb-panel" role="tabpanel" id="panel-dj"')
    s = s[:i] + PANEL.lstrip() + '      ' + s[i:]
open(f, 'w', encoding='utf-8').write(s)
print(len(BIKES), 'Cascade merged;', len(b), 'bikes total; Leisure tab', cards.count('<article'), 'xe')
