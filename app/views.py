from rest_framework.response import Response
from app.serializer import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from app.models import Category, Product


class CategoryAPIView(APIView):
    # GET all categories
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    # CREATE category
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # UPDATE category
    def put(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"})

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # DELETE category
    def delete(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"})

        category.delete()
        return Response({"message": "Category deleted successfully"})



# for Crud api product 

class ProductAPIView(APIView):
    def get(self, request, pk):
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user) 
            return Response(serializer.data)
        return Response(serializer.errors,)

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, )

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({"message": "Product deleted"})