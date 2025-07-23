from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SignupView, ProductViewSet, CartView, AddToCartView,
    UpdateCartItemView, CheckoutView, OrderHistoryView,
    UserListView, AllOrdersView, UpdateOrderStatusView, DashboardStatsView
)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # include core app
    path('api/', include('core.urls')),
]

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema config
schema_view = get_schema_view(
    openapi.Info(
        title="🛍️ E-Commerce REST API",
        default_version='v1',
        description="This is the interactive API documentation for the E-Commerce Backend.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Product router
router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    # Auth
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Product API
    path('', include(router.urls)),

    # Cart & Orders
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/item/<int:item_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderHistoryView.as_view(), name='order-history'),

    # Admin APIs
    path('admin/users/', UserListView.as_view(), name='admin-users'),
    path('admin/orders/', AllOrdersView.as_view(), name='admin-orders'),
    path('admin/orders/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('admin/dashboard/', DashboardStatsView.as_view(), name='admin-dashboard'),

    # Swagger + Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
