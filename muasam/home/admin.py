from django.contrib import admin
from .models import Product, Order, Review



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'comment')
    search_fields = ('product__name', 'name', 'rating')
    list_filter = ('rating',)


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)