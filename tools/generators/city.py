"""Polygon City - Hybrid: Heist 2 / 5 / 7 (MY27) and Path 2 / 3 / 4 (MY26), read from polygonbikes.com/us
(2026-10-21) and merged into bikes.json. Heist 5's page has no geometry table: it shares the Heist frame
(ALX HYBRID 700C), so the Heist 2/7 table is used. Obvious scrape artefacts in Polygon's spec text are cleaned.
    python3 city.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = 'https://media.polygonbikes.com/wp-content/uploads/'
SIZES = [{'id': s, 'label': s[:-3].upper()} for s in ('s-us', 'm-us', 'l-us', 'xl-us')]

HEIST = dict(headline='HEIST: For Urban Adventures', tagline='Hybrid | ALX Alloy frame | 3 Available Builds', bike_type='HYBRID',
             intro="The Polygon Heist is your all-access past to urban adventures. It's a city hybrid that’s fast enough to win the sprint to the office and tough enough to take the dirt path home.",
             feature_images=[f'{MEDIA}2026/04/23161748/Heist-Feature-1.jpg', f'{MEDIA}2026/04/23161755/Heist-Feature-2.jpg', f'{MEDIA}2026/04/23161802/Heist-Feature-3.jpg',
                             f'{MEDIA}2026/04/23161808/Heist-Feature-4.jpg', f'{MEDIA}2026/04/23161812/Heist-Feature-5.jpg'],
             features=[{'title': 'Rider Focussed Geometry', 'text': 'Lightweight alloy frame, heads-up position and flat bar.'},
                       {'title': 'Front Suspension', 'text': 'Suspension fork for potholes, gravel and rough tracks.'},
                       {'title': '1x Drivetrain', 'text': 'Simplified 1x gearing: less weight and maintenance.'},
                       {'title': 'Hydraulic Disc Brakes', 'text': 'One-finger stopping power.'},
                       {'title': 'Fast-Rolling Adventure Tires', 'text': '700x45c tires.'}])
HEIST_GEO = dict(sizes=['S', 'M', 'L', 'XL'], image=f'{MEDIA}2026/03/05051123/GE-HEIST-1024x824.jpg', rows=[
    {'label': 'Height', 'unit': 'cm', 'values': ['155-165', '165-175', '175-185', '185-195']},
    {'label': 'Seat Tube Length (A)', 'unit': '', 'values': ['405', '432', '470', '516']},
    {'label': 'Seat Tube Angle (B)', 'unit': '', 'values': ['74', '74', '74', '74']},
    {'label': 'Effective Seat Tube Angle (C)', 'unit': '', 'values': ['74', '74', '74', '74']},
    {'label': 'Head Tube Length (D)', 'unit': '', 'values': ['90', '100', '100', '110']},
    {'label': 'Head Tube Angle (E)', 'unit': '', 'values': ['71', '71', '71', '71']},
    {'label': 'Effective Top Tube (F)', 'unit': '', 'values': ['556', '579', '599', '622']},
    {'label': 'Bb Height (G)', 'unit': '', 'values': ['294', '294', '294', '294']},
    {'label': 'Bb Offset (H)', 'unit': '', 'values': ['70', '70', '70', '70']},
    {'label': 'Chainstay Length (I)', 'unit': '', 'values': ['440', '440', '440', '440']},
    {'label': 'Wheelbase (J)', 'unit': '', 'values': ['1050', '1073', '1093', '1116']},
    {'label': 'Frame Reach (K)', 'unit': '', 'values': ['385', '405', '425', '445']},
    {'label': 'Frame Stack (L)', 'unit': '', 'values': ['597', '607', '607', '616']},
    {'label': 'Standover Height (M)', 'unit': '', 'values': ['696', '711', '737', '777']}])
HEIST_COCKPIT = [['Saddle', 'SELLE ROYAL A059H, RAIL: STEEL ø7mm'], ['Handlebar', 'POLYGON SPORT, W: 680mm, BB: 31.8mm, R/D: 0mm, B: 6degree']]
HEIST_RIM = 'F: ALLOY DOUBLE WALL H: 20mm W: 21mm 32H FOR TYRE 622, R: ALLOY DOUBLE WALL H: 20mm W: 21mm 32H FOR TYRE 622'
HEIST_SPOKES = 'F: 14G STAINLESS NDS: 290mm DS: 290mm 12MM NIPPLE BRASS, R: 14G STAINLESS NDS: 290mm DS: 290mm 12MM NIPPLE BRASS'

PATH = dict(headline='PATH: Flat-Bar for Urban Adventures', tagline='Urban | ALX Alloy frame | Alloy fork', bike_type='DAILY',
            intro='The Polygon PATH combines the speed of a road bike with the upright visibility of a flat-bar commuter.',
            feature_images=[f'{MEDIA}2026/06/02161709/Path-Feature-1.jpg', f'{MEDIA}2026/06/02161715/Path-Feature-2.jpg',
                            f'{MEDIA}2026/06/02161719/Path-Feature-3.jpg', f'{MEDIA}2026/06/02161724/Path-Feature-4.jpg'],
            features=[{'title': 'ALX Urban Frame & Fork', 'text': 'Lightweight hydroformed aluminium frame.'},
                      {'title': 'Versatile Drivetrain & Disc Brakes', 'text': 'Shimano drivetrain and disc brakes.'},
                      {'title': 'Comfortable & Fast', 'text': '700c wheels and high-volume tires.'},
                      {'title': 'Utility Ready', 'text': 'Mounts for fenders, racks and bottles.'}])


def path_geo(head, bbh, wb, reach, stack, so):
    return dict(sizes=['S', 'M', 'L', 'XL'], image='https://www.polygonbikes.com/wp-content/themes/polygon2021/assets/images/heist-x7-geo.png', rows=[
        {'label': 'Height', 'unit': 'cm', 'values': ['150-163', '163-175', '175-188', '188-195']},
        {'label': 'Seat Tube Length (A)', 'unit': '', 'values': ['430', '460', '490', '520']},
        {'label': 'Seat Tube Angle (B)', 'unit': '', 'values': ['74.5', '74.5', '74', '73.5']},
        {'label': 'Effective Seat Tube Angle (C)', 'unit': '', 'values': ['74.5', '74.5', '74', '73.5']},
        {'label': 'Head Tube Length (D)', 'unit': '', 'values': head},
        {'label': 'Head Tube Angle (E)', 'unit': '', 'values': ['70.5', '70.5', '71', '71']},
        {'label': 'Effective Top Tube (F)', 'unit': '', 'values': ['530', '548', '572', '596']},
        {'label': 'Bb Height (G)', 'unit': '', 'values': [bbh] * 4},
        {'label': 'Bb Offset (H)', 'unit': '', 'values': ['72'] * 4},
        {'label': 'Chainstay Length (I)', 'unit': '', 'values': ['440'] * 4},
        {'label': 'Wheelbase (J)', 'unit': '', 'values': wb},
        {'label': 'Frame Reach (K)', 'unit': '', 'values': reach},
        {'label': 'Frame Stack (L)', 'unit': '', 'values': stack},
        {'label': 'Standover Height (M)', 'unit': '', 'values': so}])


PATH23_GEO = path_geo(['95', '125', '155', '185'], '284', ['1028', '1048', '1064', '1083'], ['379', '390', '399', '409'],
                      ['543', '571', '603', '630'], ['705', '734', '766', '794'])
PATH4_GEO = path_geo(['115', '145', '175', '205'], '286', ['1033', '1053', '1069', '1088'], ['380', '390', '400', '410'],
                     ['541', '570', '600', '628'], ['703', '735', '763', '793'])


def bike(slug, src, name, base, color, imgs, sku, frame, drive, cockpit, wheel, brake, geo):
    cid, clabel, fcol, dcol = color
    d = dict(slug=slug, source=f'https://www.polygonbikes.com/us/{src}/', name=name, **base)
    d.update(colors=[{'id': cid, 'label': clabel, 'images': [MEDIA + i for i in imgs]}], sizes=SIZES,
             skus={f'{cid}|{s["id"]}': f'{sku}{i + 1:03d}' for i, s in enumerate(SIZES)},
             specs=[{'group': 'Frameset', 'rows': frame + [['Size', 'S, M, L, XL'], ['Frame Color', fcol], ['Decal Color', dcol]]},
                    {'group': 'Drivetrain', 'rows': drive}, {'group': 'Cockpit', 'rows': cockpit},
                    {'group': 'Wheel & Tire', 'rows': wheel}, {'group': 'Brake', 'rows': brake}], geometry=geo)
    return d


M = [
    bike('heist-2', '2027-heist-2-hybrid-bike', 'HEIST 2', HEIST, ('purple-us', 'Purple', 'PURPLE', 'SILVER BLACK'),
         ['2026/03/04160207/MY26-HEIST-2-P.png', '2026/03/04160250/MY26-HEIST-2-RF.png', '2026/03/04160125/MY26-HEIST-2-LF.png'], '503755',
         [['Frameset', 'ALX HYBRID 700C'], ['Fork', 'SUNTOUR NEX 63MM TRAVEL, COIL SPRING, PRELOAD ADJUSTER']],
         [['Shifter', 'SHIMANO ALTUS SL-M315, 1x8 SPEED, RAPID FIRE SHIFTER'], ['Crank', 'PROWHEEL C10Y-NW 36T'], ['Cassette', 'SHIMANO ACERA CS-HG400, 11-45T'],
          ['Rear Derailleur', 'SHIMANO ESSA RD-U2000'], ['BB', 'SQUARE BB 68X119mm'], ['Chain', 'KMC Z-8.3'], ['Pedal', 'PP PEDAL']],
         HEIST_COCKPIT[:1] + [['Seatpost', 'POLYGON SPORT, DxL: 27.2 x 350mm']] + HEIST_COCKPIT[1:] +
         [['Handlestem', 'POLYGON SPORT, E: 75mm, BB: 31.8mm, R/D: 10degree'], ['Headset', 'ZERO STACK W/ CAGED BEARING, ZS 44/28.6 | ZS 56/30']],
         [['Wheel Set', 'ALLOY WHEELS'], ['Wheel Size', '700C'], ['Tire', 'KENDA K-1172 700X45C'], ['Rim', HEIST_RIM],
          ['Hub', 'F: ALLOY HUB QR M9x100mm 32H, R: ALLOY HUB QR M9X135mm 32H'], ['Spokes', HEIST_SPOKES]],
         [['Brake Lever', 'TEKTRO HD-M280'], ['Brake Caliper', 'TEKTRO HD-M280 HYDRAULIC DISC'], ['Rotor', 'TEKTRO TR-160-52 160mm']],
         dict(HEIST_GEO, rows=[dict(r, values=v) if r['label'] in ('Head Tube Length (D)', 'Frame Reach (K)', 'Standover Height (M)') else r
                               for r in HEIST_GEO['rows'] for v in [{'Head Tube Length (D)': ['90', '99', '100', '110'], 'Frame Reach (K)': ['384', '405', '425', '445'],
                                                                     'Standover Height (M)': ['697', '711', '737', '777']}.get(r['label'])]])),
    bike('heist-5', '2027-heist-5-hybrid-bike', 'HEIST 5', HEIST, ('blue-us', 'Blue', 'BLUE', 'BLACK'),
         ['2026/03/04160459/MY26-HEIST-5-P.png', '2026/03/04160624/MY26-HEIST-5-RR.png', '2026/03/04160416/MY26-HEIST-5-LF.png'], '503756',
         [['Frameset', 'ALX HYBRID 700C'], ['Fork', 'SUNTOUR NVX32-5TA 63MM TRAVEL, COIL SPRING, HYDRAULIC SPEED LOCKOUT']],
         [['Crank', 'PROWHEEL CHARM 36T'], ['Cassette', 'SHIMANO CUES CS-LG300, 11-48T'], ['Rear Derailleur', 'SHIMANO CUES RD-U6000'],
          ['BB', 'PROWHEEL 2 PIECES'], ['Chain', 'KMC X-GLIDE'], ['Pedal', 'PP PEDAL']],
         HEIST_COCKPIT[:1] + [['Seatpost', 'POLYGON SPORT, DxL: 27.2 x 350mm']] + HEIST_COCKPIT[1:] +
         [['Handlestem', 'POLYGON SPORT, E: 75mm, BB: 31.8mm, R/D: 10degree'], ['Headset', 'ZERO STACK W/ CAGED BEARING S.H., ZS 44/28.6 | ZS 56/40']],
         [['Wheel Set', 'ALLOY WHEELS'], ['Wheel Size', '700C'], ['Tire', 'WTB RIDDLER 700X45C'], ['Rim', HEIST_RIM],
          ['Hub', 'F: ALLOY QR HUB M9x100mm 32H, R: ALLOY QR HUB M9X135mm 32H'], ['Spokes', HEIST_SPOKES]],
         [['Brake Lever', 'SHIMANO MT200'], ['Brake Caliper', 'SHIMANO MT200 HYDRAULIC DISC'], ['Rotor', 'SHIMANO SM-RT26 180mm']], HEIST_GEO),
    bike('heist-7', '2027-heist-7-hybrid-bike', 'HEIST 7', HEIST, ('cream-us', 'Cream', 'CREAM', 'BLACK'),
         ['2026/03/04160756/MY26-HEIST-7-P.png', '2026/03/04160840/MY26-HEIST-7-RF.png', '2026/03/04160711/MY26-HEIST-7-LF.png'], '503757',
         [['Frameset', 'ALX HYBRID 700C'], ['Fork', 'SUNTOUR NVX32-5TA 63MM TRAVEL, AIR SPRING, HYDRAULIC SPEED LOCKOUT']],
         [['Shifter', 'SHIMANO DEORE SL-M6100, 1x12 SPEED, RAPID FIRE SHIFTER'], ['Crank', 'PROWHEEL DMG-FD04S 36T'], ['Cassette', 'SHIMANO DEORE CS-M6100, 10-51T'],
          ['Rear Derailleur', 'SHIMANO DEORE RD-M6100'], ['BB', 'PROWHEEL 2-PIECES'], ['Chain', 'KMC X12'], ['Pedal', 'PP PEDAL']],
         HEIST_COCKPIT[:1] + [['Seatpost', 'ALLOY SUSPENSION SEATPOST, DxL: 27.2x340mm']] + HEIST_COCKPIT[1:] +
         [['Handlestem', 'POLYGON SPORT, E: 75mm, BB: 31.8mm, R/D: ADJUSTABLE'], ['Headset', 'ZERO STACK W/ CAGED BEARING, ZS 44/28.6 | ZS 56/40']],
         [['Wheel Set', 'ALLOY WHEELS'], ['Wheel Size', '700C'], ['Tire', 'WTB RIDDLER 700X45C'], ['Rim', 'ALLOY DOUBLE WALL H: 20mm W: 21mm 32H FOR TYRE 622'],
          ['Hub', 'F: SHIMANO QC 400 M9X100mm 32H, R: SHIMANO QC 500 MICROSPLINE M9X135mm 32H'],
          ['Spokes', 'F: 14G STAINLESS NDS: 290mm DS: 292mm 12MM NIPPLE BRASS, R: 14G STAINLESS NDS: 292mm DS: 290mm 12MM NIPPLE BRASS']],
         [['Brake Lever', 'SHIMANO MT200'], ['Brake Caliper', 'SHIMANO MT200 HYDRAULIC DISC'], ['Rotor', 'SHIMANO SM-RT10 180mm']], HEIST_GEO),
    bike('path-2', '2026-path-2-city-bike', 'PATH 2', PATH, ('metalic-blue-us', 'Metallic Blue', 'METALLIC BLUE', 'BLACK'),
         ['2025/10/23113629/MY25-PATH-2-KENDA-TIRE-P.png', '2025/10/23113754/MY25-PATH-2-KENDA-TIRE-RR.png', '2025/10/23114401/MY25-PATH-2-KENDA-TIRE-LF.png'], '503347',
         [['Frameset', 'ALX URBAN FITNESS'], ['Fork', 'ALLOY RIGID']],
         [['Shifter', 'SHIMANO ALTUS M315, 1x8 SPEED RAPIDFIRE'], ['Crank', 'ALLOY, 42T'], ['Cassette', 'SHIMANO HG400, 11-45T'], ['Rear Derailleur', 'SHIMANO ESSA U2000 GS'],
          ['BB', 'SQUARE BB, 68mm'], ['Chain', 'KMC Z-8.3'], ['Pedal', 'ONE PIECE PP FLAT']],
         [['Saddle', 'LINC EASE'], ['Seatpost', 'POLYGON SPORT, DxL: 27.2x350mm, OFFSET: 15mm, SEAT CLAMP: 31.8mm BOLT'],
          ['Handlebar', 'POLYGON SPORT, W: 680mm, BB: 31.8mm, R/D: 0mm, B: 6degree'], ['Handlestem', 'POLYGON SPORT, EXT: 75mm, BB: 31.8mm, R/D: 41mm'],
          ['Headset', 'THREADLESS SEMI-INTEGRATED, IS 44/28.6 | IS 44/30']],
         [['Wheel Set', 'ALLOY DOUBLE WALL 32H'], ['Wheel Size', '700C'], ['Tire', 'KENDA 700x40C 622x40'], ['Rim', 'ALLOY DOUBLE WALL FV H:20 622X21 32H FOR TYRE 622-28/62 DISC'],
          ['Hub', 'F: ALLOY DISC BRAKE M9x100mm 32H 6 BOLT / R: ALLOY DISC BRAKE 10x135mm 32H 6 BOLT'], ['Spokes', 'F: STAINLESS 14G NDS:290 & DS:290 / R: STAINLESS 14G NDS:290 & DS:290']],
         [['Brake Lever', 'TEKTRO TS-325A'], ['Brake Caliper', 'TEKTRO M280 DISC'], ['Rotor', 'TEKTRO TR 160-52, 160mm']], PATH23_GEO),
    bike('path-3', 'path-3-2', 'PATH 3', PATH, ('green-us', 'Olive Green', 'OLIVE GREEN', 'BLACK'),
         ['2025/04/21163703/MY25-PATH-3-P.png', '2025/04/21163859/MY25-PATH-3-RR.png', '2025/04/21163803/MY25-PATH-3-RF.png'], '503348',
         [['Frameset', 'ALX URBAN FITNESS'], ['Fork', 'ALLOY RIGID']],
         [['Shifter', 'SHIMANO CUES U4000, 1x9-SPEED RAPIDFIRE'], ['Crank', 'PROWHEEL, 42T'], ['Cassette', 'SHIMANO CUES LG300 11-46T'], ['Rear Derailleur', 'SHIMANO CUES U4000'],
          ['BB', 'SQUARE BB 68mm'], ['Chain', 'KMC X-GLIDE'], ['Pedal', 'ONE PIECE PP FLAT']],
         [['Saddle', 'SELLE ROYAL EASE'], ['Seatpost', 'POLYGON SPORT, DxL: 27.2 x 350mm'], ['Handlebar', 'POLYGON SPORT, W: 680mm, BB: 31.8mm, R/D: 0mm, B: 6degree'],
          ['Handlestem', 'POLYGON SPORT, EXT: 60mm (S, M) / 80mm (L, XL), BB: 31.8mm, R/D: 41mm'], ['Headset', 'THREADLESS SEMI-INTEGRATED, IS 44/28.6 | IS 44/30']],
         [['Wheel Set', 'ALLOY DOUBLE WALL 32H'], ['Wheel Size', '700C'], ['Tire', 'VEE SPEEDSTER 700x40C 622x40'], ['Rim', 'ALLOY DOUBLE WALL FV H:20 622X21 32H FOR TYRE 622-28/62 DISC'],
          ['Hub', 'F: ALLOY DISC BRAKE M9x100mm 32H CENTERLOCK / R: ALLOY DISC BRAKE 10x135mm 32H CENTERLOCK'], ['Spokes', 'F: STAINLESS 14G NDS:292 & DS:292 / R: STAINLESS 14G NDS:292 & DS:292']],
         [['Brake Lever', 'SHIMANO BL-MT200'], ['Brake Caliper', 'SHIMANO MT200 HYDRAULIC DISC'], ['Rotor', 'SHIMANO SM-RT10, 160mm CENTERLOCK']], PATH23_GEO),
    bike('path-4', 'path-4', 'PATH 4', dict(PATH, tagline='Urban | ALX Alloy frame | Carbon fork'), ('chameleon-purple-us', 'Chameleon Purple', 'CHAMELEON GREEN PURPLE', 'BLACK'),
         ['2025/04/22074759/MY25-PATH-4-P.png', '2025/04/21164203/MY25-PATH-4-RR.png', '2025/04/21164100/MY25-PATH-4-RF.png'], '503349',
         [['Frameset', 'ALX URBAN FITNESS'], ['Fork', 'CARBON RIGID']],
         [['Shifter', 'SHIMANO TIAGRA SL-4700, 1x10-SPEED RAPIDFIRE PLUS'], ['Crank', 'PROWHEEL OUNCE, 48T'], ['Cassette', 'SHIMANO TIAGRA CS-HG500-10'],
          ['Rear Derailleur', 'SHIMANO TIAGRA RD-4700'], ['BB', 'PROWHEEL 68mm'], ['Chain', 'KMC X10'], ['Pedal', 'ONE PIECE PP FLAT']],
         [['Saddle', 'SELLE ROYAL EASE'], ['Seatpost', 'POLYGON EXPERT, DxL: 27.2 x 350mm'], ['Handlebar', 'POLYGON EXPERT, W: 680mm, BB: 31.8mm, R/D: 0mm, B: 6degree'],
          ['Handlestem', 'POLYGON EXPERT, EXT: 60mm (S, M) / 80mm (L, XL), BB: 31.8mm, R/D: 41mm'], ['Headset', 'FSA TH-881 W/ SEALED BEARING, IS 42/28.6 | IS 52/40']],
         [['Wheel Set', 'ALLOY DOUBLE WALL 24H'], ['Wheel Size', '700C'], ['Tire', 'VEE GOODIE GOODIE 700x35C 622x35'], ['Rim', 'ALLOY DOUBLE WALL FV H: 30 622X19 24H FOR TYRE 622-28/62 DISC'],
          ['Hub', 'F: ALLOY DISC BRAKE 12x100mm 24H / R: ALLOY DISC BRAKE 12x142mm 24H CENTERLOCK'], ['Spokes', 'F: STAINLESS 14G NDS:276 & DS:280 / R: STAINLESS 14G NDS:278 & DS:278']],
         [['Brake Lever', 'SHIMANO BL-MT200'], ['Brake Caliper', 'SHIMANO BR-MT200 HYDRAULIC DISC'], ['Rotor', 'SHIMANO SM-RT26, 160mm']], PATH4_GEO),
]

p = os.path.join(HERE, 'bikes.json')
b = json.load(open(p, encoding='utf-8'))
b = [x for x in b if x['slug'] not in {o['slug'] for o in M}] + M
json.dump(b, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(M), 'City - Hybrid models merged;', len(b), 'bikes total')
