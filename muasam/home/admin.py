from django.contrib import admin
from .models import Product, Order, Review, QROrder, QROrderItem

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

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review, ReviewAdmin)
admin.site.register(QROrder, QROrderAdmin)