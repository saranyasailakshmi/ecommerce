from django.urls import path
from .views import (
    OrderCreateAPIView,
    OrderDetailAPIView,
    OrderUpdateAPIView,
    OrderDeleteAPIView,
    PaymentCreateAPIView,
    PaymentDetailAPIView,
)

urlpatterns = [
    # Orders URLs
    
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('list/', OrderDetailAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/update/', OrderUpdateAPIView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrderDeleteAPIView.as_view(), name='order-delete'),

    # Payments URLs
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment-detail'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
]
