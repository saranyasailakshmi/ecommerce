from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, Payment, OrderItem,Product
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from .validators import OrderValidator, PaymentValidator


# ORDERS

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "customer":
            return Response({"success": 0, "message": "Only customers can place orders."}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response({"success": 1, "message": "Order created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "customer":
            orders = Order.objects.filter(customer=request.user).prefetch_related("items__product")
        else:
            orders = Order.objects.filter(items__product__created_by=request.user).distinct().prefetch_related("items__product")

        serializer = OrderSerializer(orders, many=True)
        return Response(
            {"success": 1, "message": "Orders retrieved successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class OrderUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get a single order details"""
        context = {"success": 0, "message": "Order not found"}
        try:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order)
            context["success"] = 1
            context["message"] = "Order retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update an order (customer only, if not paid)"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            order = get_object_or_404(Order, pk=pk)
            if request.user.role != "customer" or order.customer != request.user:
                context["message"] = "You do not have permission to update this order."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            if order.status != "pending":
                context["message"] = "Cannot update order once processed."
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            validator = OrderValidator(data=request.data, partial=True)
            if validator.is_valid():
                order.status = validator.validated_data.get("status", order.status)
                order.total_amount = validator.validated_data.get("total_amount", order.total_amount)
                order.save()
                serializer = OrderSerializer(order)
                context["success"] = 1
                context["message"] = "Order updated successfully"
                context["data"] = serializer.data
                return Response(context, status=status.HTTP_200_OK)
            else:
                context["message"] = validator.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get order details before deletion"""
        context = {"success": 0, "message": "Order not found"}
        try:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order)
            context["success"] = 1
            context["message"] = "Order retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete an order (customer only, if not paid)"""
        context = {"success": 0, "message": "Something went wrong"}
        try:
            order = get_object_or_404(Order, pk=pk)
            if request.user.role != "customer" or order.customer != request.user:
                context["message"] = "You do not have permission to delete this order."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            if order.status != "pending":
                context["message"] = "Cannot delete order once processed."
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            order.delete()
            context["success"] = 1
            context["message"] = "Order deleted successfully"
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


# PAYMENTS

class PaymentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retrieve payment details"""
        context = {"success": 0, "message": "Payment not found"}
        try:
            payment = get_object_or_404(Payment, pk=pk)
            if request.user.role != "customer" or payment.order.customer != request.user:
                context["message"] = "You do not have permission to view this payment."
                return Response(context, status=status.HTTP_403_FORBIDDEN)

            serializer = PaymentSerializer(payment)
            context["success"] = 1
            context["message"] = "Payment retrieved successfully"
            context["data"] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "customer":
            return Response({"success": 0, "message": "Only customers can make payments."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({"success": 1, "message": "Payment processed successfully", "data": PaymentSerializer(payment).data}, status=status.HTTP_201_CREATED)
        return Response({"success": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
