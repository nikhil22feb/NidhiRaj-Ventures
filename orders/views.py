from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Order, Wishlist
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from store.models import Product, Category
import razorpay, json
from .forms import LoginForm
import random
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
import re



def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, "home.html", {
        "products": products,
        "categories": categories
    })

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    cart = _get_cart(request.user)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart')

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    cart = _get_cart(request.user)
    items = CartItem.objects.filter(cart=cart).select_related('product')
    total = sum(i.product.price * i.quantity for i in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)
    if action == 'inc':
        item.quantity += 1
    elif action == 'dec':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect('cart')
    item.save()
    return redirect('cart')

def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

def checkout(request):
    items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.product.price * item.quantity for item in items)

    if total <= 0:
        return render(request, "cart.html", {"error": "Cart is empty"})

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

    amount = max(total * 100, 100)

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "payment.html", {
        "order_id": order["id"],
        "amount": amount,
        "key": settings.RAZORPAY_KEY
    })

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "product_detail.html", {"product": product})


def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)

    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Invalid credentials'
                })

    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # 🔴 Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/signup/')

        # 🔴 Password checks
        if len(password) < 6:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('/signup/')

        if not re.search(r'[A-Z]', password):
            messages.error(request, "Password must contain uppercase letter")
            return redirect('/signup/')

        if not re.search(r'[0-9]', password):
            messages.error(request, "Password must contain number")
            return redirect('/signup/')

        # ✅ Create user (inactive until verified)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False   # 🔒 important
        )

        # ✅ SAVE EMAIL IN SESSION (for OTP)
        request.session['email'] = email

        # ✅ GENERATE OTP
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp

        # ✅ SEND OTP EMAIL
        send_mail(
            'OTP Verification - NidhiRaj Ventures',
            f'Your OTP is {otp}',
            'noreply@nidhirajventures.com',
            [email],
            fail_silently=False,
        )

        # 🚀 REDIRECT TO OTP PAGE
        return redirect('/resend-otp/')

    return render(request, 'signup.html')

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            # ✅ Payment is valid
            items = CartItem.objects.filter(cart__user=request.user)
            total = sum(item.product.price * item.quantity for item in items)

            Order.objects.create(
                user=request.user,
                total_price=total,
                payment_method="ONLINE",
                is_paid=True
            )

            items.delete()

            return JsonResponse({"status": "success"})

        except:
            return JsonResponse({"status": "failed"})

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})


# 📤 SEND OTP
def send_otp(request):
    email = request.session.get('email')

    otp = random.randint(100000, 999999)
    request.session['otp'] = otp

    send_mail(
        'Your OTP - NidhiRaj Ventures',
        f'Your OTP is {otp}',
        'noreply@nidhiraj.com',
        [email],
        fail_silently=False,
    )

    return render(request, 'verify_otp.html')


def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@nidhirajventures.in',
            password='Admin@123'
        )
        return HttpResponse("Admin created ✅")
    return HttpResponse("Admin already exists")


# ✅ VERIFY OTP
def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        real_otp = request.session.get('otp')
        email = request.session.get('email')

        if str(user_otp) == str(real_otp):
            user = User.objects.filter(email=email).last()
            user.is_active = True
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # ✅ login after verification
            return redirect('/')

        else:
            return HttpResponse("Invalid OTP ❌")

# Simple dashboard (last 7 days revenue)
from django.db.models import Sum
from django.utils.timezone import now
import datetime

def dashboard(request):
    labels, data = [], []
    for i in range(7):
        day = now() - datetime.timedelta(days=i)
        total = Order.objects.filter(created_at__date=day.date(), is_paid=True)                             .aggregate(Sum('total_price'))['total_price__sum'] or 0
        labels.append(day.strftime('%d %b'))
        data.append(total)
    return render(request, 'dashboard.html', {'labels': list(reversed(labels)), 'data': list(reversed(data))})
