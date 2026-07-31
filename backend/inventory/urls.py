from rest_framework.routers import DefaultRouter

from .views import InventoryTransactionViewSet,InventoryViewSet

router = DefaultRouter()

router.register(
    r"inventory-transactions",
    InventoryTransactionViewSet,
    basename="inventory-transactions",
)

router.register(
    r"",
    InventoryViewSet,
    basename="inventory",
)
urlpatterns = router.urls