
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from store.models import Product
from .serializers import ProductSerializer

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    return Response(ProductSerializer(products, many=True).data)

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error':'username and password required'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error':'username already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({'status':'created','user_id':user.id})
