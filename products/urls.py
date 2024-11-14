from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import upload_product_csv, ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Define the upload endpoint using re_path for regex pattern
    re_path(r'upload/', upload_product_csv.as_view(), name='upload-product-csv'),
]
