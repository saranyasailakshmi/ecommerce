# products/urls.py
from django.urls import path
from .views import (
    ProductCreateAPIView,ProductListAPIView,ProductDetailAPIView,
    ProductUpdateAPIView,ProductDeleteAPIView,CategoryCreateAPIView,
    CategoryListAPIView,ProductImageUploadAPIView,

)

urlpatterns = [
    path("create/", ProductCreateAPIView.as_view(), name="product-create"),
    path("list/", ProductListAPIView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("update/<int:pk>/", ProductUpdateAPIView.as_view(), name="product-update"),
    path("delete/<int:pk>/", ProductDeleteAPIView.as_view(), name="product-delete"),
    path("<int:product_id>/images/", ProductImageUploadAPIView.as_view(), name="product-upload-images"),
    path("categories/list/", CategoryListAPIView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateAPIView.as_view(), name="category-create"),

]
