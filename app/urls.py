from django.urls import path
from .views import CategoryAPIView
from django.urls import path
from .views import ProductListAPIView
urlpatterns = [
   path('api/categories/', CategoryAPIView.as_view()),
   path("api/categories/<int:pk>/", CategoryAPIView.as_view()),
    # for product
    path("api/products/", ProductListAPIView.as_view()),
    path("api/products/<int:pk>/", ProductListAPIView.as_view()),
]
