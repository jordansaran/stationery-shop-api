"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from people.views import ClientViewSet, SellerViewSet
from products.views import ProductViewSet
from sales.views import SaleViewSet

router = routers.DefaultRouter()
router.register(r'client', ClientViewSet, basename="client")
router.register(r'seller', SellerViewSet, basename="seller")
router.register(r'product', ProductViewSet, basename="product")
router.register(r'sale', SaleViewSet, basename="sale")


schema_view = get_schema_view(
   openapi.Info(
      title="Stationery Shop API",
      default_version='v1.0.4',
      description="Stationery Shop API",
      terms_of_service="",
      contact=openapi.Contact(email="contato@jordanferreirasaran.com.br"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('doc/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
