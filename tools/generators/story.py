"""Story Bike — Continue Pro (24" street trial) and Curvet C2.0 Ultra (26" dirt jump). Only facts visible in the supplied photos are recorded;
no official spec sheet was provided. Merges into bikes.json. Usage: python3 story.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = 'img/story/'

BIKE = dict(
    slug='story-continue-pro', source='Story Bike — ảnh do Spinlab cung cấp', name='Continue Pro',
    headline='', tagline='Street trial | 24"', intro='', bike_type='TRIAL',
    colors=[{'id': 'yellow', 'label': 'Vàng', 'images': [IMG + f for f in ('continue-yellow.jpg', 'continue-yellow-2.jpg', 'continue-yellow-3.jpg', 'continue-yellow-4.jpg')]},
            {'id': 'silver', 'label': 'Bạc', 'images': [IMG + f for f in ('continue-silver.jpg', 'continue-silver-2.jpg', 'continue-silver-3.jpg')]},
            {'id': 'purple', 'label': 'Tím', 'images': [IMG + f for f in ('continue-purple.jpg', 'continue-purple-2.jpg', 'continue-purple-3.jpg')]}],
    sizes=[{'id': '24', 'label': '24"'}], skus={},
    feature_images=[IMG + 'continue-lifestyle-1.jpg', IMG + 'continue-silver-3.jpg', IMG + 'continue-detail-1.jpg'],
    features=[],
    specs=[{'group': 'Wheel & Tire', 'rows': [['Wheel Size', '24"'], ['Tire', 'MAXXIS HOLY ROLLER 24"'], ['Rim', 'STORY']]},
           {'group': 'Drivetrain', 'rows': [['Gearing', 'SINGLE SPEED (1 TỐC ĐỘ)'], ['Crank', 'STORY']]},
           {'group': 'Brake', 'rows': [['Brakes', 'PHANH ĐĨA TRƯỚC / SAU']]},
           {'group': 'Other', 'rows': [['Frame Color', 'VÀNG / BẠC / TÍM'], ['Details', 'ĐANG CẬP NHẬT (vật liệu khung, trọng lượng, bộ phanh, giò đĩa)']]}],
    geometry=None)

p = os.path.join(HERE, 'bikes.json')
b = json.load(open(p, encoding='utf-8'))
b = [x for x in b if x['slug'] != BIKE['slug']] + [BIKE]
json.dump(b, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('merged', BIKE['slug'], '—', len(b), 'bikes')

# ---- Story Curvet C2.0 Ultra (26" dirt jump) — from Story's spec table (Ultra column) ----
CURVET = dict(
    slug='story-curvet-c2-ultra', source='Bảng thông số Story Curvet C2.0 (cột Ultra)', name='Curvet C2.0 Ultra',
    headline='', tagline='Dirt jump | 26"', intro='', bike_type='DIRT JUMP',
    colors=[{'id': 'black', 'label': 'Đen nhám', 'images': [IMG + f for f in ('curvet-black.jpg', 'curvet-black-2.jpg')]},
            {'id': 'white', 'label': 'Trắng', 'images': [IMG + f for f in ('curvet-white.jpg', 'curvet-white-2.jpg', 'curvet-pumptrack.jpg', 'curvet-jump.jpg')]}],
    sizes=[{'id': '26', 'label': '26"'}], skus={},
    feature_images=[IMG + 'curvet-pumptrack.jpg', IMG + 'curvet-jump.jpg', IMG + 'curvet-white-2.jpg'],
    features=[],
    specs=[{'group': 'Frameset', 'rows': [['Frameset', 'STORY CURVET 2.0 26", 6061 ALLOY'], ['Headset', '41.8/52mm TAPERED'],
                                          ['Dropout', '135x10mm, INTEGRATED CNC FISH-TAIL DROPOUTS'], ['Brake Mount', 'B-POST'],
                                          ['Fork', 'X-FUSION SLANT RC 34, TAPERED, 100mm TRAVEL, 100x15mm THRU AXLE / QR'],
                                          ['Frame Color', 'TRẮNG / ĐEN / HỒNG / XANH STARRY / CAM ĐỎ HUỲNH QUANG']]},
           {'group': 'Cockpit', 'rows': [['Handlebar', 'STORY ALLOY, RISE 35mm, W: 740mm'], ['Handlestem', 'STORY CNC, EXT: 35mm, BB: 31.8mm'],
                                        ['Grips', 'STORY SINGLE-SIDE LOCK-ON'], ['Saddle', 'STORY, CR-MO RAIL'], ['Seatpost', 'STORY CNC LIGHTWEIGHT ALLOY']]},
           {'group': 'Wheel & Tire', 'rows': [['Hub', 'F: STORY 100x15mm THRU AXLE / R: STORY 120-CLICK SINGLE SPEED CASSETTE HUB'],
                                             ['Rim', 'STORY 35mm, HIGH-STRENGTH ANODIZED, RIVETED'], ['Spokes', '14G x 258mm STAINLESS'],
                                             ['Tire', 'MAXXIS DTH 26x2.3, SKINWALL']]},
           {'group': 'Drivetrain', 'rows': [['Crank', 'STORY 7050 DUB29'], ['Chainring', 'STORY 7075 GXP 32T NARROW-WIDE'], ['Cog', 'STORY 17T HIGH-STRENGTH CASSETTE COG'],
                                           ['Chain', 'KMC Z1eHX NARROW'], ['Chain Tensioner', 'INTEGRATED CRESCENT TENSIONER BOLTS'], ['Pedal', 'SG NYLON, BEARING']]},
           {'group': 'Brake', 'rows': [['Brakes', 'KHÔNG KÈM PHANH — TUỲ CHỌN: SHIMANO MT200, MAGURA MT30, MAGURA MT5, MAGURA MT (BẢN GIỚI HẠN)']]}],
    geometry={'sizes': ['26"'], 'image': '', 'rows': [
        {'label': 'Head Tube Angle', 'unit': '', 'values': ['70']},
        {'label': 'Chainstay Length', 'unit': '', 'values': ['377']},
        {'label': 'Bb Offset', 'unit': '', 'values': ['-14']},
        {'label': 'Wheelbase', 'unit': '', 'values': ['1027']},
        {'label': 'Frame Reach', 'unit': '', 'values': ['410']}]})

b = json.load(open(p, encoding='utf-8'))
b = [x for x in b if x['slug'] != CURVET['slug']] + [CURVET]
json.dump(b, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('merged', CURVET['slug'], '—', len(b), 'bikes')
