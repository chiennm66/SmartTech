from django.db import models
from django.urls import reverse

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