from django.contrib import admin
from .models import Order, OrderItem, Payment

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__email', 'id')
    inlines = [OrderItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_id', 'payment_method', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order__id', 'payment_id', 'payment_method')
