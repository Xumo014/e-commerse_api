from . import signals
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from products.services import FlashSaleListCreateView, check_flash_sale, ProductViewHistoryCreate, admin_replanish_stock
from products.views import ProductViewSet, CategoryViewSet, ReviewViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
    path('product_view/', ProductViewHistoryCreate.as_view(), name='product_view_history_create'),
    path('check_sale/<int:product_id>/', check_flash_sale, name='check_flash_sale'),

    path('admin/replenish_stock/<int:product_id>/<int:amount>', admin_replanish_stock, name='admin_replanish_stock'),
]
