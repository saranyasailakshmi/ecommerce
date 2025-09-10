from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product, Category,ProductImage 
from .serializers import ProductSerializer,CategorySerializer,ProductImageSerializer
from .validators import ProductValidator
from rest_framework.parsers import MultiPartParser,FormParser

class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a new product (seller only)"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            if request.user.role != "seller":
                context["message"] = "Only sellers can add products."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            validator = ProductValidator(data=request.data)
            if validator.is_valid():
                category = get_object_or_404(Category, id=validator.validated_data["category"])
                product = Product.objects.create(
                    name=validator.validated_data["name"],
                    description=validator.validated_data["description"],
                    price=validator.validated_data["price"],
                    quantity=validator.validated_data["quantity"],
                    category=category,
                    created_by=request.user
                )
                serializer = ProductSerializer(product)
                context["success"] = 1
                context["message"] = "Product created successfully"
                context["data"] = serializer.data
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context["message"] = validator.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all products (customer and seller)"""
        context = {"success": 0, "message": "No products found", "data": []}
        try:
            if request.user.role == "seller":
                # Seller sees only their products
                products = Product.objects.filter(created_by=request.user, is_active=True)
            else:
                # Customer sees all products
                products = Product.objects.filter(is_active=True)

            serializer = ProductSerializer(products, many=True)
            context["success"] = 1
            context["message"] = "Products retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=200)

        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=400)
        

class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get complete information of a single product"""
        context = {"success": 0, "message": "Product not found", "data": None}
        try:
            product = get_object_or_404(Product, pk=pk, is_active=True)
            serializer = ProductSerializer(product)
            context["success"] = 1
            context["message"] = "Product retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=200)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=400)
        

class ProductUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get a single product details"""
        context = {"success": 0, "message": "Product not found"}
        try:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            context["success"] = 1
            context["message"] = "Product retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update a product (seller only)"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            product = get_object_or_404(Product, pk=pk)

            if request.user.role != "seller" or product.created_by != request.user:
                context["message"] = "You do not have permission to update this product."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            validator = ProductValidator(data=request.data)
            if validator.is_valid():
                category = get_object_or_404(Category, id=validator.validated_data["category"])
                product.name = validator.validated_data["name"]
                product.description = validator.validated_data["description"]
                product.price = validator.validated_data["price"]
                product.quantity = validator.validated_data["quantity"]
                product.category = category
                product.save()
                serializer = ProductSerializer(product)
                context["success"] = 1
                context["message"] = "Product updated successfully"
                context["data"] = serializer.data
                return Response(context, status=status.HTTP_200_OK)
            else:
                context["message"] = validator.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get a single product details"""
        context = {"success": 0, "message": "Product not found"}
        try:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            context["success"] = 1
            context["message"] = "Product retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a product (seller only)"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            product = get_object_or_404(Product, pk=pk)

            if request.user.role != "seller" or product.created_by != request.user:
                context["message"] = "You do not have permission to delete this product."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            product.delete()
            context["success"] = 1
            context["message"] = "Product deleted successfully"
            return Response(context, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all categories"""
        context = {"success": 0, "message": "No categories found", "data": []}
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            context["success"] = 1
            context["message"] = "Categories retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=200)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=400)


class CategoryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            name = request.data.get("name")
            description = request.data.get("description", "")

            if not name:
                return Response({"success": 0, "message": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

            category = Category.objects.create(name=name, description=description)
            serializer = CategorySerializer(category)
            return Response({"success": 1, "data": serializer.data, "message": "Category created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class ProductImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Important for file uploads

    def post(self, request, product_id):
        """Upload one or more images for a product"""
        try:
            product = Product.objects.get(pk=product_id)
            if request.user != product.created_by:
                return Response({"success": 0, "message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            files = request.FILES.getlist("images")
            if not files:
                return Response({"success": 0, "message": "No images uploaded"}, status=status.HTTP_400_BAD_REQUEST)

            for f in files:
                ProductImage.objects.create(product=product, image=f)

            return Response({"success": 1, "message": "Images uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"success": 0, "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
