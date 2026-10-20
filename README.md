# Spinlab Vietnam — website (bản thiết kế xem trước)

Website phân phối xe đạp và phụ kiện của **Spinlab Việt Nam**: xe đạp Polygon và Story, lốp và phụ kiện tubeless Vittoria, dây cuốn tay lái Emume.

Đây là bản thiết kế dạng HTML tĩnh để duyệt giao diện và nội dung trước khi dựng website Node.js (có trang quản trị và MySQL) và đưa lên Hostinger.

## Xem thử trên máy

Website dùng đường dẫn gọn (`/trangchu`, `/xe-road`, `/polygon-xtrada-7`…), nên cần mở qua server:

```bash
python3 tools/serve.py
```

Rồi mở http://127.0.0.1:8765/trangchu

Trên Hostinger, file `.htaccess` lo việc này: `/` chuyển tới `/trangchu`, `/xe-road` trả về `xe-road.html`, link cũ `…html` tự chuyển sang link gọn, thư mục `tools/` bị chặn truy cập.

## Cấu trúc

| Thư mục / file | Nội dung |
|---|---|
| `index.html` | Trang chủ |
| `xe-road.html`, `xe-mtb.html`, `xe-gravel.html`, `xe-trial.html` | Danh mục xe |
| `lop-xe.html`, `tubeless.html`, `day-cuon-tay-lai.html` | Danh mục phụ tùng |
| `thuong-hieu-*.html` | Trang thương hiệu (Polygon, Vittoria, Emume, Story Bike) |
| `polygon-*.html`, `story-*.html`, `vittoria-*.html`, `terreno-*.html`, `corsa-pro.html`, `emume-*.html` | Trang chi tiết sản phẩm |
| `san-pham-moi.html`, `so-sanh.html`, `dai-ly.html` | Sản phẩm mới, so sánh sản phẩm, hệ thống đại lý |
| `img/` | Ảnh sản phẩm lưu cục bộ (Tambora, Story, Emume) |
| `data/` | Dữ liệu sản phẩm và ngày đăng (`catalog.json`) |
| `tools/` | Công cụ tạo trang — xem `tools/README.md` |

## Cập nhật sau khi thêm / gỡ sản phẩm

```bash
cd tools/generators && python3 brands.py ../.. bikes.json && cd ../..
python3 tools/build_new_products.py
python3 tools/apply_prices.py
python3 tools/build_compare.py
python3 tools/brand_logos.py
python3 tools/build_hubs.py
python3 tools/clean_urls.py      # luôn chạy cuối cùng
```
