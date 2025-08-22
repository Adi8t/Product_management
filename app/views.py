from rest_framework.response import Response
from app.serializer import CategorySerializer
from rest_framework.views import APIView

from app.models import Category
class CategoryAPIView(APIView):
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)