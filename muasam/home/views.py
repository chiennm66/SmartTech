from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Order, Cart, QROrder, QROrderItem
from .forms import OrderForm, ReviewForm, QROrderForm
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.sessions.models import Session
import qrcode
from io import BytesIO
import base64
import uuid
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


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





# QR Payment Views
def qr_checkout(request):
    """Hiển thị form thông tin khách hàng trước khi tạo mã QR"""
    session_key = request.session.session_key
    if not session_key:
        messages.error(request, 'Phiên làm việc không hợp lệ. Vui lòng thêm sản phẩm vào giỏ hàng.')
        return redirect('view_cart')
    
    cart_items = Cart.objects.filter(session_key=session_key)
    if not cart_items.exists():
        messages.error(request, 'Giỏ hàng trống. Vui lòng thêm sản phẩm trước khi thanh toán.')
        return redirect('view_cart')
    
    total_price = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        form = QROrderForm(request.POST)
        if form.is_valid():
            # Tạo đơn hàng mới
            order = form.save(commit=False)
            order.order_id = f"QR{uuid.uuid4().hex[:8].upper()}"
            order.session_key = session_key
            order.total_amount = total_price
            
            # Tạo nội dung mã QR (thông tin chuyển khoản)
            bank_info = {
                "bank": "Vietcombank",
                "account": "1234567890",
                "name": "SMARTTECH STORE",
                "amount": str(total_price),
                "description": f"Thanh toan don hang {order.order_id}"
            }
            order.qr_content = json.dumps(bank_info, ensure_ascii=False)
            order.save()
            
            # Tạo các item của đơn hàng
            for cart_item in cart_items:
                QROrderItem.objects.create(
                    qr_order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Xóa giỏ hàng sau khi tạo đơn hàng
            cart_items.delete()
            
            return redirect('qr_payment', order_id=order.order_id)
    else:
        form = QROrderForm()
    
    return render(request, 'qr_checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })

def qr_payment(request, order_id):
    """Hiển thị mã QR thanh toán"""
    order = get_object_or_404(QROrder, order_id=order_id)
    
    # Tạo mã QR
    qr_data = order.qr_content
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Tạo hình ảnh QR
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Chuyển đổi thành base64 để hiển thị trên web
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Parse thông tin ngân hàng từ QR content
    bank_info = json.loads(order.qr_content)
    
    return render(request, 'qr_payment.html', {
        'order': order,
        'qr_image': qr_image_base64,
        'bank_info': bank_info
    })

@csrf_exempt
@require_http_methods(["POST"])
def check_payment_status(request, order_id):
    """API để kiểm tra trạng thái thanh toán (giả lập)"""
    try:
        order = QROrder.objects.get(order_id=order_id)
        
        # Trong thực tế, bạn sẽ tích hợp với API ngân hàng để kiểm tra thanh toán
        # Ở đây tôi giả lập việc thanh toán thành công sau 30 giây
        time_diff = timezone.now() - order.created_at
        if time_diff.total_seconds() > 30:  # Giả lập thanh toán thành công sau 30 giây
            order.status = 'paid'
            order.save()
            return JsonResponse({'status': 'paid', 'message': 'Thanh toán thành công!'})
        else:
            return JsonResponse({'status': 'pending', 'message': 'Đang chờ thanh toán...'})
    except QROrder.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy đơn hàng'})
    





def payment_success(request, order_id):
    """Trang thông báo thanh toán thành công"""
    order = get_object_or_404(QROrder, order_id=order_id)
    if order.status != 'paid':
        messages.warning(request, 'Đơn hàng chưa được thanh toán.')
        return redirect('qr_payment', order_id=order_id)
    
    return render(request, 'payment_success.html', {'order': order})