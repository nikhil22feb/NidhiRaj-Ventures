
from django.contrib import admin
from .models import Cart, CartItem, Order

admin.site.register(Cart)
admin.site.register(CartItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total_price','payment_method','status','is_paid','created_at')
    list_filter = ('payment_method','status','is_paid')
    search_fields = ('user__username',)
    list_editable = ('status',)
