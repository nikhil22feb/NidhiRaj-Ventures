
from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Packed','Packed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
    ]
    PAYMENT_CHOICES = [
        ('COD','Cash on Delivery'),
        ('ONLINE','Online'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    razorpay_order_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
