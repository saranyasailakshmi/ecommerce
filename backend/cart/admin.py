from django.contrib import admin
from .models import Cart,CartItem

# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ("product", "quantity")  # optional: make read-only


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at", "updated_at")
    search_fields = ("customer__username", "customer__email")
    list_filter = ("created_at", "updated_at")
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
    search_fields = ("cart__customer__username", "product__name")
    list_filter = ("cart__created_at",)