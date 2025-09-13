from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from app.serializer import CategorySerializer, ProductSerializer
from app.models import Category, Product
from rest_framework.pagination import LimitOffsetPagination


# -----------------------------
# Category API
# -----------------------------
class CategoryAPIView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE category
    def put(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE category
    def delete(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# -----------------------------
# Product API
# -----------------------------


from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q

class ProductListAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        # filters ...
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_qs = paginator.paginate_queryset(queryset, request, view=self)
        serializer = ProductSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)


    # CREATE product
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE product
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE product
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
