from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, ReceiptViewSet

router = DefaultRouter()

router.register(
    r"invoices",
    InvoiceViewSet,
    basename="invoices",
)

router.register(
    r"receipts",
    ReceiptViewSet,
    basename="receipts",
)

urlpatterns = router.urls