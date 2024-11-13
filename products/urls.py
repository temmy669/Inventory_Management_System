from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import upload_product_csv, ProductViewSet

router = DefaultRouter()

router.register(r'products', ProductViewSet)

urlpatterns= [
    path('', include(router.urls)),
    path('upload-product/', upload_product_csv.as_view(), name='upload-product-csv' )
]