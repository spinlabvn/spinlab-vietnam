"""Polygon Tambora MY27 (gravel) data, typed in from the official spec sheets + geometry table
(WeTransfer 'product-update-q4-2026 / Tambora GA'). Merges into bikes.json. Usage: python3 tambora.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = 'img/tambora/'
SIZES = ['XXS', 'XS', 'S', 'M', 'L', 'XL']
GEO = {'sizes': SIZES, 'image': IMG + 'tambora-geometry.png', 'rows': [
    {'label': 'Height', 'unit': 'cm', 'values': ['151-161', '157-167', '164-174', '171-181', '178-188', '185-195']},
    {'label': 'Seat Tube Length (A)', 'unit': '', 'values': ['434', '454', '474', '494', '514', '524']},
    {'label': 'Seat Tube Angle (B)', 'unit': '', 'values': ['74.5', '74.5', '74.5', '74', '73.5', '73']},
    {'label': 'Effective Seat Tube Angle (C)', 'unit': '', 'values': ['74.5', '74.5', '74.5', '74', '73.5', '73']},
    {'label': 'Head Tube Length (D)', 'unit': '', 'values': ['87', '95', '101', '125', '139', '162']},
    {'label': 'Head Tube Angle (E)', 'unit': '', 'values': ['70', '70', '70.5', '70.5', '71', '71']},
    {'label': 'Effective Top Tube (F)', 'unit': '', 'values': ['516', '523', '529', '550', '570', '592']},
    {'label': 'Bb Height (G)', 'unit': '', 'values': ['283', '285', '288', '291', '291', '293']},
    {'label': 'Bb Offset (H)', 'unit': '', 'values': ['77', '75', '72', '69', '69', '67']},
    {'label': 'Chainstay Length (I)', 'unit': '', 'values': ['435'] * 6},
    {'label': 'Wheelbase (J)', 'unit': '', 'values': ['1022', '1030', '1033', '1052', '1062', '1080']},
    {'label': 'Frame Reach (K)', 'unit': '', 'values': ['365', '370', '375', '385', '395', '405']},
    {'label': 'Frame Stack (L)', 'unit': '', 'values': ['545', '550', '555', '575', '590', '610']},
    {'label': 'Standover Height (M)', 'unit': '', 'values': ['742', '759', '777', '779', '817', '903']}]}

FRAME = [['Frameset', 'CARBON GRAVEL FRAME, BB THREADED T47 76.75mm, UDH DROPOUT, INTERNAL ROUTING'],
         ['Fork', 'CARBON RIGID FORK, FULL CARBON, TAPERED 1-1/8" TO 1-1/2", FLAT MOUNT 160mm, THRU AXLE 12x100mm']]
FRONT_WHEEL_CARBON = [['Wheel Set', 'NOVATEC G29 DISC'],
    ['Rim', 'CARBON, H: 35mm, 24H FOR TYRE 622-54/76, TUBELESS READY'],
    ['Hub', None],
    ['Spokes', 'F: STAINLESS 14G NDS: 274 & DS: 276 W/ NIPPLE BRASS / R: STAINLESS 14G NDS: 274 & DS: 274 W/ NIPPLE BRASS']]
ALLOY_WHEEL = [['Wheel Set', 'ALLOY DOUBLE WALL 24H'],
    ['Rim', 'ALLOY DOUBLE WALL, H: 30mm, 24H FOR TYRE 622-44/76, TUBELESS READY'],
    ['Hub', 'F: NOVATEC D981SB, THRU AXLE 12x100mm, 24H, CENTER LOCK / R: NOVATEC D982SB, 12x142mm, 24H, CENTER LOCK'],
    ['Spokes', 'F: STAINLESS 14G NDS: 278 & DS: 280 W/ NIPPLE BRASS / R: STAINLESS 14G NDS: 278 & DS: 276 W/ NIPPLE BRASS']]


def wheels(carbon, rear_hub=None):
    if not carbon:
        return [list(r) for r in ALLOY_WHEEL]
    w = [list(r) for r in FRONT_WHEEL_CARBON]
    w[2][1] = f'F: NOVATEC D981SB, THRU AXLE 12x100mm, 24H, CENTER LOCK / R: {rear_hub}'
    return w


M = [
 dict(slug='tambora-9-axs', n='9', name='TAMBORA 9 AXS', color=('blue-orange', 'Blue / Orange', 'METALLIC DEEP BLUE GLOSS & ORANGE GLOSS', 'HOLOGRAPHIC & FADE BLACK'),
      sku_base='50401000', carbon=True,
      drive=[['Shifter', 'SRAM FORCE AXS E1, 1x13-SPEED'], ['Crank', 'SRAM FORCE XPLR AXS E1, 40T, 165mm (XXS, XS, S) / 170mm (M, L, XL)'],
             ['Cassette', 'SRAM FORCE XPLR XG-1371, 10-46T, XDR'], ['Rear Derailleur', 'SRAM FORCE XPLR AXS E1'],
             ['BB', 'SRAM DUB T47 WIDE 76.75mm ASYMMETRIC'], ['Chain', 'SRAM FORCE E1 W/ POWERLOCK']],
      cockpit=[['Saddle', 'FIZIK TERRA ARGO, ALLOY RAIL ø 7mm'], ['Seatpost', 'CARBON SEATPOST, D x L: 27.2 x 350mm, OFFSET: 0mm'],
               ['Handlebar', 'LINC CARBON INTEGRATED GRAVEL HANDLEBAR, W x EXT: 400x90mm (XXS) / 400x100mm (XS, S, M) / 420x110mm (L, XL), DROP: 115mm, REACH: 65mm'],
               ['Headset', 'TOKEN CHA1956D-36 W/ PREMIUM BEARING, IS 52/28.6 | IS 52/40']],
      rear_hub='NOVATEC D982 DUAL RATCHET SYSTEM, 12x142mm, 24H, CENTER LOCK FOR XDR DRIVER',
      tire='SCHWALBE G-ONE R PRO TAN WALL 700X50C (MAX 700X55C)',
      brake=[['Brake Lever', 'SRAM FORCE'], ['Brake Caliper', 'SRAM FORCE HYDRAULIC DISC, FLAT MOUNT'], ['Rotor', 'SRAM PACELINE 160mm, CENTER LOCK']]),
 dict(slug='tambora-7-di2', n='7', name='TAMBORA 7 Di2', color=('white-blue', 'White / Blue', 'WHITE GLOSS & METALLIC BLUE GLOSS', 'HOLOGRAM BLACK & FADE PURPLE'),
      sku_base='50400900', carbon=True,
      drive=[['Shifter', 'SHIMANO GRX ST-RX715, 1x12-SPEED, DUAL CONTROL SHIFTER'], ['Crank', 'SHIMANO FC-RX610, 40T, 165mm (XXS, XS, S) / 170mm (M, L, XL)'],
             ['Cassette', 'SHIMANO CS-M6100, 10-51T, MICROSPLINE'], ['Rear Derailleur', 'SHIMANO GRX RD-RX717'],
             ['BB', 'TOKEN T47 76.75mm'], ['Chain', 'KMC X-12']],
      cockpit=[['Saddle', 'LINC VOID, STEEL RAIL ø 7mm'], ['Seatpost', 'CARBON SEATPOST, D x L: 27.2 x 350mm, OFFSET: 0mm'],
               ['Handlebar', 'FSA ADVENTURE COMPACT AGX, W: 400mm (XXS, XS) / 420mm (S, M) / 440mm (L, XL), BB: 31.8mm, DROP: 125mm, REACH: 80mm'],
               ['Handlestem', 'FSA NS SMR-II, EXT: 90mm (XXS) / 100mm (XS, S, M) / 110mm (L, XL), BB: 31.8mm, R/D: 10degree'],
               ['Headset', 'FSA HS-PG-02 W/ SEALED BEARING, IS 52/28.6 | IS 52/40']],
      rear_hub='NOVATEC D982 DUAL RATCHET SYSTEM, TA 12x142mm, 24H, CENTER LOCK FOR MICROSPLINE',
      tire='SCHWALBE G-ONE R PRO TAN WALL 700X50C (MAX 700X55C)',
      brake=[['Brake Lever', 'SHIMANO BL-RS717'], ['Brake Caliper', 'SHIMANO GRX RX715 / BR-RX410 HYDRAULIC DISC, FLAT MOUNT'], ['Rotor', 'SHIMANO RT-CL700, 160mm, CENTER LOCK']]),
 dict(slug='tambora-6', n='6', name='TAMBORA 6', color=('red-black', 'Red / Black', 'CANDY RED GLOSS & METALLIC BLACK GLOSS', 'HOLOGRAPHIC & FADE BLACK'),
      sku_base='50400800', carbon=False,
      drive=[['Shifter', 'SHIMANO GRX ST-RX610, 2x12-SPEED, DUAL CONTROL SHIFTER'], ['Crank', 'SHIMANO FC-RX610, 46/30T, 165mm (XXS, XS, S) / 170mm (M, L, XL)'],
             ['Cassette', 'SHIMANO CS-HG710, 11-36T'], ['Front Derailleur', 'SHIMANO GRX FD-RX820'], ['Rear Derailleur', 'SHIMANO GRX RD-RX820'],
             ['BB', 'TOKEN T47 76.75mm'], ['Chain', 'KMC X-12']],
      cockpit=[['Saddle', 'LINC VOID, STEEL RAIL ø 7mm'], ['Seatpost', 'POLYGON EXPERT ALLOY, D x L: 27.2 x 350mm, OFFSET: 4mm'],
               ['Handlebar', 'FSA ADVENTURE COMPACT AGX, W: 400mm (XXS, XS) / 420mm (S, M) / 440mm (L, XL), BB: 31.8mm, DROP: 125mm, REACH: 80mm'],
               ['Handlestem', 'FSA NS SMR-II, EXT: 90mm (XXS) / 100mm (XS, S, M) / 110mm (L, XL), BB: 31.8mm, R/D: 10degree'],
               ['Headset', 'FSA HS-PG-02 W/ SEALED BEARING, IS 52/28.6 | IS 52/40']],
      tire='SCHWALBE G-ONE R 700X50C (MAX 700X55C)',
      brake=[['Brake Lever', 'SHIMANO ST-RX610'], ['Brake Caliper', 'SHIMANO GRX BR-RX410 HYDRAULIC DISC, FLAT MOUNT'], ['Rotor', 'SHIMANO RT-CL300, 160mm, CENTER LOCK']]),
 dict(slug='tambora-4', n='4', name='TAMBORA 4', color=('cream-black', 'Cream / Black', 'SOLID TAN GLOSS & METALLIC BLACK GLOSS', 'BRUSH POLISH BROWN & FADE BLACK'),
      sku_base='50400700', carbon=False,
      drive=[['Shifter', 'SHIMANO CUES ST-U6030, 2x10-SPEED, DUAL CONTROL SHIFTER'], ['Crank', 'SHIMANO CUES FC-U6030, 46/32T, 165mm (XXS, XS, S) / 170mm (M, L, XL)'],
             ['Cassette', 'SHIMANO CUES CS-LG300, 11-39T'], ['Front Derailleur', 'SHIMANO CUES FD-U6030'], ['Rear Derailleur', 'SHIMANO CUES RD-U6020'],
             ['BB', 'TOKEN T47 76.75mm'], ['Chain', 'KMC X-GLIDE']],
      cockpit=[['Saddle', 'LINC VOID, STEEL RAIL ø 7mm'], ['Seatpost', 'POLYGON EXPERT ALLOY, D x L: 27.2 x 350mm, OFFSET: 4mm'],
               ['Handlebar', 'POLYGON EXPERT ALLOY, W: 400mm (XXS, XS) / 420mm (S, M) / 440mm (L, XL), BB: 31.8mm, DROP: 130mm, REACH: 70mm'],
               ['Handlestem', 'POLYGON EXPERT ALLOY, EXT: 90mm (XXS) / 100mm (XS, S, M) / 110mm (L, XL), BB: 31.8mm, R/D: 7degree'],
               ['Headset', 'TOKEN CHA1956D-36 W/ PREMIUM BEARING, IS 52/28.6 | IS 52/40']],
      tire='DELIUM SPEEDX 700X45C (MAX 700X55C)',
      brake=[['Brake Lever', 'SHIMANO ST-U6030'], ['Brake Caliper', 'SHIMANO CUES BR-U6030 HYDRAULIC DISC, FLAT MOUNT'], ['Rotor', 'SHIMANO RT-CL300, 180mm, CENTER LOCK']]),
]

out = []
for m in M:
    cid, clabel, fcol, dcol = m['color']
    imgs = [f'{IMG}tambora-{m["n"]}-{v}.jpg' for v in ('p', 'rf', 'lf', 'rr')]
    sizes = [{'id': s.lower(), 'label': s} for s in SIZES]
    skus = {f'{cid}|{s.lower()}': f'{m["sku_base"]}{i+1}' for i, s in enumerate(SIZES)}
    wh = wheels(m['carbon'], m.get('rear_hub'))
    wh.insert(1, ['Tire', m['tire']])
    out.append(dict(slug=m['slug'], source='Polygon spec sheet MY27 (GA)', name=m['name'], headline='', tagline='Gravel | Carbon frame | 700C',
                    intro='', bike_type='GRAVEL', colors=[{'id': cid, 'label': clabel, 'images': imgs}], sizes=sizes, skus=skus,
                    feature_images=[imgs[1], imgs[2], imgs[3]], features=[],
                    specs=[{'group': 'Frameset', 'rows': FRAME + [['Frame Color', fcol], ['Decal Color', dcol]]},
                           {'group': 'Drivetrain', 'rows': m['drive']},
                           {'group': 'Cockpit', 'rows': m['cockpit']},
                           {'group': 'Wheel & Tire', 'rows': wh},
                           {'group': 'Brake', 'rows': m['brake']}],
                    geometry=GEO))
p = os.path.join(HERE, 'bikes.json')
b = json.load(open(p, encoding='utf-8'))
b = [x for x in b if x['slug'] not in {o['slug'] for o in out}] + out
json.dump(b, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'Tambora models merged;', len(b), 'bikes total')
