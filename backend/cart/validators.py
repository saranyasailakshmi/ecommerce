from rest_framework import serializers
from product.models import Product


quantity = serializers.IntegerField(
    required=True,
    min_value=1,
    error_messages={
        "required": "Quantity is required.",
        "invalid": "Enter a valid quantity.",
        "min_value": "Quantity must be at least 1."
    }
)

product_id = serializers.PrimaryKeyRelatedField(
    queryset=Product.objects.all(),
    required=True,
    error_messages={
        "required": "Product is required.",
        "does_not_exist": "The selected product does not exist.",
        "incorrect_type": "Invalid product ID."
    }
)
