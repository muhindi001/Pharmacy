from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MedicineViewSet

router = DefaultRouter()

router.register(
    r"medicines",
    MedicineViewSet,
    basename="medicines",
)

urlpatterns = [
    path("medicines/import_file/", MedicineViewSet.as_view({"post": "import_file"}), name="medicines-import-file"),
    *router.urls,
]