from django.utils import timezone
from datetime import timedelta
from home.models import Coupon

# Mã giảm giá 10%
coupon1 = Coupon(
    code="WELCOME10",
    discount_type="percentage",
    value=10,
    min_value=100000,
    max_discount=100000,
    valid_from=timezone.now(),
    valid_to=timezone.now() + timedelta(days=30),
    max_uses=100,
    active=True
)
coupon1.save()

# Mã giảm giá 50k
coupon2 = Coupon(
    code="SALE50K",
    discount_type="fixed",
    value=50000,
    min_value=200000,
    valid_from=timezone.now(),
    valid_to=timezone.now() + timedelta(days=30),
    max_uses=50,
    active=True
)
coupon2.save()

# Mã giảm giá 20% có giới hạn tối đa
coupon3 = Coupon(
    code="MEGA20",
    discount_type="percentage",
    value=20,
    min_value=500000,
    max_discount=200000,
    valid_from=timezone.now(),
    valid_to=timezone.now() + timedelta(days=15),
    max_uses=30,
    active=True
)
coupon3.save()

# Mã giảm giá 100k có số lượng giới hạn
coupon4 = Coupon(
    code="FLASH100K",
    discount_type="fixed",
    value=100000,
    min_value=1000000,
    valid_from=timezone.now(),
    valid_to=timezone.now() + timedelta(days=7),
    max_uses=10,
    active=True
)
coupon4.save()

print("Đã tạo 4 mã giảm giá mẫu thành công!")
