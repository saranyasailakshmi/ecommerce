from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a cart for the logged-in customer"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            # Role check
            if request.user.role.lower() != "customer":
                context["message"] = "Only customers can create a cart."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            cart, created = Cart.objects.get_or_create(customer=request.user)
            serializer = CartSerializer(cart)
            context["success"] = 1
            context["message"] = "Cart created successfully" if created else "Cart already exists"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the logged-in customer's cart"""
        context = {"success": 0, "message": "Cart not found"}
        try:
            cart = get_object_or_404(Cart, customer=request.user)
            serializer = CartSerializer(cart)
            context["success"] = 1
            context["message"] = "Cart retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CartItemCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Add a product to the customer's cart"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            # Role check
            if request.user.role.lower() != "customer":
                context["message"] = "Only customers can add items to the cart."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            cart, _ = Cart.objects.get_or_create(customer=request.user)
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                product = serializer.validated_data["product"]
                quantity = serializer.validated_data["quantity"]

                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = quantity
                cart_item.save()

                context["success"] = 1
                context["message"] = "Item added to cart successfully"
                context["data"] = CartItemSerializer(cart_item).data
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context["message"] = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CartItemUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get details of a single cart item"""
        context = {"success": 0, "message": "Cart item not found"}
        try:
            cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
            serializer = CartItemSerializer(cart_item)
            context["success"] = 1
            context["message"] = "Cart item retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update quantity of a cart item"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
            serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context["success"] = 1
                context["message"] = "Cart item updated successfully"
                context["data"] = serializer.data
                return Response(context, status=status.HTTP_200_OK)
            else:
                context["message"] = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CartItemDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get details of a single cart item before deletion"""
        context = {"success": 0, "message": "Cart item not found"}
        try:
            cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
            serializer = CartItemSerializer(cart_item)
            context["success"] = 1
            context["message"] = "Cart item retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a cart item"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
            cart_item.delete()
            context["success"] = 1
            context["message"] = "Cart item deleted successfully"
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
