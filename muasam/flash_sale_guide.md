# Quản Lý Flash Sale

Tài liệu này hướng dẫn cách quản lý chức năng Flash Sale trên website SmartTech.

## Giới thiệu về Flash Sale

Flash Sale là các chương trình khuyến mãi giới hạn thời gian với mức giảm giá hấp dẫn, nhằm tạo sự cấp bách và thúc đẩy người dùng mua hàng ngay lập tức. Đặc điểm của Flash Sale:
- Giảm giá sâu (thường từ 10% đến 50%)
- Thời gian giới hạn (thường từ vài giờ đến 1 ngày)
- Số lượng sản phẩm giới hạn
- Hiển thị đồng hồ đếm ngược

## Tạo Flash Sale

### Bằng giao diện quản trị Django

1. Đăng nhập vào trang quản trị Django (/admin)
2. Điều hướng đến mục "Flash Sales" và nhấp vào "Thêm Flash Sale"
3. Điền các thông tin sau:
   - Sản phẩm: Chọn sản phẩm áp dụng Flash Sale
   - Thời gian bắt đầu: Thời điểm bắt đầu Flash Sale
   - Thời gian kết thúc: Thời điểm kết thúc Flash Sale
   - Phần trăm giảm giá: Mức giảm giá (%)
   - Giá gốc: Giá trước khi giảm
   - Giá bán: Giá sau khi giảm
   - Số lượng có sẵn: Tổng số sản phẩm trong đợt Flash Sale
   - Số lượng đã bán: Số lượng sản phẩm đã bán (mặc định là 0)
   - Đang hoạt động: Trạng thái của Flash Sale (nên bật)
4. Lưu lại để tạo Flash Sale

### Bằng script tự động

Để tạo nhanh nhiều Flash Sale cho các sản phẩm, bạn có thể sử dụng script `create_flash_sales.py`:

```bash
python create_flash_sales.py
```

Script này sẽ tự động tạo Flash Sale cho khoảng 70% sản phẩm hiện có trong hệ thống, với mức giảm giá ngẫu nhiên từ 10% đến 50%.

## Hiển thị Flash Sale trên trang chủ

Flash Sale sẽ tự động hiển thị trên trang chủ khi:
1. Flash Sale đang trong thời gian hoạt động (thời gian hiện tại nằm giữa thời gian bắt đầu và kết thúc)
2. Flash Sale được đánh dấu là "Đang hoạt động"
3. Còn sản phẩm trong kho (số lượng có sẵn > số lượng đã bán)

## Bộ đếm thời gian

Bộ đếm thời gian sẽ hiển thị thời gian còn lại của Flash Sale. Khi thời gian kết thúc, bộ đếm sẽ hiển thị "Flash Sale đã kết thúc!" và Flash Sale sẽ không còn hiển thị trên trang chủ trong lần tải trang tiếp theo.

## Quản lý giỏ hàng và thanh toán

Khi người dùng thêm sản phẩm Flash Sale vào giỏ hàng, hệ thống sẽ sử dụng giá Flash Sale thay vì giá gốc của sản phẩm. Tuy nhiên, cần lưu ý:
- Kiểm tra tính hợp lệ của Flash Sale tại thời điểm thêm vào giỏ hàng
- Kiểm tra lại tính hợp lệ của Flash Sale tại thời điểm thanh toán
- Cập nhật số lượng đã bán khi hoàn tất đơn hàng

## Lưu ý quan trọng

- Flash Sale có thể bị trùng lặp: Một sản phẩm có thể có nhiều Flash Sale cùng lúc, trong trường hợp này hệ thống sẽ sử dụng Flash Sale có mức giảm giá cao nhất.
- Đồng bộ thời gian: Đảm bảo máy chủ và trình duyệt người dùng có thời gian chính xác để hiển thị đúng thời gian còn lại của Flash Sale.
