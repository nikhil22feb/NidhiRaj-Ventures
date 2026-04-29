
from . import views
from django.urls import path
from .views import add_to_cart, cart_view, update_quantity, remove_item, checkout, verify_payment, my_orders, dashboard

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('update/<int:item_id>/<str:action>/', update_quantity),
    path('remove/<int:item_id>/', remove_item),
    path('checkout/', checkout, name='checkout'),
    path('verify-payment/', verify_payment, name='verify_payment'),
    path('my-orders/', my_orders, name='my_orders'),
    path('dashboard/', dashboard, name='dashboard'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.send_otp, name='resend_otp'),
    # path('create-admin/', views.create_admin),
]
