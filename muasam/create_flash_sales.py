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
