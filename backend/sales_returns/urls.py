from rest_framework.routers import DefaultRouter

from .views import (
    SalesReturnViewSet,
    SalesReturnItemViewSet,
)

router = DefaultRouter()

router.register(
    r"sales-returns",
    SalesReturnViewSet,
    basename="sales-returns",
)

router.register(
    r"sales-return-items",
    SalesReturnItemViewSet,
    basename="sales-return-items",
)

urlpatterns = router.urls