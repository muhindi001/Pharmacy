from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RFIDReaderViewSet,
    RFIDTagViewSet,
    RFIDScanViewSet,
    RFIDMovementViewSet,
)

app_name = "rfid"

router = DefaultRouter()

router.register(
    r"readers",
    RFIDReaderViewSet,
    basename="rfid-reader"
)

router.register(
    r"tags",
    RFIDTagViewSet,
    basename="rfid-tag"
)

router.register(
    r"scans",
    RFIDScanViewSet,
    basename="rfid-scan"
)

router.register(
    r"movements",
    RFIDMovementViewSet,
    basename="rfid-movement"
)

urlpatterns = [
    path("", include(router.urls)),
]