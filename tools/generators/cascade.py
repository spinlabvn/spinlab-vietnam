"""Polygon Cascade 3 / 4 / 5 (Leisure MTB hardtail), read from polygonbikes.com/us on 2026-10-21:
Cascade 3 (polygonbikes.com/cascade-3, re-read 2026-10-23), 4 and 5 are MY26. Spinlab sells size XS with 27.5" wheels, S-XL with 29".
Merges the bikes into bikes.json and (re)builds the Cascade group in the Cross Country tab of xe-mtb.html.
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
# Spinlab sells every Cascade as XS with 27.5" wheels and S / M / L / XL with 29" wheels
SALE = ['XS (27.5″)', 'S (29″)', 'M (29″)', 'L (29″)', 'XL (29″)']
SIZES2 = [{'id': i, 'label': l} for i, l in WS if l in SALE]
SIZE_ROW = 'XS (27.5") / S, M, L, XL (29")'
WHEEL_ROW = '27.5" (XS) / 29" (S–XL)'
TIRE_ROW = '27.5" (XS) / 29" (S–XL)'
COCKPIT45 = [['Saddle', 'BLACK STEEL ø7mm'], None, ['Handlebar', 'POLYGON SPORT W: 700MM, B: 31.8MM, R/D: 20MM'],
             ['Handlestem', 'POLYGON SPORT E: 40MM, B: 31.8MM, R/D: 7'], ['Headset', 'ZERO STACK W/ SEALED BEARING, ZS 44/28.6 | ZS 44/30']]
BRAKE45 = [['Brake Lever', 'SHIMANO MT200'], ['Brake Caliper', 'SHIMANO MT200 HYDRAULIC DISC'], ['Rotor', 'SHIMANO SM-RT10, 160mm']]


def geo(sizes, image, rows):
    labels = ['Height', 'Seat Tube Length (A)', 'Seat Tube Angle (B)', 'Effective Seat Tube Angle (C)', 'Head Tube Length (D)', 'Head Tube Angle (E)',
              'Effective Top Tube (F)', 'Bb Height (G)', 'Bb Offset (H)', 'Chainstay Length (I)', 'Wheelbase (J)', 'Frame Reach (K)', 'Frame Stack (L)', 'Standover Height (M)']
    return dict(sizes=sizes, image=image, rows=[{'label': l, 'unit': 'cm' if l == 'Height' else '', 'values': v.split()} for l, v in zip(labels, rows)])


def geo8(rows):
    """Geometry given for all 8 Polygon sizes (WS order), keeping only the sizes Spinlab sells."""
    keep = [k for k, (_, l) in enumerate(WS) if l in SALE]
    return geo(SALE, GEO_IMG, [' '.join(v.split()[k] for k in keep) for v in rows])


GEO_IMG = M + '2025/07/31151317/GEOMETRY-DRAWING-CASCADE-FA-01-1024x724.png'
BIKES = [
    dict(BASE, slug='cascade-3', source='https://www.polygonbikes.com/cascade-3/', name='CASCADE 3',
         colors=[{'id': 'cream', 'label': 'Cream', 'images': [M + '2025/10/24133041/MY25-CASCADE-THREE-G2-P.png']},  # Polygon's other angles show the red bike
                 {'id': 'red', 'label': 'Red', 'images': [M + '2025/07/29213652/MY26-CASCADE-THREE-P.png', M + '2025/07/29214318/MY26-CASCADE-THREE-RR.png',
                                                       M + '2025/07/29214123/MY26-CASCADE-THREE-lf.png', M + '2025/07/29213803/MY26-CASCADE-THREE-RF.png']}],
         sizes=SIZES2,
         skus=dict(**{f'cream|{i}': s for (i, _), s in zip(WS, ['503668001', '503668002', '503668003', '503668004', '503669001', '503669002', '503669003', '503669004'])},
                   **{f'red|{i}': s for (i, _), s in zip(WS, ['503682001', '503439001', '503439002', '503439003', '503440001', '503440002', '503440003', '503683001'])}),
         specs=[{'group': 'Frameset', 'rows': [['Frameset', 'ALX XC SPORT FRAME'], ['Fork', 'SUNTOUR XCE 28 100mm TRAVEL'], ['Size', SIZE_ROW],
                                               ['Frame Color', 'CREAM / RED'], ['Decal Color', 'WHITE - BLACK']]},
                {'group': 'Drivetrain', 'rows': [['Shifter', 'SHIMANO ALTUS SL-M315, 1x8-SPEED TRIGGER'], ['Crank', 'PROWHEEL C10Y, 36T'], ['Cassette', 'SHIMANO CS-HG400, 11-45T'],
                                                 ['Rear Derailleur', 'SHIMANO ESSA RD-U2000'], ['BB', 'SQUARE BB, 68mm'], ['Chain', 'KMC Z-8.3'], ['Pedal', 'ONE PIECE PP BODY']]},
                {'group': 'Cockpit', 'rows': [r if r else ['Seatpost', 'ALLOY SEATPOST 27.2x350mm'] for r in COCKPIT45]},
                {'group': 'Wheel & Tire', 'rows': [['Wheel Set', 'ALLOY DOUBLE WALL'], ['Wheel Size', WHEEL_ROW], ['Tire', TIRE_ROW + ' x 2.25"'], ['Rim', 'ALLOY DOUBLE WALL'],
                                                   ['Hub', 'F: ALLOY, 100mm 32H QR / R: ALLOY, 135mm 32H QR'],
                                                   ['Spokes', '27.5": 14G STAINLESS NDS:270mm / DS:272mm · 29": 14G STAINLESS NDS:290mm / DS:292mm, 12mm NIPPLE BRASS']]},
                {'group': 'Brake', 'rows': [['Brake Lever', 'HYDRAULIC DISC BRAKE'], ['Brake Caliper', 'HYDRAULIC DISC BRAKE'], ['Rotor', '6-BOLTS 160mm']]}],
         # Polygon lists S/M/L 27.5" and S/M/L 29" for Cascade 3; XS and XL come from Cascade 4 / 5 (same ALX XC Sport frame)
         geometry=geo8(['145-155 155-165 165-175 175-185 155-165 165-175 175-185 185-195', '360 390 430 460 390 430 460 491', '75 75 75 75 75 75 75 75',
                        '75 75 75 73 74 75 75 75', '110 115 120 125 90 95 100 110', '68 68 68 68 68 68 68 68', '538 561 582 603 566 585 604 624',
                        '310 310 310 310 304 303 304 304', '-45 -45 -45 -45 -69 -69 -69 -69', '440 440 440 440 455 455 455 455',
                        '1085 1108 1129 1151 1142 1142 1161 1182', '380 400 420 440 420 420 440 453', '596 601 606 610 624 624 629 638',
                        '684 703 733 756 737 737 759 780'])),
    dict(BASE, slug='cascade-4', source='https://www.polygonbikes.com/us/cascade-4-2/', name='CASCADE 4',
         colors=[{'id': 'green-latte-us', 'label': 'Green Latte', 'images': [M + '2025/10/24131851/MY25-CASCADE-FOUR-G2-P.png', M + '2025/07/30093430/MY26-CASCADE-FOUR-DECAL-RIMS-RR.png',
                                                                           M + '2025/07/30093219/MY26-CASCADE-FOUR-DECAL-RIMS-RF.png', M + '2025/07/30093137/MY26-CASCADE-FOUR-DECAL-RIMS-LF.png']},
                 {'id': 'charcoal', 'label': 'Charcoal', 'images': [M + '2025/07/30091822/MY26-CASCADE-FOUR-DECAL-RIMS-P.png', M + '2025/07/30093219/MY26-CASCADE-FOUR-DECAL-RIMS-RF.png']}],
         sizes=SIZES2,
         skus=dict(**{f'green-latte-us|{i}': s for (i, _), s in zip(WS, ['503670001', '503670002-en', '503670003-en', '503670004-en', '503671001', '503671002', '503671003', '503671004'])},
                   **{f'charcoal|{i}': s for (i, _), s in zip(WS, ['503441001', '503441002', '503441003', '503441004', '503442001', '503442002', '503442003', '503442004'])}),
         specs=[{'group': 'Frameset', 'rows': [['Frameset', 'ALX XC SPORT FRAME'], ['Fork', 'SUNTOUR XCM 32 100MM TRAVEL'], ['Size', SIZE_ROW],
                                               ['Frame Color', 'GREEN LATTE / CHARCOAL CHROME'], ['Decal Color', 'WHITE - BLACK']]},
                {'group': 'Drivetrain', 'rows': [['Shifter', 'SHIMANO CUES SL-U4010, 1x9 RAPID FIRE'], ['Crank', 'PROWHEEL C10Y-NW, 36T'], ['Cassette', 'SHIMANO CUES CS-LG300, 11-46T'],
                                                 ['Rear Derailleur', 'SHIMANO CUES RD-U4000GS'], ['BB', 'SQUARE BB, 68mm'], ['Chain', 'KMC X-GLIDE'], ['Pedal', 'ONE PIECE PP BODY']]},
                {'group': 'Cockpit', 'rows': [r if r else ['Seatpost', 'POLYGON SPORT 27.2 x 350mm'] for r in COCKPIT45]},
                {'group': 'Wheel & Tire', 'rows': [['Wheel Set', 'ALLOY DOUBLE WALL'], ['Wheel Size', WHEEL_ROW], ['Tire', TIRE_ROW + ' x 2.25"'], ['Rim', 'ALLOY DOUBLE WALL'],
                                                   ['Hub', 'F: ALLOY, 100mm 32H QR / R: ALLOY, 135mm 32H QR'],
                                                   ['Spokes', '27.5": 14G STAINLESS NDS:270mm / DS:272mm · 29": 14G STAINLESS NDS:290mm / DS:292mm, 12mm NIPPLE BRASS']]},
                {'group': 'Brake', 'rows': BRAKE45}],
         # Polygon has no XL (29") column for Cascade 4; it comes from Cascade 5 (same ALX XC Sport frame)
         geometry=geo8(['145-155 155-165 165-175 175-185 155-165 165-175 175-185 185-195', '360 390 430 460 390 430 460 491', '75 75 75 75 75 75 75 75', '75 74 74 74 75 75 74 75',
                        '110 115 120 125 90 95 100 110', '68 67 68 68 67 68 68 68', '538 561 582 603 566 585 604 624', '310 310 310 310 304 303 303 304', '-45 -45 -45 -45 -69 -69 -69 -69',
                        '440 439 439 439 455 454 454 455', '1085 1108 1129 1151 1122 1142 1161 1182', '380 400 420 440 400 420 440 453', '596 601 606 610 620 624 629 638', '684 703 734 755 709 736 759 780'])),
    dict(BASE, slug='cascade-5', source='https://www.polygonbikes.com/us/2026-cascade-5-mountain-bike/', name='CASCADE 5',
         colors=[{'id': 'white-us', 'label': 'White', 'images': [M + '2025/11/14130258/MY26-CASCADE-FIVE-G2-P.png', M + '2025/11/14130215/MY26-CASCADE-FIVE-G2-RF.png',
                                                               M + '2025/11/14130342/MY26-CASCADE-FIVE-G2-LF.png']},
                 {'id': 'brown-us', 'label': 'Brown', 'images': [M + '2025/07/29154405/MY26-CASCADE-FIVE-P.png', M + '2025/07/29154635/MY26-CASCADE-FIVE-RF.png',
                                                               M + '2025/07/29154510/MY26-CASCADE-FIVE-LF.png', M + '2025/07/29155848/MY26-CASCADE-FIVE-RR.png']}],
         sizes=SIZES2,
         skus=dict(**{f'brown-us|{i}': s for (i, _), s in zip(WS, ['503443001', '503443002', '503443003', '503443004', '503444001', '503444002', '503444003', '503444004'])},
                   **{f'white-us|{i}': s for (i, _), s in zip(WS, ['503672001', '503665001', '503665002', '503665003', '503673001', '503673002', '503673003', '503673004'])}),
         specs=[{'group': 'Frameset', 'rows': [['Frameset', 'ALX XC SPORT FRAME'], ['Fork', 'SUNTOUR XCM 32 100MM TRAVEL'], ['Size', SIZE_ROW],
                                               ['Frame Color', 'WHITE / BROWN METALLIC'], ['Decal Color', 'WHITE - BLACK']]},
                {'group': 'Drivetrain', 'rows': [['Shifter', 'SHIMANO CUES SL-U6000, 1x10 RAPID FIRE'], ['Crank', 'PROWHEEL CHARM, 36T'], ['Cassette', 'SHIMANO CUES CS-LG300, 11-48T'],
                                                 ['Rear Derailleur', 'SHIMANO CUES RD-U6000GS'], ['BB', 'PROWHEEL TWO PIECE BB'], ['Chain', 'KMC X-GLIDE'], ['Pedal', 'ONE PIECE PP BODY']]},
                {'group': 'Cockpit', 'rows': [r if r else ['Seatpost', 'ALLOY SEATPOST 27.2x350mm'] for r in COCKPIT45]},
                {'group': 'Wheel & Tire', 'rows': [['Wheel Set', 'ALLOY DOUBLE WALL'], ['Wheel Size', WHEEL_ROW], ['Tire', 'DELI ' + TIRE_ROW + ' x 2.25"'],
                                                   ['Rim', 'ALLOY DOUBLE WALL H: 20mm W: 21mm 32H'], ['Hub', 'F: ALLOY, 100mm 32H QR / R: ALLOY, 135mm 32H QR'],
                                                   ['Spokes', '14G STAINLESS, 12mm NIPPLE BRASS']]},
                {'group': 'Brake', 'rows': BRAKE45}],
         geometry=geo8(
                      ['145-155 155-165 165-175 175-185 155-165 165-175 175-185 185-195', '360 390 430 460 390 430 460 491', '75 75 75 75 75 75 75 75', '75 75 74 75 73 74 75 75',
                       '110 115 120 125 90 95 99 110', '69 70 68 69 68 69 68 68', '539 561 581 603 565 585 604 624', '310 310 309 310 304 303 303 304',
                       '-45 -45 -45 -45 -69 -69 -69 -69', '440 440 440 440 455 455 454 455', '1085 1108 1129 1151 1122 1142 1161 1182', '380 400 420 440 400 420 440 453',
                       '596 601 606 610 620 624 629 638', '646 704 734 756 709 736 759 780'])),
]

from latest_colors import latest  # noqa: E402
SOLD = {i for i, l in WS if l in SALE}
for _b in BIKES:
    latest(_b)
    _b['skus'] = {k: v for k, v in _b['skus'].items() if k.split('|')[1] in SOLD}
p = os.path.join(HERE, 'bikes.json')
b = json.load(open(p, encoding='utf-8'))
b = [x for x in b if x['slug'] not in {o['slug'] for o in BIKES}] + BIKES
json.dump(b, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- Cascade group in the Cross Country panel of xe-mtb.html ----
sys.path.insert(0, HERE)
from vi import VI  # noqa: E402
DESC = {'cascade-5': 'Shimano CUES 1x10 · Phanh đĩa dầu', 'cascade-4': 'Shimano CUES 1x9 · Phanh đĩa dầu', 'cascade-3': 'Shimano 1x8 · Phanh đĩa dầu'}
cards = ''
for o in sorted(BIKES, key=lambda o: o['slug'], reverse=True):
    if o['slug'] in VI:
        cards += (f'<article class="p-card"><div class="p-img"><img src="{E(o["colors"][0]["images"][0])}" alt="Polygon {E(o["name"])}" loading="lazy"></div>'
                  f'<div class="p-body"><span class="p-brand">Polygon · Cascade</span><h3 class="p-name"><a class="stretch" href="{VI[o["slug"]]["file"]}.html">{E(o["name"])}</a></h3>'
                  f'<p class="p-desc">{E(DESC[o["slug"]])}</p><span class="p-price">1.980.000₫</span></div></article>')
GROUP = ('<section class="road-group"><div class="rg-head"><div><h2>Cascade</h2><p class="rg-sub">XC hardtail phổ thông · Nhôm · Phuộc 100mm</p></div>'
         '<p class="rg-desc">Hardtail nhập môn nhẹ và bền, phuộc nhún 100mm, phanh đĩa; size XS bánh 27.5", size S–XL bánh 29".</p></div>'
         f'<div class="grid">{cards}</div></section>')
f = os.path.join(D, 'xe-mtb.html')
s = open(f, encoding='utf-8').read()
# remove the old Leisure tab/panel and any previous Cascade group
s = s.replace('        <button role="tab" id="tab-leisure" aria-controls="panel-leisure" aria-selected="false" tabindex="-1">Leisure</button>\n', '')
s = re.sub(r'      <div class="mtb-panel" role="tabpanel" id="panel-leisure".*?\n      </div>\n', '', s, flags=re.S)
s = re.sub(r'\s*<section class="road-group"><div class="rg-head"><div><h2>Cascade</h2>.*?</section>', '', s, flags=re.S)
if cards:   # last group of the Cross Country panel
    a = s.index('id="panel-xc"')
    z = s.index('\n      </div>', a)
    s = s[:z] + '\n        ' + GROUP + s[z:]
open(f, 'w', encoding='utf-8').write(s)
print(len(BIKES), 'Cascade merged;', len(b), 'bikes total; Cross Country', cards.count('<article'), 'xe')
