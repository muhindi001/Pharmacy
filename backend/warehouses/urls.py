from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    WarehouseViewSet,
    WarehouseTransferViewSet,
    WarehouseInventoryViewSet,
)

app_name = "warehouses"

router = DefaultRouter()

router.register(
    r"",
    WarehouseViewSet,
    basename="warehouse",
)

router.register(
    r"transfers",
    WarehouseTransferViewSet,
    basename="warehouse-transfer",
)

urlpatterns = [

    path("", include(router.urls)),

    path(
        "inventory/receive/",
        WarehouseInventoryViewSet.as_view(
            {
                "post": "receive",
            }
        ),
        name="warehouse-receive",
    ),

    path(
        "inventory/issue/",
        WarehouseInventoryViewSet.as_view(
            {
                "post": "issue",
            }
        ),
        name="warehouse-issue",
    ),

    path(
        "inventory/adjust/",
        WarehouseInventoryViewSet.as_view(
            {
                "post": "adjust",
            }
        ),
        name="warehouse-adjust",
    ),
]