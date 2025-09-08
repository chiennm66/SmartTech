# Hướng Dẫn Triển Khai Chức Năng Flash Sale

Tài liệu này hướng dẫn chi tiết cách triển khai chức năng Flash Sale cho website thương mại điện tử của bạn. Flash Sale là chương trình khuyến mãi giảm giá mạnh trong thời gian giới hạn, tạo cảm giác khẩn cấp và thúc đẩy khách hàng mua sắm ngay lập tức.

![Flash Sale Example](https://via.placeholder.com/800x200?text=Flash+Sale+Example)

## Mục lục
1. [Tổng quan về chức năng](#tổng-quan-về-chức-năng)
2. [Các bước triển khai](#các-bước-triển-khai)
3. [Chi tiết từng bước](#chi-tiết-từng-bước)
   - [Bước 1: Tạo Model Flash Sale](#bước-1-tạo-model-flash-sale)
   - [Bước 2: Thêm Migration](#bước-2-thêm-migration)
   - [Bước 3: Cập nhật Views](#bước-3-cập-nhật-views)
   - [Bước 4: Thiết kế UI trên Template](#bước-4-thiết-kế-ui-trên-template)
   - [Bước 5: Thêm JavaScript cho đồng hồ đếm ngược](#bước-5-thêm-javascript-cho-đồng-hồ-đếm-ngược)
   - [Bước 6: Thiết kế CSS](#bước-6-thiết-kế-css)
   - [Bước 7: Đăng ký với Admin](#bước-7-đăng-ký-với-admin)
   - [Bước 8: Tạo dữ liệu mẫu](#bước-8-tạo-dữ-liệu-mẫu)
   - [Bước 9: Tích hợp với giỏ hàng](#bước-9-tích-hợp-với-giỏ-hàng)
   - [Bước 10: Cập nhật thanh toán](#bước-10-cập-nhật-thanh-toán)
4. [Kiểm thử](#kiểm-thử)
5. [Các cải tiến đề xuất](#các-cải-tiến-đề-xuất)
6. [Khắc phục sự cố](#khắc-phục-sự-cố)

## Tổng quan về chức năng

Chức năng Flash Sale bao gồm:
- Hiển thị sản phẩm giảm giá mạnh trong thời gian giới hạn
- Đồng hồ đếm ngược hiển thị thời gian còn lại
- Hiển thị giá gốc, giá giảm và phần trăm giảm giá
- Hiển thị số lượng sản phẩm còn lại
- Cập nhật số lượng đã bán khi thanh toán thành công
- Tự động vô hiệu hóa Flash Sale khi hết hạn hoặc hết hàng

## Các bước triển khai

1. Tạo Model Flash Sale
2. Thêm Migration
3. Cập nhật Views
4. Thiết kế UI trên Template
5. Thêm JavaScript cho đồng hồ đếm ngược
6. Thiết kế CSS
7. Đăng ký với Admin
8. Tạo dữ liệu mẫu
9. Tích hợp với giỏ hàng
10. Cập nhật thanh toán

## Chi tiết từng bước

### Bước 1: Tạo Model Flash Sale

Thêm model FlashSale vào file `models.py`:

```python
class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    discount_percentage = models.IntegerField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.IntegerField(default=1)
    sold_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Flash Sale: {self.product.name} - {self.discount_percentage}% off"
    
    def get_remaining_items(self):
        return self.available_quantity - self.sold_quantity
        
    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time and self.get_remaining_items() > 0
```

### Bước 2: Thêm Migration

Tạo file migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

Hoặc tạo file migration thủ công:

```python
# home/migrations/0010_add_flash_sale_model.py
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_merge_20250825_0705'),  # Điều chỉnh tùy theo migration cuối cùng của bạn
    ]

    operations = [
        migrations.CreateModel(
            name='FlashSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('discount_percentage', models.IntegerField()),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_quantity', models.IntegerField(default=1)),
                ('sold_quantity', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
            ],
        ),
    ]
```

### Bước 3: Cập nhật Views

Cập nhật view `home` trong `views.py` để hiển thị Flash Sale trên trang chủ:

```python
from .models import Product, Order, Cart, QROrder, QROrderItem, Coupon, FlashSale

def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)  # Hiển thị 6 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Lấy danh sách flash sale đang hoạt động
    active_flash_sales = FlashSale.objects.filter(
        is_active=True,
        start_time__lte=timezone.now(),
        end_time__gte=timezone.now()
    ).select_related('product')
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'flash_sales': active_flash_sales
    })
```

### Bước 4: Thiết kế UI trên Template

Thêm phần Flash Sale vào template `index.html` (sau phần navigation và trước danh sách sản phẩm chính):

```html
{% load static %}

{% if flash_sales %}
<div class="container">
  <div class="flash-sale-section">
    <div class="flash-sale-header">
      <div class="flash-sale-title">
        <img src="{% static 'img/flash-sale-icon.png' %}" onerror="this.src='https://via.placeholder.com/40x40?text=FLASH'" alt="Flash Sale">
        <h2>FLASH SALE</h2>
      </div>
      <div class="flash-sale-countdown" data-end-time="{{ flash_sales.0.end_time|date:'c' }}">
        <div>KẾT THÚC TRONG</div>
        <div class="countdown-box countdown-hours">00</div>
        <div class="countdown-separator">:</div>
        <div class="countdown-box countdown-minutes">00</div>
        <div class="countdown-separator">:</div>
        <div class="countdown-box countdown-seconds">00</div>
        <div class="flash-sale-time">
          <div>Đang diễn ra</div>
          <div>09:00 - 23:59</div>
        </div>
      </div>
    </div>
    
    <div class="flash-sale-container">
      <div class="flash-sale-items">
        {% for flash_sale in flash_sales %}
        <div class="flash-sale-item">
          <div class="discount-tag">-{{ flash_sale.discount_percentage }}%</div>
          <a href="{% url 'product_detail' flash_sale.product.pk %}">
            <img src="{{ flash_sale.product.image.url }}" alt="{{ flash_sale.product.name }}">
          </a>
          <div class="flash-sale-item-content">
            <div class="flash-sale-item-title">{{ flash_sale.product.name }}</div>
            <div class="flash-sale-item-price">
              <div class="sale-price">{{ flash_sale.sale_price|floatformat:0 }}đ</div>
              <div class="original-price">{{ flash_sale.original_price|floatformat:0 }}đ</div>
            </div>
            <div class="stock-info">
              <span>Còn {{ flash_sale.get_remaining_items }}/{{ flash_sale.available_quantity }}</span>
            </div>
            <div class="stock-progress">
              <div class="stock-progress-bar" style="width: {% widthratio flash_sale.sold_quantity flash_sale.available_quantity 100 %}%;"></div>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
      <div class="flash-sale-nav flash-sale-prev">&#10094;</div>
      <div class="flash-sale-nav flash-sale-next">&#10095;</div>
    </div>
  </div>
</div>
{% endif %}
```

Đảm bảo thêm `{% load static %}` ở đầu file template.

### Bước 5: Thêm JavaScript cho đồng hồ đếm ngược

Tạo file `flash_sale.js` trong thư mục `static/js/`:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Lấy tất cả bộ đếm ngược
    const countdownElements = document.querySelectorAll('.flash-sale-countdown');
    
    // Cập nhật đếm ngược mỗi giây
    function updateCountdowns() {
        countdownElements.forEach(element => {
            const endTime = new Date(element.dataset.endTime).getTime();
            const now = new Date().getTime();
            const timeRemaining = endTime - now;
            
            if (timeRemaining <= 0) {
                element.innerHTML = 'Flash Sale đã kết thúc!';
                return;
            }
            
            const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);
            
            element.querySelector('.countdown-hours').textContent = hours.toString().padStart(2, '0');
            element.querySelector('.countdown-minutes').textContent = minutes.toString().padStart(2, '0');
            element.querySelector('.countdown-seconds').textContent = seconds.toString().padStart(2, '0');
        });
    }
    
    // Cập nhật đếm ngược ngay lập tức và sau đó mỗi giây
    updateCountdowns();
    setInterval(updateCountdowns, 1000);
    
    // Xử lý trượt (slide) của carousel Flash Sale
    const prevButton = document.querySelector('.flash-sale-prev');
    const nextButton = document.querySelector('.flash-sale-next');
    const slideContainer = document.querySelector('.flash-sale-items');
    
    if (prevButton && nextButton && slideContainer) {
        const slideWidth = slideContainer.querySelector('.flash-sale-item')?.offsetWidth + 30 || 230; // 30 là margin
        const slidesCount = slideContainer.querySelectorAll('.flash-sale-item').length;
        const containerWidth = slideContainer.offsetWidth;
        const maxScroll = slidesCount * slideWidth - containerWidth;
        
        let currentScroll = 0;
        
        nextButton.addEventListener('click', function() {
            if (currentScroll < maxScroll) {
                currentScroll += slideWidth;
                if (currentScroll > maxScroll) currentScroll = maxScroll;
                slideContainer.scrollTo({
                    left: currentScroll,
                    behavior: 'smooth'
                });
            }
        });
        
        prevButton.addEventListener('click', function() {
            if (currentScroll > 0) {
                currentScroll -= slideWidth;
                if (currentScroll < 0) currentScroll = 0;
                slideContainer.scrollTo({
                    left: currentScroll,
                    behavior: 'smooth'
                });
            }
        });
    }
});
```

Thêm reference đến script này trong `base.html`:

```html
<script src="{% static 'js/flash_sale.js' %}"></script>
```

### Bước 6: Thiết kế CSS

Thêm CSS vào file `styles.css`:

```css
/* Flash Sale Styles */
.flash-sale-section {
    margin: 30px 0;
    background: #000;
    color: #fff;
    border-radius: 10px;
    padding: 20px;
    position: relative;
    overflow: hidden;
}

.flash-sale-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid #333;
    padding-bottom: 15px;
}

.flash-sale-title {
    display: flex;
    align-items: center;
}

.flash-sale-title img {
    height: 40px;
    margin-right: 15px;
}

.flash-sale-countdown {
    display: flex;
    align-items: center;
}

.countdown-box {
    background: #333;
    color: #fff;
    font-size: 24px;
    font-weight: bold;
    padding: 5px 10px;
    border-radius: 5px;
    margin: 0 3px;
}

.countdown-separator {
    font-size: 24px;
    font-weight: bold;
    margin: 0 2px;
}

.flash-sale-time {
    margin-left: 15px;
    font-size: 14px;
    opacity: 0.8;
}

.flash-sale-container {
    position: relative;
    overflow: hidden;
}

.flash-sale-items {
    display: flex;
    overflow-x: auto;
    scroll-behavior: smooth;
    scrollbar-width: none; /* Hide scrollbar Firefox */
    -ms-overflow-style: none; /* Hide scrollbar IE and Edge */
    gap: 15px;
    padding: 10px 0;
}

.flash-sale-items::-webkit-scrollbar {
    display: none; /* Hide scrollbar Chrome, Safari, Opera */
}

.flash-sale-item {
    flex: 0 0 auto;
    width: 200px;
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    color: #000;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s;
    position: relative;
}

.flash-sale-item:hover {
    transform: translateY(-5px);
}

.flash-sale-item img {
    width: 100%;
    height: 150px;
    object-fit: contain;
    background: #f5f5f5;
}

.flash-sale-item-content {
    padding: 15px;
}

.flash-sale-item-title {
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 10px;
    height: 40px;
    overflow: hidden;
}

.flash-sale-item-price {
    display: flex;
    flex-direction: column;
}

.sale-price {
    font-size: 16px;
    font-weight: bold;
    color: #ff4d4d;
}

.original-price {
    font-size: 12px;
    text-decoration: line-through;
    color: #999;
}

.discount-tag {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #ff4d4d;
    color: #fff;
    font-size: 12px;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 3px;
}

.stock-info {
    display: flex;
    align-items: center;
    margin-top: 10px;
    font-size: 12px;
    color: #666;
}

.stock-progress {
    height: 8px;
    background: #ddd;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 5px;
}

.stock-progress-bar {
    height: 100%;
    background: linear-gradient(to right, #ff9a9e, #ff4d4d);
}

.flash-sale-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    background: rgba(255,255,255,0.8);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 10;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.flash-sale-prev {
    left: 10px;
}

.flash-sale-next {
    right: 10px;
}
```

### Bước 7: Đăng ký với Admin

Đăng ký model FlashSale với Django Admin trong `admin.py`:

```python
from django.contrib import admin
from .models import Product, Order, Review, QROrder, QROrderItem, Coupon, FlashSale

class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'original_price_display', 'sale_price_display', 'start_time', 'end_time', 'stock_display', 'is_currently_active')
    list_filter = ('is_active', 'discount_percentage')
    search_fields = ('product__name',)
    
    def original_price_display(self, obj):
        return f"{int(obj.original_price):,} VND"
    original_price_display.short_description = 'Giá gốc'
    
    def sale_price_display(self, obj):
        return f"{int(obj.sale_price):,} VND"
    sale_price_display.short_description = 'Giá sale'
    
    def stock_display(self, obj):
        return f"{obj.get_remaining_items()}/{obj.available_quantity}"
    stock_display.short_description = 'Kho'
    
    def is_currently_active(self, obj):
        return obj.is_valid()
    is_currently_active.boolean = True
    is_currently_active.short_description = 'Đang hoạt động'

admin.site.register(FlashSale, FlashSaleAdmin)
```

### Bước 8: Tạo dữ liệu mẫu

Tạo file `create_flash_sales.py` để tạo dữ liệu mẫu:

```python
#!/usr/bin/env python
import os
import django
import random
from datetime import timedelta
from decimal import Decimal

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muasam.settings')
django.setup()

from django.utils import timezone
from home.models import Product, FlashSale

def create_flash_sales():
    """Tạo Flash Sales mẫu cho các sản phẩm hiện có"""
    # Lấy tất cả sản phẩm
    products = Product.objects.all()
    
    if not products:
        print("Không có sản phẩm nào trong cơ sở dữ liệu")
        return
    
    # Thời gian hiện tại
    now = timezone.now()
    
    # Xóa tất cả flash sale cũ
    FlashSale.objects.all().delete()
    
    # Tạo flash sale mới cho mỗi sản phẩm
    for product in products:
        # Chọn ngẫu nhiên một số sản phẩm để đưa vào flash sale
        if random.random() < 0.7:  # 70% sản phẩm sẽ có flash sale
            discount_percentage = random.choice([10, 15, 20, 25, 30, 40, 50])
            original_price = product.price
            sale_price = original_price * (1 - Decimal(discount_percentage) / 100)
            available_quantity = random.randint(5, 20)
            sold_quantity = random.randint(0, available_quantity - 1)
            
            # Tạo flash sale cho sản phẩm
            FlashSale.objects.create(
                product=product,
                start_time=now,
                end_time=now + timedelta(hours=24),  # Flash sale kéo dài 24 giờ
                discount_percentage=discount_percentage,
                original_price=original_price,
                sale_price=sale_price,
                available_quantity=available_quantity,
                sold_quantity=sold_quantity,
                is_active=True
            )
            print(f"Đã tạo Flash Sale cho sản phẩm: {product.name} với giảm giá {discount_percentage}%")
    
    print("\nĐã tạo xong các Flash Sale mẫu!")

if __name__ == '__main__':
    create_flash_sales()
```

### Bước 9: Tích hợp với giỏ hàng

Cập nhật hàm `add_to_cart` trong `views.py` để hỗ trợ giá Flash Sale:

```python
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
        
    # Kiểm tra xem sản phẩm có đang trong Flash Sale không
    flash_sale = FlashSale.objects.filter(
        product=product,
        is_active=True,
        start_time__lte=timezone.now(),
        end_time__gte=timezone.now()
    ).first()
    
    # Nếu có Flash Sale hợp lệ và còn hàng, sử dụng giá Flash Sale
    price = product.price
    if flash_sale and flash_sale.get_remaining_items() > 0:
        price = flash_sale.sale_price
    
    # Tạo hoặc cập nhật giỏ hàng với giá đã xác định
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')
```

Nếu muốn lưu giá lúc thêm vào giỏ hàng, cần cập nhật model Cart:

```python
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    session_key = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Thêm trường price
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * (self.price or self.product.price)
```

### Bước 10: Cập nhật thanh toán

Cập nhật xử lý thanh toán để cập nhật số lượng Flash Sale đã bán:

```python
@csrf_exempt
@require_http_methods(["POST"])
def check_payment_status(request, order_id):
    """API để kiểm tra trạng thái thanh toán (giả lập)"""
    try:
        order = QROrder.objects.get(order_id=order_id)
        
        # Trong thực tế, bạn sẽ tích hợp với API ngân hàng để kiểm tra thanh toán
        # Ở đây tôi giả lập việc thanh toán thành công sau 30 giây
        time_diff = timezone.now() - order.created_at
        if time_diff.total_seconds() > 30:  # Giả lập thanh toán thành công sau 30 giây
            order.status = 'paid'
            order.save()
            
            # Cập nhật số lượng đã bán trong Flash Sale
            for item in order.items.all():
                # Tìm flash sale đang hoạt động cho sản phẩm này
                flash_sales = FlashSale.objects.filter(
                    product=item.product,
                    is_active=True,
                )
                
                if flash_sales.exists():
                    flash_sale = flash_sales.first()
                    # Sử dụng F() để tránh race condition
                    from django.db.models import F
                    flash_sale.sold_quantity = F('sold_quantity') + item.quantity
                    flash_sale.save()
                    
                    # Kiểm tra lại để xem có hết hàng không
                    flash_sale.refresh_from_db()
                    if flash_sale.sold_quantity >= flash_sale.available_quantity:
                        flash_sale.is_active = False
                        flash_sale.save()
            
            return JsonResponse({'status': 'paid', 'message': 'Thanh toán thành công!'})
        else:
            return JsonResponse({'status': 'pending', 'message': 'Đang chờ thanh toán...'})
    except QROrder.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy đơn hàng'})
```

## Kiểm thử

Sau khi triển khai, thực hiện các bước kiểm thử sau:

1. Áp dụng migration:
   ```bash
   python manage.py migrate
   ```

2. Tạo dữ liệu mẫu:
   ```bash
   python create_flash_sales.py
   ```

3. Chạy server và kiểm tra trang chủ:
   ```bash
   python manage.py runserver
   ```

4. Kiểm tra các tính năng:
   - Hiển thị Flash Sale trên trang chủ
   - Đồng hồ đếm ngược hoạt động đúng
   - Nút điều hướng trái/phải hoạt động đúng
   - Thêm sản phẩm Flash Sale vào giỏ hàng với giá đã giảm
   - Thanh toán và xác minh số lượng đã bán được cập nhật

## Các cải tiến đề xuất

1. **Tối ưu hiệu suất**: Sử dụng caching để lưu trữ danh sách Flash Sale đang hoạt động.
2. **Thông báo hết hàng**: Hiển thị thông báo khi Flash Sale hết hàng.
3. **Đặt trước Flash Sale**: Cho phép đặt trước Flash Sale sắp diễn ra.
4. **Giới hạn số lượng mua**: Giới hạn số lượng sản phẩm Flash Sale mỗi người dùng có thể mua.
5. **Thông báo đẩy**: Gửi thông báo đẩy khi Flash Sale bắt đầu.

## Khắc phục sự cố

### Không hiển thị Flash Sale trên trang chủ
- Kiểm tra xem có Flash Sale nào đang hoạt động không
- Xác minh thời gian hệ thống
- Kiểm tra xem Flash Sale có còn hàng không

### Đồng hồ đếm ngược không hoạt động
- Kiểm tra JavaScript Console
- Xác minh định dạng thời gian end_time trong template

### Flash Sale hiển thị nhưng giá không được áp dụng
- Kiểm tra hàm add_to_cart đã được cập nhật chưa
- Xác nhận Flash Sale đang hoạt động và còn hàng

### Thanh toán không cập nhật số lượng đã bán
- Kiểm tra xử lý thanh toán
- Xác minh transaction có được commit đúng cách không

---

Theo dõi và phân tích hiệu quả của các Flash Sale để điều chỉnh chiến lược tiếp thị và giảm giá trong tương lai. Chức năng này sẽ giúp tăng tỷ lệ chuyển đổi và doanh số bán hàng đáng kể.
