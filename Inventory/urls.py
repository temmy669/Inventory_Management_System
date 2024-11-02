"""
URL configuration for Inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="API DOCUMENTATION FOR INVENTORY MANAGEMENT SYSTEM",
        default_version='v1',
        description="The Inventory Management System API allows efficient management of products, suppliers, and stock levels. It includes endpoints for creating, updating, viewing, and deleting product and supplier records. Features include real-time stock tracking, background processing for automated tasks.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="temmy@waje.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('inventoryapp.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('suppliers.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)