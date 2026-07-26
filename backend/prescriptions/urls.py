from rest_framework.routers import DefaultRouter

from .views import (
    PrescriptionViewSet,
    PrescriptionItemViewSet,
)

router = DefaultRouter()

router.register(
    "prescriptions",
    PrescriptionViewSet,
    basename="prescriptions",
)

router.register(
    "prescription-items",
    PrescriptionItemViewSet,
    basename="prescription-items",
)

urlpatterns = router.urls