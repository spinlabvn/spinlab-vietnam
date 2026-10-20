# Công cụ tạo trang — Spinlab design preview

Các công cụ dùng để tạo trang sản phẩm cho bản thiết kế xem trước. Chạy bằng `python3` (3.9 trở lên), không cần cài thêm gì.
Các lệnh dưới đây chạy từ thư mục `design-preview/tools/generators`.

## Sau mỗi lần thêm hoặc gỡ sản phẩm

```bash
python3 brands.py ../.. bikes.json        # tạo lại 4 trang thương hiệu
python3 ../build_new_products.py      # cập nhật "Sản phẩm mới" (trang chủ + san-pham-moi.html)
python3 ../apply_prices.py            # giá Vittoria theo từng mã (data/vittoria-stock.json)
python3 ../build_compare.py           # cập nhật dữ liệu so sánh (so-sanh.html) + nút So sánh trên mọi trang
python3 ../build_hubs.py              # trang tổng hợp /xe-dap, /phu-tung, /thuong-hieu
python3 ../clean_urls.py              # LUÔN chạy cuối: đổi link sang dạng gọn (/xe-road, /trangchu)
```

## Xe đạp (Polygon, Story)

`gen.py` dùng chung cho mọi hãng xe: đặt `brand='Story'` trong mục `vi.py` cho xe không phải Polygon (mặc định là Polygon).

| File | Vai trò |
|---|---|
| `bikes.json` | Dữ liệu xe: màu, size, mã sản phẩm, thông số, bảng kích thước khung (lấy từ polygonbikes.com hoặc spec sheet) |
| `vi.py` | Nội dung tiếng Việt cho từng xe: danh mục, dòng xe, giới thiệu, tính năng; bảng dịch tên thông số |
| `gen.py` | Tạo trang chi tiết xe: `python3 gen.py ../.. bikes.json [slug ...]` (bỏ trống slug = tạo lại tất cả) |
| `extract.py` | Đọc trang sản phẩm Polygon đã tải về → JSON: `python3 extract.py <thư mục html> <out.json> <slug ...>` |
| `tambora.py` | Dữ liệu Tambora MY27 nhập từ spec sheet; gộp vào `bikes.json` |
| `story.py` | Dữ liệu Story Continue Pro (chỉ các thông tin thấy được trên ảnh); gộp vào `bikes.json` |

Thêm một xe mới: lấy dữ liệu (extract.py hoặc nhập tay như tambora.py) → gộp vào `bikes.json` → thêm mục trong `vi.py` → chạy `gen.py` cho slug đó → thêm thẻ vào trang danh sách (xe-road / xe-mtb / xe-gravel) → chạy hai lệnh ở trên.

## Lốp và phụ kiện Vittoria

Giá bán lẻ và hàng có sẵn lấy từ `data/vittoria-stock.json` (chuyển từ bảng giá của Spinlab). Chỉ những mã có trong file này mới hiện trên web; dòng lốp không còn mã nào thì không tạo trang. Sau khi chạy `vtires.py` / `terreno.py`, chạy `python3 tires_listing.py ../..` để dựng lại lưới sản phẩm của `lop-xe.html`.

| File | Vai trò |
|---|---|
| `vtires.py`, `mtbtires.py`, `terreno.py` | Tạo trang chi tiết lốp: `python3 <file> ../.. vittoria-json/<thư mục>` |
| `vcommon.py`, `vtech.json` | Phần dùng chung: bảng kỹ thuật, bản dịch công nghệ lốp |
| `vtech.py` | Đọc trang Vittoria đã tải về → `vtech.json` |
| `tires-page.py` | Tạo trang danh sách `lop-xe.html` |
| `tubeless.py` | Keo tự vá + Air-Liner Light và trang `tubeless.html` |
| `vittoria-json/` | Dữ liệu sản phẩm Vittoria (Shopify JSON) |

## Dây cuốn tay lái Emume

| File | Vai trò |
|---|---|
| `emume.py` | 10 trang sản phẩm Emume + trang `day-cuon-tay-lai.html`. Lần đầu chạy kèm thư mục ảnh trích từ file Excel: `python3 emume.py ../.. <thư mục imageN.png>`; sau đó chỉ cần `python3 emume.py ../..` |

## Trang khác

| File | Vai trò |
|---|---|
| `daily.py` | Trang `dai-ly.html` (danh sách đại lý — đang là dữ liệu mẫu) |
| `drawer.py` | Thêm menu trượt cho điện thoại vào các trang |

## Lưu ý

- `corsa-pro.html` là trang mẫu (khung đầu trang, menu, chân trang) cho các trang xe và lốp. Muốn đổi menu hay chân trang thì sửa trên tất cả các trang, kể cả `corsa-pro.html`, để trang tạo sau giữ thay đổi.
- `removed-pages/` lưu các trang sản phẩm đã gỡ khỏi website (xe điện, Syncline C, Helios A8X/A9X), phòng khi cần dùng lại.
