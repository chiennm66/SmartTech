from django.contrib import admin
from .models import Product, Order, Review, QROrder, QROrderItem, Coupon
from django.utils import timezone

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'comment')
    search_fields = ('product__name', 'name', 'rating')
    list_filter = ('rating',)

class QROrderItemInline(admin.TabularInline):
    model = QROrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'get_total_price')

class QROrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'customer_name', 'customer_email')
    readonly_fields = ('order_id', 'session_key', 'qr_content', 'created_at', 'updated_at')
    inlines = [QROrderItemInline]
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('order_id', 'status', 'total_amount')
        }),
        ('Thông tin khách hàng', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Thông tin hệ thống', {
            'fields': ('session_key', 'qr_content', 'created_at', 'updated_at')
        }),
    )

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_display', 'is_active', 'valid_from', 'valid_to', 'times_used', 'max_uses', 'min_value_display')
    list_filter = ('active', 'discount_type')
    search_fields = ('code',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        help_text = """
        <strong>Hướng dẫn tạo mã giảm giá:</strong><br/>
        - <strong>Code</strong>: Mã code giảm giá (ví dụ: WELCOME10, SALE50K)<br/>
        - <strong>Discount type</strong>: Chọn loại giảm giá (percentage: theo %, fixed: số tiền cố định)<br/>
        - <strong>Value</strong>: Giá trị giảm giá (nếu là % thì nhập số %, nếu là số tiền cố định thì nhập số tiền)<br/>
        - <strong>Min value</strong>: Giá trị đơn hàng tối thiểu để áp dụng mã giảm giá (VND)<br/>
        - <strong>Max discount</strong>: Giới hạn số tiền giảm giá tối đa (chỉ áp dụng cho loại giảm giá theo %)<br/>
        - <strong>Valid from/to</strong>: Thời gian hiệu lực của mã giảm giá<br/>
        - <strong>Max uses</strong>: Số lần sử dụng tối đa<br/>
        <a href="/admin/coupon-guide/" target="_blank">Xem hướng dẫn đầy đủ</a>
        """
        form.base_fields['code'].help_text = help_text
        return form
    
    fieldsets = (
        ('Thông tin mã giảm giá', {
            'fields': ('code', 'discount_type', 'value', 'min_value', 'max_discount', 'active')
        }),
        ('Thời gian và lượt sử dụng', {
            'fields': ('valid_from', 'valid_to', 'max_uses', 'times_used')
        }),
    )
    
    def discount_display(self, obj):
        if obj.discount_type == 'percentage':
            return f"{obj.value}%"
        return f"{int(obj.value):,} VND"
    discount_display.short_description = 'Giảm giá'
    
    def min_value_display(self, obj):
        return f"{int(obj.min_value):,} VND"
    min_value_display.short_description = 'Đơn hàng tối thiểu'
    
    def is_active(self, obj):
        now = timezone.now()
        if not obj.active:
            return False
        if now < obj.valid_from or now > obj.valid_to:
            return False
        if obj.times_used >= obj.max_uses:
            return False
        return True
    is_active.boolean = True
    is_active.short_description = 'Còn hiệu lực'

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review, ReviewAdmin)
admin.site.register(QROrder, QROrderAdmin)
admin.site.register(Coupon, CouponAdmin)