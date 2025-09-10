from django.contrib import admin
from .models import Category, Product, ProductImage

# Inline for ProductImage in Product admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to display
    fields = ("image", "alt_text", "is_featured")
    readonly_fields = ("image",)  # optional: make image readonly if you don't want to edit in admin

# Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity", "created_by", "is_active", "created_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "description", "category__name")
    inlines = [ProductImageInline]
    readonly_fields = ("created_at", "updated_at")

# Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

# Optional: ProductImage admin if you want to manage images separately
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "alt_text", "is_featured")
    list_filter = ("is_featured",)
    search_fields = ("product__name", "alt_text")
