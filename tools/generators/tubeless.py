"""Vittoria tubeless accessories (Universal sealant + Air-Liner Light): detail pages + tubeless.html listing.
Shell = vittoria-tattoo.html (tire PDP). Usage: python3 tubeless.py <design-preview dir>"""
import sys, os, re, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stock
E = html.escape
D = sys.argv[1]
CDN = 'https://cdn.shopify.com/s/files/1/0800/0549/7120/files/'
ZALO = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg'

P = [
 dict(file='vittoria-universal-sealant.html', group='sealant', name='Universal Tubeless Sealant', short='Keo tự vá Universal',
      cat='Keo tự vá', tag='Không amoniac', headline='Một loại keo cho mọi chiếc xe',
      desc='Vá tức thì lỗ thủng tới 7mm',
      intro=['Keo tự vá Universal Tubeless Sealant của Vittoria được phát triển để phục vụ mọi người đạp xe, dù bạn đi road, gravel hay MTB. Bí quyết nằm ở gốc dung dịch đủ loãng để nhanh chóng tìm và bịt kín cả những lỗ thủng nhỏ nhất.',
             'Bên trong dung dịch là các hạt vảy kết dính lại với nhau để bịt những lỗ thủng lớn hơn. Trong thử nghiệm của Vittoria, keo vá tức thì lỗ thủng tới 7mm và giữ hơi tốt tới 1.200 km. Công thức không chứa amoniac nên không làm hại lốp và dùng được cùng miếng lót Air-Liner.'],
      fit=['Road', 'Gravel', 'MTB', 'Dùng cùng Air-Liner'],
      imgs=['universal-tire-sealant-family', 'vittoria-Universal-Tire-Sealant-80ml', 'vittoria-Universal-Tire-Sealant-250ml', 'vittoria-Universal-Tire-Sealant-500ml'],
      opt='Dung tích',
      features=[('Vá nhanh lỗ nhỏ', 'Gốc dung dịch loãng len vào và bịt kín những lỗ thủng nhỏ nhất trong tích tắc.'),
                ('Hạt vảy bịt lỗ lớn', 'Các hạt vảy lơ lửng trong keo kết lại với nhau, vá tức thì lỗ thủng tới 7mm.'),
                ('Giữ hơi tới 1.200 km', 'Khả năng giữ hơi xuất sắc theo thử nghiệm của Vittoria.'),
                ('Không chứa amoniac', 'Không làm hại lốp; an toàn khi dùng cùng miếng lót Air-Liner.'),
                ('Cho mọi loại xe', 'Một công thức cho road, gravel và MTB — không cần chọn keo riêng cho từng xe.')],
      cols=['Dung tích', 'Mã sản phẩm'],
      rows=[('80ml', '1AA00095'), ('150ml', '1AA00096'), ('250ml', '1AA00097'), ('500ml', '1AA00098'), ('1000ml', '1AA00099'), ('5 lít', '1AA00458')],
      note='Lượng keo cần dùng tùy cỡ lốp — liên hệ Spinlab để được tư vấn.',
      faq=[('Cần bao nhiêu keo cho một lốp?', 'Lượng keo phụ thuộc cỡ lốp: lốp road cần ít, lốp gravel và MTB bản to cần nhiều hơn. Đội kỹ thuật Spinlab sẽ tư vấn lượng phù hợp với lốp của bạn.'),
           ('Có dùng chung với Air-Liner được không?', 'Được. Keo Universal không chứa amoniac nên an toàn với miếng lót Air-Liner; Vittoria yêu cầu chỉ dùng keo không amoniac cùng Air-Liner.'),
           ('Nên chọn dung tích nào?', 'Chai 80ml và 150ml tiện mang theo hoặc châm thêm cho một bộ lốp; chai 500ml và 1000ml phù hợp cho xưởng hoặc người dùng nhiều xe.')]),
 dict(file='vittoria-air-liner-light-xc.html', group='air-liner', name='Air-Liner Light XC', short='Air-Liner Light XC',
      cat='Air-Liner Light', tag='MTB · XC', headline='Lót tubeless siêu nhẹ cho tốc độ XC',
      desc='Chỉ 55g · Run-flat tới 25 km',
      intro=['Air-Liner Light XC mang lại toàn bộ khả năng chống thủng kiểu “rắn cắn” (pinch-flat) và tăng hiệu năng lốp của Air-Liner MTB, nhưng chỉ bằng một phần nhỏ trọng lượng — nhẹ hơn cả lượng keo cần để lắp lốp. Được phát triển cùng các đội đua World Cup.',
             'Miếng lót gia cố thành lốp trong khi mặt lốp vẫn “chạy trên hơi”: lốp bám địa hình mượt mà, đạp bốc, không bị gập khi vào cua. Khi lốp bị nén mạnh, Air-Liner cứng dần để chống va vành; khi lốp xì hơi, miếng lót nở ra giúp bạn tiếp tục đi tới 25 km nếu chạy cẩn thận.'],
      fit=['Marathon', 'Cross country', 'Down-country'],
      imgs=['air-liner-light-tire-insert-1', 'air-liner-light-tire-insert-2', 'air-liner-light-xc'],
      opt='Kích thước',
      features=[('Siêu nhẹ 55g', 'Giảm khối lượng quay phía trên tanh lốp, giữ cảm giác lốp nhanh và bốc.'),
                ('Chống thủng rắn cắn & xì tanh', 'Loại bỏ pinch-flat và hiện tượng “ợ hơi” ở tanh lốp khi chạy áp suất thấp.'),
                ('Bảo vệ vành', 'Cứng dần khi bị nén, chống va vành khi gặp cạnh đá vuông hoặc đáp đất mạnh.'),
                ('Ổn định khi vào cua', 'Gia cố thành lốp để lốp không gập khi chịu lực ngang.'),
                ('Run-flat tới 25 km', 'Khi lốp xì hơi, miếng lót nở ra lấp khoảng trống để bạn về đích.')],
      cols=['Cỡ lốp', 'Lòng vành trong', 'Trọng lượng', 'Van đi kèm', 'Xe điện', 'Mã sản phẩm'],
      rows=[('29x2.1-2.4', '25-30mm', '55g', '40mm', 'Không', '1AA00412')],
      note='Mỗi hộp gồm 1 miếng lót và 1 van Vittoria Multiway Tubeless 40mm. Chỉ dùng với lốp tubeless, van multiway và keo không amoniac.',
      faq=[('Air-Liner Light XC hợp với vành nào?', 'Bánh 29 inch, lòng vành trong 25–30mm, lốp bản 2.1–2.4 inch.'),
           ('Có dùng cho xe đạp điện được không?', 'Không. Vittoria công bố Air-Liner Light XC không dành cho e-bike.'),
           ('Cần chuẩn bị gì khi lắp?', 'Lốp tubeless, van multiway (có sẵn trong hộp) và keo không amoniac như Vittoria Universal Sealant. Spinlab có thể hỗ trợ lắp đặt.')]),
 dict(file='vittoria-air-liner-light-gravel.html', group='air-liner', name='Air-Liner Light Gravel', short='Air-Liner Light Gravel',
      cat='Air-Liner Light', tag='Gravel', headline='Êm hơn, bám hơn trên đường sỏi',
      desc='40–45g · 650b & 700c',
      intro=['Air-Liner Light Gravel là vòng lót siêu nhẹ mang màu xanh đặc trưng của Air-Liner. Có hai cỡ bánh 650b và 700c, dùng cho lốp gravel bản 37–50mm.',
             'Miếng lót tăng độ êm cho những ngày đạp dài, bảo vệ vành khỏi va đập, tăng độ ổn định khi vào cua và nở ra như run-flat khi lốp bị thủng. Chỉ dùng với lốp tubeless và van multiway.'],
      fit=['Gravel', 'Bikepacking', 'Đua gravel'],
      imgs=['air-liner-light-gravel-tire-insert-1', 'air-liner-light-gravel', 'air-liner-gravel-light-packaging'],
      opt='Kích thước',
      features=[('Êm ái hơn', 'Tăng độ êm cho những ngày dài trên yên, chạy áp suất thấp để bám đường hơn.'),
                ('Bảo vệ vành', 'Bảo vệ vành khỏi va đập, giảm nguy cơ thủng kiểu rắn cắn.'),
                ('Ổn định khi vào cua', 'Tăng lực đỡ thành lốp khi ôm cua — đi nhanh hơn, tự tin hơn.'),
                ('Run-flat', 'Lớp bọt nở ra khi lốp bị thủng để bạn tiếp tục hành trình.')],
      cols=['Cỡ lốp', 'Lòng vành', 'Trọng lượng', 'Van đi kèm', 'Mã sản phẩm'],
      rows=[('650b x 42-50', '23-28mm', '40g', '60mm', '1AA00499'), ('700c x 37-40', '21-27mm', '40g', '60mm', '1AA00546'), ('700c x 42-50', '23-28mm', '45g', '60mm', '1AA00495')],
      note='Mỗi hộp gồm 1 miếng lót và 1 van Vittoria Multiway Tubeless. Mẹo tháo lốp: xả hết hơi và để ít nhất 1 giờ trước khi tháo để miếng lót trả lại độ căng.',
      faq=[('Chọn cỡ nào cho xe của tôi?', 'Chọn theo cỡ bánh (650b hoặc 700c) và bản lốp: 700c x 37–40, 700c x 42–50 hoặc 650b x 42–50. Kiểm tra thêm lòng vành trong bảng kỹ thuật.'),
           ('Có khó tháo lốp không?', 'Hãy xả hết hơi và để lốp ít nhất 1 giờ trước khi tháo; dùng cần tháo lốp Vittoria và bộ dụng cụ Air-Liner Tool Kit sẽ dễ hơn.'),
           ('Dùng keo gì đi kèm?', 'Chỉ dùng keo không amoniac, ví dụ Vittoria Universal Sealant.')]),
 dict(file='vittoria-air-liner-light-road.html', group='air-liner', name='Air-Liner Light Road', short='Air-Liner Light Road',
      cat='Air-Liner Light', tag='Road', headline='Lót tubeless siêu nhẹ cho tốc độ road',
      desc='29–40g · Run-flat tới 50 km',
      intro=['Air-Liner Light Road là miếng lót tubeless siêu nhẹ được phát triển để tối đa hiệu năng đua road. Đã được kiểm chứng ở World Tour: tăng độ ổn định tanh lốp, hỗ trợ run-flat và chống va đập, trong khi vẫn giữ cảm giác lốp nhanh, mềm mại.',
             'Vật liệu siêu nhẹ chỉ thêm 29–40g mỗi bánh tùy cỡ. Thể tích tối ưu cho vành và lốp bản rộng hiện đại; khi thủng, miếng lót giúp bạn đi tiếp tới 50 km.'],
      fit=['Road race', 'Endurance', 'Gravel nhẹ (bản 38–42)'],
      imgs=['air-liner-light-road-insert-01', 'air-liner-light-road', 'air-liner-light-road-insert-03', 'air-liner-light-road-insert-02'],
      opt='Kích thước',
      features=[('Áp suất thấp hơn', 'Bám đường hơn, êm hơn mà không lo va vành.'),
                ('Run-flat tới 50 km', 'Lớp bọt nở ra khi thủng; tanh lốp TLR được giữ ổn định.'),
                ('Ổn định khi vào cua', 'Tăng lực đỡ thành lốp — vào cua nhanh và chắc hơn.'),
                ('Độ trễ thấp', 'Gần như không ảnh hưởng tới lực cản lăn.'),
                ('Siêu nhẹ', 'Chỉ thêm 29–40g mỗi bánh, tối đa tốc độ trên các chặng đua.')],
      cols=['Cỡ lốp', 'Lòng vành', 'Trọng lượng', 'Van đi kèm', 'Mã sản phẩm'],
      rows=[('700x28-30c', '20-25mm', '29g', '60mm', '1AA00541'), ('700x32-36c', '21-27mm', '35g', '60mm', '1AA00542'), ('700x38-42c', '23-28mm', '40g', '60mm', '1AA00543')],
      note='Mỗi hộp gồm 1 miếng lót và 1 van Vittoria Multiway Tubeless 60mm. Chỉ dùng với lốp tubeless, van multiway và keo không amoniac.',
      faq=[('Hợp với lốp nào?', 'Lốp road tubeless bản 28–42mm như Vittoria Corsa PRO, Corsa N.Ext hoặc Rubino. Chọn cỡ theo bản lốp và lòng vành trong bảng kỹ thuật.'),
           ('Có làm xe chậm đi không?', 'Miếng lót có độ trễ thấp, gần như không ảnh hưởng lực cản lăn, chỉ thêm 29–40g mỗi bánh.'),
           ('Dùng keo gì đi kèm?', 'Chỉ dùng keo không amoniac, ví dụ Vittoria Universal Sealant.')]),
 dict(file='vittoria-multiway-valve.html', group='valve', name='Chân van Multiway (bộ 2 van)', short='Chân van Multiway',
      cat='Chân van', tag='Bộ 2 van', headline='Van tubeless nhôm cho mọi loại vành',
      desc='Nhôm · 40 / 60 / 80 / 100mm · bộ 2 van',
      intro=['Chân van tubeless Vittoria Multiway làm từ nhôm cao cấp, bền và nhẹ. Nắp van bằng hợp kim có tích hợp dụng cụ tháo ruột van để bơm keo hay thay ruột van nhanh chóng.',
             'Van tương thích với keo có hạt đậm đặc và miếng lót Air-Liner — lựa chọn cần có cho một bộ lốp tubeless hoàn chỉnh. Có 4 chiều dài 40, 60, 80 và 100mm cho mọi độ cao vành, cả road lẫn MTB; gioăng và ruột van đều thay được để dùng lâu dài.'],
      fit=['Road', 'Gravel', 'MTB', 'Dùng cùng Air-Liner'],
      imgs=['multiway-valves'],
      opt='Chiều dài van',
      features=[('Nhôm cao cấp', 'Thân van nhôm bền và nhẹ.'),
                ('Nắp có dụng cụ tháo ruột van', 'Tháo ruột van ngay bằng nắp van — tiện khi bơm keo hoặc thay ruột van.'),
                ('Tương thích keo hạt & Air-Liner', 'Dùng được với keo có hạt đậm đặc và miếng lót Air-Liner của Vittoria.'),
                ('4 chiều dài', '40, 60, 80 và 100mm — phù hợp mọi độ cao vành road và MTB.'),
                ('Gioăng & ruột van thay được', 'Thay riêng từng chi tiết để kéo dài tuổi thọ van.')],
      cols=['Chiều dài van', 'Số lượng', 'Mã sản phẩm'],
      rows=[('40mm', '2 van', '1AA00091'), ('60mm', '2 van', '1AA00092'), ('80mm', '2 van', '1AA00093'), ('100mm', '2 van', '1AA00094')],
      note='Mỗi bộ gồm 2 chân van.',
      faq=[('Chọn chiều dài van thế nào?', 'Chọn van dài hơn chiều cao vành để đầu van nhô ra đủ cho đầu bơm. Vành thấp thường dùng 40mm, vành cao (carbon aero) cần 60–100mm. Liên hệ Spinlab kèm thông tin vành để được tư vấn đúng cỡ.'),
           ('Có dùng với Air-Liner được không?', 'Được. Vittoria thiết kế van Multiway tương thích với miếng lót Air-Liner; các bộ Air-Liner Light cũng đi kèm van Multiway.'),
           ('Một bộ có mấy van?', 'Mỗi bộ gồm 2 chân van, đủ cho cả bánh trước và bánh sau.')]),
 dict(file='vittoria-air-liner-protect-trail.html', group='air-liner', name='Air-Liner Protect Trail', short='Air-Liner Protect Trail',
      cat='Air-Liner Protect', tag='MTB · Trail', headline='Lót tubeless đa năng nhất cho đường mòn',
      desc='29x2.1–2.6 · Run-flat tới 50 km',
      intro=['Air-Liner Protect Trail là hệ thống lót tubeless MTB đa năng nhất của Vittoria, cân bằng giữa khả năng bảo vệ, độ ổn định thành lốp và trọng lượng — hoạt động tốt trên nhiều loại địa hình.',
             'Miếng lót giảm va đập và làm êm những đoạn đường mòn gồ ghề, tăng khả năng chống thủng, giảm rung, giữ xe ổn định và lái chính xác khi đổ dốc kỹ thuật.'],
      fit=['Trail', 'All-mountain', 'Bánh 29"'],
      imgs=['air-liner-protect-trail.webp', 'air-liner-protect-trail-insert-01_e6908d12-899a-47d3-a5f0-2c79ec1b74f9.png', 'air-liner-protect-trail-insert-03.jpg'],
      opt='Kích thước',
      features=[('Bảo vệ vành', 'Chống những cú va đập mạnh nhất và ngăn thủng kiểu rắn cắn.'),
                ('Run-flat tới 50 km', 'Khi thủng lốp, vẫn có thể đạp tiếp tới 50 km ở chế độ run-flat.'),
                ('Ổn định thành lốp', 'Giữ thành lốp vững khi vào cua và tiếp đất.'),
                ('Giảm rung', 'Làm êm đường mòn gồ ghề, lái chính xác hơn.')],
      cols=['Cỡ lốp', 'Mã sản phẩm'],
      rows=[('29x2.1-2.6', '1AA00496')],
      note='Chỉ dùng với lốp tubeless, van multiway và keo không amoniac.',
      faq=[('Hợp với lốp nào?', 'Bánh 29 inch, lốp bản 2.1–2.6 inch.'),
           ('Dùng keo gì đi kèm?', 'Chỉ dùng keo không amoniac, ví dụ Vittoria Universal Sealant.')]),
 dict(file='vittoria-tubeless-rim-tape.html', group='rim-tape', name='Băng keo vành tubeless', short='Băng keo vành tubeless',
      cat='Băng keo vành', tag='Tubeless', headline='Bịt kín lòng vành để lên tubeless',
      desc='23 – 32mm · cuộn 9m / 66m',
      intro=['Băng keo vành tubeless Vittoria dán kín các lỗ căm trong lòng vành để giữ hơi khi chạy lốp không săm (tubeless).',
             'Chọn bản băng keo theo bề rộng lòng trong của vành. Cuộn 9m đủ dán nhiều bộ vành; cuộn 66m dành cho xưởng sửa xe.'],
      fit=['Road', 'Gravel', 'MTB'],
      imgs=['tubeless-rim-tape-01_1.webp', 'tubeless-rim-tape-04_1.webp', 'tubeless-rim-tape-03_1.webp'],
      opt='Bản rộng x chiều dài',
      features=[('Kín hơi cho tubeless', 'Bịt kín lòng vành và lỗ căm để giữ hơi khi chạy không săm.'),
                ('Nhiều bản rộng', 'Chọn theo lòng trong vành: 23, 25, 27, 29 hoặc 32mm.'),
                ('Cuộn cho xưởng', 'Bản 32mm x 66m tiết kiệm cho cửa hàng và xưởng.')],
      cols=['Bản rộng x chiều dài', 'Mã sản phẩm'],
      rows=[('23mm x 9m', '1AA00549'), ('25mm x 9m', '1AA00550'), ('27mm x 9m', '1AA00551'), ('29mm x 9m', '1AA00552'), ('32mm x 66m', '1AA00561')],
      note='Chọn bản rộng bằng hoặc lớn hơn lòng trong của vành một chút.',
      faq=[('Chọn bản rộng nào?', 'Chọn theo bề rộng lòng trong của vành (thường in trên vành hoặc trong thông số bánh). Liên hệ Spinlab để được tư vấn đúng bản.')]),
 dict(file='vittoria-sidewall-cleaner.html', group='care', name='Dung dịch vệ sinh thành lốp', short='Sidewall Cleaner',
      cat='Vệ sinh lốp', tag='Vệ sinh', headline='Làm sạch thành lốp, kể cả lốp cotton',
      desc='Dùng được cho lốp cotton và nylon',
      intro=['Vittoria Sidewall Cleaner làm sạch và phục hồi vẻ ngoài của thành lốp xe đạp mà không ảnh hưởng tới cấu trúc lốp.',
             'Theo Vittoria, đây là sản phẩm duy nhất trên thị trường dùng được cho lốp cotton, giúp thành lốp sáng đẹp như mới. Đầu bọt biển tích hợp giúp thao tác nhanh và gọn.'],
      fit=['Lốp cotton', 'Lốp nylon', 'Bảo dưỡng định kỳ'],
      imgs=['sidewall-cleaner-01_1.webp', 'sidewall-cleaner-03_1.webp', 'sidewall-cleaner-04_1.webp'],
      opt='Quy cách',
      features=[('Cho lốp cotton và nylon', 'Công thức dành riêng cho cả thân lốp cotton và nylon.'),
                ('Đầu bọt biển tích hợp', 'Thoa chính xác, không cần dụng cụ khác.'),
                ('Nhẹ nhàng với lốp', 'Làm sạch bụi bẩn mà không ảnh hưởng cấu trúc lốp.')],
      cols=['Quy cách', 'Mã sản phẩm'],
      rows=[('Chai kèm đầu bọt biển', '1AA00455')],
      note='',
      faq=[('Dùng cho lốp nào?', 'Dùng cho thành lốp cotton (như Corsa PRO) và nylon.')]),
 dict(file='vittoria-standard-inner-tube.html', group='other', name='Săm Standard 700x20/28c', short='Săm Standard',
      cat='Săm', tag='Săm butyl', headline='Săm butyl bền, giữ hơi lâu',
      desc='700x20/28c · van Presta 48 / 60 / 80mm',
      intro=['Săm butyl Standard của Vittoria giữ hơi tốt qua nhiều ngày và đủ bền để mang theo trong túi áo hay túi yên, thay nhanh bên đường khi cần.',
             'Cỡ 700x20/28c cho xe road, van Presta (FV) với 3 chiều dài 48, 60 và 80mm cho các độ cao vành khác nhau.'],
      fit=['Road', 'Dự phòng khi đi tour', 'Tập luyện hằng ngày'],
      imgs=['standard-inner-tube.webp', 'vittoria-standard-tube-700x20-28c-valve-48-mm.jpg'],
      opt='Van Presta',
      features=[('Butyl bền bỉ', 'Giữ hơi qua nhiều ngày, chịu được va chạm khi mang theo.'),
                ('3 chiều dài van', '48mm, 60mm và 80mm cho vành thấp đến vành cao.')],
      cols=['Van Presta (FV)', 'Cỡ', 'Mã sản phẩm'],
      rows=[('48mm (RVC)', '700x20/28c', '1TA00010'), ('60mm (RVC)', '700x20/28c', '1TA00011'), ('80mm', '700x20/28c', '1TA00012')],
      note='RVC: ruột van tháo được.',
      faq=[('Chọn chiều dài van nào?', 'Chọn van dài hơn chiều cao vành để đủ chỗ gắn đầu bơm; vành cao (aero) cần van 60–80mm.')]),
 dict(file='vittoria-bottle-550.html', group='other', name='Bình nước Vittoria 550ml', short='Bình nước 550ml',
      cat='Bình nước', tag='550ml', headline='Bình nước siêu nhẹ của Vittoria',
      desc='550ml · xám than + đen',
      intro=['Bình nước Vittoria 550ml màu xám than kết hợp đen. Dòng bình FLY của Vittoria do Elite — nhà sản xuất bình nước hàng đầu — sản xuất, cùng công nghệ với bình của các đội World Tour.',
             'Theo Vittoria, bình FLY chỉ nặng 54g cho dung tích 550ml; thân bình dễ bóp, cho dòng nước mạnh mà không cần bóp mạnh tay.'],
      fit=['Road', 'Gravel', 'MTB'],
      imgs=['vittoria-bottle.webp', 'vittoria-bottle-cage.webp'],
      opt='Màu',
      features=[('Siêu nhẹ', 'Thân bình mỏng nhẹ, ít nhựa.'),
                ('Dễ bóp', 'Dòng nước mạnh với lực bóp nhẹ.')],
      cols=['Màu', 'Dung tích', 'Mã sản phẩm'],
      rows=[('Xám than + đen', '550ml', '1AA00577')],
      note='Ảnh minh họa dòng bình FLY 550ml của Vittoria.',
      faq=[('Bình có vừa giá đỡ bình thông thường không?', 'Có, bình 550ml dùng với giá đỡ bình tiêu chuẩn.')]),
]
GROUPS = [('sealant', 'Keo tự vá', 'Keo tubeless không amoniac cho road, gravel và MTB.'),
          ('valve', 'Chân van', 'Van tubeless Multiway bằng nhôm, bộ 2 van, 4 chiều dài.'),
          ('rim-tape', 'Băng keo vành', 'Băng keo bịt kín lòng vành để lên tubeless.'),
          ('air-liner', 'Air-Liner', 'Miếng lót tubeless: chống va vành, chống thủng rắn cắn và chạy run-flat khi xì lốp.'),
          ('care', 'Vệ sinh lốp', 'Dung dịch làm sạch thành lốp cotton và nylon.'),
          ('other', 'Săm & phụ kiện khác', 'Săm butyl và bình nước Vittoria.')]

# Spinlab's stock list decides which rows (sizes) are shown; a product with no row in stock is not published
for _p in P:
    _p['rows'] = [r for r in _p['rows'] if stock.ok(r[-1])]
ALL_P = list(P)
P[:] = [p for p in P if p['rows']]

price = lambda p: stock.label(r[-1] for r in p['rows'])
_EXT = re.compile(r'\.(webp|png|jpe?g)$')
img = lambda n, w: CDN + n + ('' if _EXT.search(n) else '.webp') + f'?width={w}'


def card(p):
    return (f'<article class="p-card" data-type="{p["group"]}"><div class="p-img tire"><span class="tag dark">{E(p["tag"])}</span>'
            f'<img src="{img(p["imgs"][0], 600)}" alt="Vittoria {E(p["name"])}" loading="lazy"></div>'
            f'<div class="p-body"><span class="p-brand">Vittoria · {E(p["cat"])}</span><h3 class="p-name"><a class="stretch" href="{p["file"]}">{E(p["name"])}</a></h3>'
            f'<p class="p-desc">{E(p["desc"])}</p><span class="p-price">{price(p)}</span></div></article>')


def page(p, shell):
    thumbs = ''.join(f'<li><button aria-pressed="{"true" if i == 0 else "false"}" data-src="{img(n, 1000)}" data-alt="{E(p["name"])} – ảnh {i+1}"><img src="{img(n, 160)}" alt="Ảnh {i+1}"></button></li>' for i, n in enumerate(p['imgs']))
    opts = ''.join(f'<label><input type="radio" name="size" value="{E(r[0])}" data-sku="{r[-1]}"{" checked" if i == 0 else ""}><span>{E(r[0])}</span></label>' for i, r in enumerate(p['rows']))
    feats = ''.join(f'<article><span class="num">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(x)}</p></article>' for i, (t, x) in enumerate(p['features']))
    head = ''.join(f'<th scope="col">{E(c)}</th>' for c in p['cols'])
    rows = ''.join(f'<tr data-sku="{r[-1]}">' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in p['rows'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in p['faq'])
    rel = ''.join(card(o) for o in P if o is not p)
    intro = ''.join(f'<p>{E(t)}</p>' for t in p['intro'])
    fit = ''.join(f'<li>{E(f)}</li>' for f in p['fit'])
    main = f'''<main id="main" class="pdp">
  <div class="container">
    <nav class="crumbs" aria-label="Đường dẫn"><ol>
      <li><a href="index.html">Trang chủ</a></li><li><a href="index.html#hot">Phụ tùng</a></li><li><a href="tubeless.html">Tubeless</a></li>
      <li><a class="crumb" href="tubeless.html#{p["group"]}">{E(p["cat"])}</a></li><li aria-current="page">{E(p["name"])}</li></ol></nav>
    <div class="pdp-top">
      <div class="gallery">
        <div class="g-main"><img id="g-main" src="{img(p["imgs"][0], 1000)}" alt="Vittoria {E(p["name"])}" width="1000" height="1000"></div>
        <ul class="g-thumbs" aria-label="Ảnh sản phẩm">{thumbs}</ul>
      </div>
      <div class="buy">
        <span class="p-brand">Vittoria · Tubeless · {E(p["cat"])}</span>
        <h1>{E(p["name"])}</h1>
        <p class="tagline">{E(p["headline"])}</p>
        <fieldset class="sizes"><legend>{E(p["opt"])} <span class="size-meta" aria-live="polite">Mã <span id="sz-sku">{p["rows"][0][-1]}</span></span></legend><div class="size-opts" id="size-opts">{opts}</div></fieldset>
        <div class="price-row"><span class="label">Giá bán lẻ</span><span class="p-price big">{price(p)}</span></div>
        <div class="buy-ctas">
          <a class="btn btn-zalo outline" href="https://zalo.me/0399337533" target="_blank" rel="noopener"><img src="{ZALO}" alt="" width="22" height="22">Chat Zalo</a>
          <a class="btn btn-outline" href="tel:0399337533">Gọi 0399 337 533</a>
        </div>
        <ul class="assure">
          <li><svg aria-hidden="true"><use href="#i-shield"/></svg>Hàng chính hãng Vittoria, phân phối bởi Spinlab</li>
          <li><svg aria-hidden="true"><use href="#i-truck"/></svg>Giao hàng toàn quốc</li>
          <li><svg aria-hidden="true"><use href="#i-chat"/></svg>Tư vấn và hỗ trợ lắp tubeless qua hotline</li>
        </ul>
      </div>
    </div>

    <nav class="pdp-nav" aria-label="Nội dung sản phẩm"><a href="#gioi-thieu">Giới thiệu</a><a href="#cong-nghe">Tính năng</a><a href="#ma-san-pham">Bảng kỹ thuật</a><a href="#hoi-dap">Hỏi đáp</a></nav>

    <section class="pdp-sec intro" id="gioi-thieu">
      <div><h2>{E(p["headline"])}</h2>{intro}
        <p class="siblings"><b>Phù hợp:</b></p><ul class="fit">{fit}</ul></div>
      <figure><img src="{img(p["imgs"][1] if len(p["imgs"]) > 1 else p["imgs"][0], 900)}" alt="Vittoria {E(p["name"])}" loading="lazy"></figure>
    </section>

    <section class="pdp-sec" id="cong-nghe"><h2>Tính năng</h2><div class="tech">{feats}</div></section>

    <section class="pdp-sec" id="ma-san-pham"><h2>Bảng kỹ thuật</h2><div class="table-wrap"><table class="sku-table spec-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div><p class="geo-note">Dòng đang chọn được tô màu. {E(p["note"])} Số liệu theo công bố của Vittoria; vui lòng liên hệ Spinlab để kiểm tra hàng có sẵn.</p></section>

    <section class="pdp-sec" id="hoi-dap"><h2>Hỏi đáp</h2><div class="faq">{faq}</div></section>

    <section class="pdp-sec"><div class="sec-head"><h2>Phụ kiện tubeless khác</h2><a class="see-all" href="tubeless.html">Xem tất cả</a></div>
      <div class="grid related" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">{rel}</div></section>
  </div>
</main>'''
    js = '''// Tubeless accessory page: gallery + size/volume selector
(() => {
  const main=document.getElementById('g-main'), t=[...document.querySelectorAll('.g-thumbs button')];
  t.forEach(b=>b.addEventListener('click',()=>{ main.src=b.dataset.src; main.alt=b.dataset.alt; t.forEach(x=>x.setAttribute('aria-pressed',x===b)); }));
  const upd=()=>{ const r=document.querySelector('input[name=size]:checked'); if(!r) return;
    document.getElementById('sz-sku').textContent=r.dataset.sku;
    document.querySelectorAll('.sku-table tbody tr').forEach(tr=>tr.classList.toggle('on',tr.dataset.sku===r.dataset.sku)); };
  document.querySelectorAll('input[name=size]').forEach(r=>r.addEventListener('change',upd)); upd();
})();
'''
    s = shell
    s = re.sub(r'<title>.*?</title>', f'<title>Vittoria {E(p["name"])} — {E(p["cat"])} — Spinlab</title>', s, 1, flags=re.S)
    s = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="Vittoria {E(p["name"])}: {E(p["headline"])}. Phân phối chính hãng bởi Spinlab.">', s, 1)
    s = re.sub(r'<main id="main".*?</main>', lambda m: main, s, 1, flags=re.S)
    s = re.sub(r'// MTB tire page: version.*?\}\)\(\);\n', lambda m: js, s, 1, flags=re.S)
    assert '// Tubeless accessory page' in s
    return s


shell = open(os.path.join(D, 'vittoria-tattoo.html'), encoding='utf-8').read()
for p in P:
    open(os.path.join(D, p['file']), 'w', encoding='utf-8').write(page(p, shell))
    print(p['file'])

# listing page, built on lop-xe.html
L = open(os.path.join(D, 'lop-xe.html'), encoding='utf-8').read()
secs = ''
for g, t, s_ in GROUPS:
    cs = ''.join(card(p) for p in P if p['group'] == g)
    secs += (f'  <section class="brand-cat" id="{g}"><div class="container"><h2 class="bc-title">{E(t)}</h2><p class="bc-sub">{E(s_)}</p>'
             f'<div class="grid">{cs}</div></div></section>\n')
main = f'''<main id="main" class="pdp listing">
  <div class="container"><nav class="crumbs" aria-label="Đường dẫn"><ol><li><a href="index.html">Trang chủ</a></li><li><a href="index.html#hot">Phụ tùng</a></li><li aria-current="page">Tubeless &amp; phụ kiện</li></ol></nav></div>
  <section class="list-hero">
    <img src="{img("air-liner-light-road", 1920)}" alt="Miếng lót tubeless Vittoria Air-Liner Light Road">
    <div class="container"><div class="lh-copy"><span class="kicker">Vittoria</span><h1>Tubeless &amp; phụ kiện</h1><p>Keo tự vá, chân van, băng keo vành, miếng lót Air-Liner, săm và phụ kiện chính hãng Vittoria.</p></div></div>
  </section>
  <nav class="brand-nav" aria-label="Danh mục tubeless"><div class="container"><ul>{"".join(f'<li><a href="#{g}">{E(t)}<small>{sum(p["group"] == g for p in P)}</small></a></li>' for g, t, s_ in GROUPS)}</ul></div></nav>
{secs}</main>'''
L = re.sub(r'<title>.*?</title>', '<title>Tubeless &amp; phụ kiện Vittoria — Spinlab</title>', L, 1, flags=re.S)
L = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Phụ kiện tubeless Vittoria chính hãng tại Spinlab: keo tự vá Universal Sealant và miếng lót Air-Liner Light cho road, gravel, MTB.">', L, 1)
L = re.sub(r'<main id="main".*?</main>', lambda m: main, L, 1, flags=re.S)
L = re.sub(r'\n// Tire listing[^\n]*\n.*?\}\)\(\);\n', '\n', L, 1, flags=re.S)
brand_css = re.search(r'/\* Brand page \*/.*?(?=</style>)', open(os.path.join(D, 'thuong-hieu-vittoria.html'), encoding='utf-8').read(), re.S).group(0)
L = L.replace('</style>', brand_css + '</style>', 1)
open(os.path.join(D, 'tubeless.html'), 'w', encoding='utf-8').write(L)
print('tubeless.html')
json.dump([{k: p[k] for k in ('file', 'group', 'name', 'cat', 'tag', 'desc', 'imgs')} for p in P], open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tubeless-cards.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
