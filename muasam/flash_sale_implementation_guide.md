# Hướng Dẫn Triển Khai Chức Năng Flash Sale

Đây là hướng dẫn từng bước để triển khai chức năng Flash Sale vào trang web của bạn.

## Bước 1: Áp dụng Migration

Trước tiên, bạn cần áp dụng migration để tạo bảng FlashSale trong cơ sở dữ liệu:

```bash
python manage.py migrate
```

## Bước 2: Tạo dữ liệu mẫu

Bạn có thể tạo dữ liệu Flash Sale mẫu bằng script đã cung cấp:

```bash
python create_flash_sales.py
```

## Bước 3: Kiểm tra giao diện

1. Khởi động server Django:

```bash
python manage.py runserver
```

2. Truy cập trang chủ (http://localhost:8000) và kiểm tra phần Flash Sale
3. Xác nhận rằng bộ đếm ngược đang hoạt động đúng cách
4. Kiểm tra các nút điều hướng (trái/phải) để xem tất cả sản phẩm Flash Sale

## Bước 4: Quản lý Flash Sale trong Admin

1. Truy cập trang quản trị (http://localhost:8000/admin)
2. Điều hướng đến mục "Flash sales"
3. Bạn có thể thêm, sửa hoặc xóa các Flash Sale tại đây

## Tùy chỉnh thêm

### Thay đổi giao diện

Bạn có thể tùy chỉnh giao diện Flash Sale bằng cách chỉnh sửa CSS trong file `/home/static/styles.css`.

### Thêm ảnh icon Flash Sale

Để thêm icon Flash Sale, đặt một hình ảnh có tên là `flash-sale-icon.png` trong thư mục `/home/static/img/`.

### Tùy chỉnh thời gian Flash Sale

Mặc định, Flash Sale được tạo bằng script sẽ kéo dài 24 giờ. Bạn có thể điều chỉnh thời gian này trong file `create_flash_sales.py`.

## Xử lý Flash Sale trong quá trình thanh toán

Để Flash Sale hoạt động đầy đủ, bạn cần cập nhật phần xử lý giỏ hàng và thanh toán để:

1. Sử dụng giá Flash Sale thay vì giá gốc khi sản phẩm đang trong thời gian Flash Sale
2. Cập nhật số lượng đã bán sau khi thanh toán thành công

### Cập nhật hàm thêm vào giỏ hàng

Thêm mã sau vào view xử lý thêm sản phẩm vào giỏ hàng:

```python
from home.models import FlashSale
from django.utils import timezone

# Khi thêm sản phẩm vào giỏ hàng
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Kiểm tra xem sản phẩm có đang trong Flash Sale không
    flash_sale = FlashSale.objects.filter(
        product=product,
        is_active=True,
        start_time__lte=timezone.now(),
        end_time__gte=timezone.now()
    ).first()
    
    # Nếu có Flash Sale hợp lệ, sử dụng giá Flash Sale
    if flash_sale and flash_sale.get_remaining_items() > 0:
        price = flash_sale.sale_price
    else:
        price = product.price
    
    # Thêm sản phẩm vào giỏ hàng với giá đã xác định
    # ...
```

### Cập nhật số lượng đã bán

Sau khi thanh toán thành công:

```python
# Sau khi thanh toán thành công
def payment_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    # Cập nhật Flash Sale nếu có
    for item in order.items.all():
        flash_sale = FlashSale.objects.filter(
            product=item.product,
            is_active=True
        ).first()
        
        if flash_sale:
            flash_sale.sold_quantity += item.quantity
            flash_sale.save()
    
    # Xử lý thanh toán thành công
    # ...
```

## Lưu ý

- Đảm bảo kiểm tra tính hợp lệ của Flash Sale tại thời điểm thanh toán
- Flash Sale chỉ có hiệu lực khi còn hàng và trong thời gian hiệu lực
- Cần cập nhật số lượng đã bán khi người dùng hoàn thành đơn hàng
