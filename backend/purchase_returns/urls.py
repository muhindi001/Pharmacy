from rest_framework.routers import DefaultRouter

from .views import (
    PurchaseReturnViewSet,
    PurchaseReturnItemViewSet,
)

router = DefaultRouter()

router.register(
    r"purchase-returns",
    PurchaseReturnViewSet,
)

router.register(
    r"purchase-return-items",
    PurchaseReturnItemViewSet,
)

urlpatterns = router.urls