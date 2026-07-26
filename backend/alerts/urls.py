from rest_framework.routers import DefaultRouter
from .views import StockAlertViewSet

router = DefaultRouter()

router.register(
    r"stock-alerts",
    StockAlertViewSet,
    basename="stock-alerts",
)

urlpatterns = router.urls