from rest_framework.routers import DefaultRouter

from .views import GoodsReceiptViewSet

router = DefaultRouter()

router.register(
    "",
    GoodsReceiptViewSet,
    basename="goods-receiving"
)

urlpatterns = router.urls