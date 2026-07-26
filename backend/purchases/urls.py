from rest_framework.routers import DefaultRouter

from .views import PurchaseItemViewSet, PurchaseViewSet

router = DefaultRouter()

router.register(
    r"purchases",
    PurchaseViewSet,
    basename="purchase",
)

router.register(
    r"purchase-items",
    PurchaseItemViewSet,
    basename="purchase-item",
)

urlpatterns = router.urls