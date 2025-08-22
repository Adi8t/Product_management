from django.urls import path
from .views import CategoryAPIView
urlpatterns = [
   path('api/categories/', CategoryAPIView.as_view()),
   path("api/categories/<int:pk>/", CategoryAPIView.as_view())
]