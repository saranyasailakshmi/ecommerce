from django.urls import path
from .views import (
    CartCreateAPIView,
    CartDetailAPIView,
    CartItemCreateAPIView,
    CartItemUpdateAPIView,
    CartItemDeleteAPIView,
)

urlpatterns = [
    path("create/", CartCreateAPIView.as_view(), name="cart-create"),
    path("cart_items/", CartDetailAPIView.as_view(), name="cart-detail"),
    path("cart_items/add/", CartItemCreateAPIView.as_view(), name="cartitem-create"),
    path("cart_items/<int:pk>/", CartItemUpdateAPIView.as_view(), name="cartitem-update"),
    path("cart_items/<int:pk>/delete/", CartItemDeleteAPIView.as_view(), name="cartitem-delete"),
]
