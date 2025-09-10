from rest_framework import serializers
from .models import Order, OrderItem, Payment
from product.models import Product
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 
            'product', 
            'product_id', 
            'quantity', 
            'price', 
            'total_price'
        ]
        read_only_fields = ['id', 'price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'customer_email', 'total_amount', 'status', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total_amount = 0
        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            price = product.price
            quantity = item['quantity']
            total_price = price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price, total_price=total_price)
            total_amount += total_price
        order.total_amount = total_amount
        order.save()
        return order

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'payment_id', 'payment_method', 'amount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        order = Order.objects.get(id=validated_data['order_id'])
        payment = Payment.objects.create(
            order=order,
            amount=validated_data['amount'],
            payment_method=validated_data.get('payment_method', 'card'),
            status='success'
        )
        order.status = 'completed'
        order.save()
        return payment



