from django.urls import path
from .views import CategoryAPIView
from django.urls import path
from .views import ProductAPIView
urlpatterns = [
   path('api/categories/', CategoryAPIView.as_view()),
   path("api/categories/<int:pk>/", CategoryAPIView.as_view()),
    # for product
    path("api/products/", ProductAPIView.as_view()),
    path("api/products/<int:pk>/", ProductAPIView.as_view()),
]
