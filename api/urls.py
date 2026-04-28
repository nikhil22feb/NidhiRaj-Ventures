
from django.urls import path
from .views import product_list, signup
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('products/', product_list),
    path('signup/', signup),
    path('login/', TokenObtainPairView.as_view()),
]
