from rest_framework import serializers
from .models import Category, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_featured"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  
    images = ProductImageSerializer(many=True, read_only=True)  
    created_by = serializers.StringRelatedField()  

    class Meta:
        model = Product
        fields = ["id","name","description","price","quantity","category","created_by","images","is_active","created_at","updated_at",]

    def get_price(self, obj):
        return f"₹{obj.price}"
    
