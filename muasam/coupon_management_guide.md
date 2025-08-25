# Hướng dẫn tạo và quản lý mã giảm giá

## 1. Truy cập trang quản trị Django Admin

1. Khởi động server Django:
   ```
   python3 manage.py runserver
   ```

2. Truy cập trang quản trị Django Admin:
   ```
   http://127.0.0.1:8000/admin/
   ```

3. Đăng nhập với tài khoản admin của bạn (nếu chưa có, tạo tài khoản superuser):
   ```
   python3 manage.py createsuperuser
   ```

## 2. Tạo mã giảm giá mới

1. Sau khi đăng nhập vào trang admin, tìm mục **Coupons** và nhấp vào "Add Coupon"

2. Điền các thông tin mã giảm giá:

   **Thông tin mã giảm giá:**
   - **Code**: Mã code giảm giá (ví dụ: WELCOME10, SALE50K)
   - **Discount type**: Chọn loại giảm giá:
     - `percentage`: Giảm giá theo phần trăm (%)
     - `fixed`: Giảm giá theo số tiền cố định (VND)
   - **Value**: Giá trị giảm giá (nếu là % thì nhập số %, nếu là số tiền cố định thì nhập số tiền)
   - **Min value**: Giá trị đơn hàng tối thiểu để áp dụng mã giảm giá (VND)
   - **Max discount**: Giới hạn số tiền giảm giá tối đa (chỉ áp dụng cho loại giảm giá theo %)
   - **Active**: Trạng thái kích hoạt (chọn để kích hoạt mã)

   **Thời gian và lượt sử dụng:**
   - **Valid from**: Thời gian bắt đầu hiệu lực
   - **Valid to**: Thời gian kết thúc hiệu lực
   - **Max uses**: Số lần sử dụng tối đa
   - **Times used**: Số lần đã được sử dụng (mặc định là 0 cho mã mới)

3. Nhấp vào nút "Save" để lưu mã giảm giá

## 3. Quản lý mã giảm giá

1. **Danh sách mã giảm giá**:
   - Hiển thị tất cả các mã giảm giá trong hệ thống
   - Thông tin hiển thị: Mã, giá trị giảm giá, trạng thái, thời gian hiệu lực, số lần sử dụng
   - Có thể lọc theo trạng thái và loại giảm giá
   - Tìm kiếm theo mã code

2. **Chỉnh sửa mã giảm giá**:
   - Nhấp vào mã code để chỉnh sửa
   - Cập nhật thông tin, thời gian, lượt sử dụng
   - Lưu thay đổi

3. **Vô hiệu hóa mã giảm giá**:
   - Để vô hiệu hóa mã, bỏ chọn trường "Active"
   - Hoặc thay đổi thời gian "Valid to" thành thời điểm trong quá khứ

## 4. Các loại mã giảm giá thông dụng

### Mã giảm theo phần trăm (%)

1. **Giảm giá 10% cho đơn hàng từ 100,000 VND**:
   - Code: WELCOME10
   - Discount type: percentage
   - Value: 10
   - Min value: 100000
   - Max discount: 100000 (giới hạn tối đa 100,000 VND)

2. **Giảm giá 20% không giới hạn cho đơn hàng từ 500,000 VND**:
   - Code: MEGA20
   - Discount type: percentage
   - Value: 20
   - Min value: 500000
   - Max discount: (để trống nếu không muốn giới hạn)

### Mã giảm theo số tiền cố định

1. **Giảm giá 50,000 VND cho đơn hàng từ 200,000 VND**:
   - Code: SALE50K
   - Discount type: fixed
   - Value: 50000
   - Min value: 200000

2. **Giảm giá 100,000 VND có số lượng giới hạn (10 lượt) cho đơn hàng từ 1,000,000 VND**:
   - Code: FLASH100K
   - Discount type: fixed
   - Value: 100000
   - Min value: 1000000
   - Max uses: 10

## 5. Theo dõi sử dụng mã giảm giá

- Theo dõi số lần sử dụng mã trong cột "Times used"
- Mã sẽ tự động ngừng hoạt động khi số lần sử dụng đạt đến "Max uses"
- Xem chi tiết các đơn hàng đã sử dụng mã trong phần QROrders

## 6. Một số mẹo quản lý mã giảm giá

- Tạo mã giảm giá có thời hạn để tạo cảm giác khẩn cấp
- Đặt tên mã dễ nhớ và liên quan đến chiến dịch
- Thiết lập giới hạn số tiền giảm giá tối đa đối với mã theo %
- Đối với mã có giá trị cao, nên giới hạn số lần sử dụng
- Đặt giá trị đơn hàng tối thiểu để khuyến khích khách hàng mua nhiều hơn
