from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Order, Cart
from .forms import OrderForm, ReviewForm
from django.http import HttpResponseNotFound
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.sessions.models import Session


def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)  # Hiển thị 6 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})  # Truyền page_obj vào template
     #{'page_obj': page_obj}
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def place_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'product': product, 'form': form})

def order_success(request):
    return render(request, 'order_success.html')


def about(request):
    return render(request, 'about.html')

def contact(request):
    products = Product.objects.all()
    return render(request, 'contact.html', {'products': products})


def submit_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', pk=pk)
    return redirect('product_detail', pk=pk)


def iphone_products(request):
    products = Product.objects.filter(category='iphone')  # Lọc sản phẩm thuộc danh mục iPhone
    return render(request, 'iphone.html', {'products': products})


def macbook_products(request):
    products = Product.objects.filter(category='macbook')  # Lọc sản phẩm thuộc danh mục MacBook
    return render(request, 'macbook.html', {'products': products})




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản {username} đã được tạo thành công! Bạn có thể đăng nhập.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})  # Đảm bảo tên template là 'register.html'


def custom_404(request, exception):
    # Kiểm tra nếu URL thuộc admin, không áp dụng custom 404
    if request.path.startswith('/admin/'):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, '404.html', status=404)

# cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('view_cart')