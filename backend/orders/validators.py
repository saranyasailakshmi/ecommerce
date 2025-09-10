from rest_framework import serializers
from .models import Order, Payment, Product

class OrderValidator(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
        error_messages={
            "required": "Product is required.",
            "does_not_exist": "Selected product does not exist.",
            "incorrect_type": "Invalid product ID."
        }
    )
    quantity = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "Quantity is required.",
            "invalid": "Enter a valid quantity.",
            "min_value": "Quantity must be at least 1."
        }
    )

class PaymentValidator(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        required=True,
        error_messages={
            "required": "Order is required.",
            "does_not_exist": "Selected order does not exist.",
            "incorrect_type": "Invalid order ID."
        }
    )
    payment_method = serializers.ChoiceField(
        choices=[('card', 'Card'), ('upi', 'UPI'), ('netbanking', 'NetBanking')],
        required=True,
        error_messages={
            "required": "Payment method is required.",
            "invalid_choice": "Select a valid payment method."
        }
    )
