from django import forms
from .models import Order, QROrder
from .models import Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'phone', 'quantity']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'name', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class QROrderForm(forms.ModelForm):
    class Meta:
        model = QROrder
        fields = ['customer_name', 'customer_email', 'customer_phone', 'customer_address']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Địa chỉ giao hàng'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Chỉ bao gồm tài khoản và mật khẩu