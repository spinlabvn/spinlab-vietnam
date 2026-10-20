# Spinlab Vietnam — website (bản thiết kế xem trước)

Website phân phối xe đạp và phụ kiện của **Spinlab Việt Nam**: xe đạp Polygon và Story, lốp và phụ kiện tubeless Vittoria, dây cuốn tay lái Emume.

Đây là bản thiết kế dạng HTML tĩnh để duyệt giao diện và nội dung trước khi dựng website Node.js (có trang quản trị và MySQL) và đưa lên Hostinger.

## Xem thử trên máy

Ảnh sản phẩm lưu trong thư mục `img/` cần mở qua server thì mới hiện:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Rồi mở http://127.0.0.1:8765/index.html

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
```
