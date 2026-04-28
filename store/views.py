
from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    price_min = request.GET.get('min')
    price_max = request.GET.get('max')

    products = Product.objects.all().select_related('category')
    categories = Category.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category:
        products = products.filter(category__id=category)

    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    return render(request, 'home.html', {'products': products, 'categories': categories})
