from django import forms
from .models import Order
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



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Chỉ bao gồm tài khoản và mật khẩu