from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product
from . import validators


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "quantity"]


class CartItemSerializer(serializers.ModelSerializer):
    product_id = validators.product_id
    quantity = validators.quantity
    product = ProductSerializer(read_only=True)  # show product details
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "total_price"]

    def get_total_price(self, obj):
        """Calculate price × quantity for each cart item"""
        return obj.product.price * obj.quantity if obj.product else 0


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    final_amount = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "customer", "created_at", "updated_at", "items", "final_amount","customer_name"]
        read_only_fields = ["customer", "created_at", "updated_at"]

    def get_final_amount(self, obj):
        """Calculate sum of all cart item totals"""
        return sum([item.product.price * item.quantity for item in obj.items.all()])
