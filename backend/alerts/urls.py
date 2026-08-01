from rest_framework.routers import DefaultRouter
from .views import StockAlertViewSet

router = DefaultRouter()

router.register(
    r"stock-alerts",
    StockAlertViewSet,
    basename="stock-alerts",
)

router.register(
    r"inventory-alerts",
    StockAlertViewSet,
    basename="inventory-alerts",
)

urlpatterns = router.urls