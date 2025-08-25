from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('iphone', 'iPhone'),
        ('macbook', 'MacBook'),
        ('accessory', 'Phụ Kiện'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='iphone')  # Thêm trường phân loại
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Lựa chọn từ 1 đến 5 sao
    name = models.CharField(max_length=255)  # Tên người đánh giá
    comment = models.TextField()  # Nhận xét của người đánh giá

    def __str__(self):
        return f'{self.name} - {self.rating} sao'  # Hiển thị tên và số sao đánh giá

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order for {self.product.name} by {self.name}"
    
    
### Thêm mô hình giỏ hàng
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    session_key = models.CharField(max_length=255)  # Dùng để liên kết với session người dùng

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

### Thêm mô hình đơn hàng QR
### Mã giảm giá
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=[
        ('percentage', 'Phần trăm'),
        ('fixed', 'Số tiền cố định')
    ])
    value = models.DecimalField(max_digits=10, decimal_places=2)  # Giá trị giảm giá
    min_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Giá trị đơn hàng tối thiểu
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Giảm giá tối đa (cho % giảm giá)
    valid_from = models.DateTimeField(default=timezone.now)  # Thời gian bắt đầu hiệu lực
    valid_to = models.DateTimeField()  # Thời gian kết thúc hiệu lực
    max_uses = models.IntegerField(default=1)  # Số lần sử dụng tối đa
    times_used = models.IntegerField(default=0)  # Số lần đã được sử dụng
    active = models.BooleanField(default=True)  # Trạng thái kích hoạt

    def __str__(self):
        if self.discount_type == 'percentage':
            return f"{self.code} - {self.value}%"
        return f"{self.code} - {self.value} VND"
    
    def is_valid(self):
        now = timezone.now()
        if not self.active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.times_used >= self.max_uses:
            return False
        return True
    
    def calculate_discount(self, total_amount):
        if not self.is_valid() or total_amount < self.min_value:
            return 0
        
        if self.discount_type == 'percentage':
            discount = total_amount * (self.value / 100)
            if self.max_discount and discount > self.max_discount:
                discount = self.max_discount
        else:  # fixed amount
            discount = self.value
            
        return discount

### Thêm mô hình đơn hàng QR
class QROrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('cancelled', 'Đã hủy'),
    ]
    order_id = models.CharField(max_length=50, unique=True)
    session_key = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    qr_content = models.TextField()  # Nội dung mã QR
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Thêm trường coupon
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Số tiền giảm giá
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Số tiền trước khi giảm giá
    
    def __str__(self):
        return f"Order {self.order_id} - {self.total_amount} VND"

class QROrderItem(models.Model):
    qr_order = models.ForeignKey(QROrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.price