# products/validators.py
from rest_framework import serializers

class ProductValidator(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        max_length=200,
        error_messages={
            "required": "Product name is required.",
            "max_length": "Product name cannot exceed 200 characters.",
            "blank": "Product name cannot be blank."
        }
    )
    description = serializers.CharField(
        required=True,
        error_messages={
            "required": "Description is required.",
            "blank": "Description cannot be blank."
        }
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={
            "required": "Price is required.",
            "invalid": "Enter a valid price."
        }
    )
    quantity = serializers.IntegerField(
        required=True,
        min_value=0,
        error_messages={
            "required": "Quantity is required.",
            "invalid": "Enter a valid quantity.",
            "min_value": "Quantity cannot be negative."
        }
    )
    category = serializers.CharField(
        required=True,
        error_messages={
            "required": "Category is required.",
            "blank": "Category cannot be blank."
        }
    )

class ProductImageValidator(serializers.Serializer):
    product = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "Product is required.",
            "invalid": "Enter a valid product ID."
        }
    )
    image = serializers.ImageField(
        required=True,
        error_messages={
            "required": "Product image is required.",
            "invalid": "Upload a valid image file."
        }
    )
    alt_text = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
        error_messages={
            "max_length": "Alt text cannot exceed 255 characters."
        }
    )
    is_featured = serializers.BooleanField(
        required=False,
        default=False,
        error_messages={
            "invalid": "Enter a valid boolean value."
        }
    )
