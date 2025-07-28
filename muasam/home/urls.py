from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/review/', views.submit_review, name='submit_review'),
    path('order/<int:pk>/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('iphone/', views.iphone_products, name='iphone_products'),  # URL cho trang iPhone
    path('macbook/', views.macbook_products, name='macbook_products'),  # URL cho trang MacBook
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),  # Đăng ký
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Đăng nhập
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),  # Đăng xuất


    
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
]