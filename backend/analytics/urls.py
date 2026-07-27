from django.urls import path

from .views import (
    DashboardAnalyticsView,
    DailySalesAnalyticsView,
    TopSellingMedicinesView,
    AverageSaleView,
    InventorySummaryView,
    InventoryValueView,
    FinancialOverviewView,
    CustomerOverviewView,
    SupplierOverviewView,
    FastMovingMedicinesView,
    SlowMovingMedicinesView,
    DeadStockView,
    SalesForecastView,
)

app_name = "analytics"

urlpatterns = [

    # Dashboard
    path(
        "dashboard/",
        DashboardAnalyticsView.as_view(),
        name="dashboard",
    ),

    # Sales Analytics
    path(
        "sales/daily/",
        DailySalesAnalyticsView.as_view(),
        name="daily-sales",
    ),

    path(
        "sales/top-selling/",
        TopSellingMedicinesView.as_view(),
        name="top-selling",
    ),

    path(
        "sales/average/",
        AverageSaleView.as_view(),
        name="average-sale",
    ),

    # Inventory Analytics
    path(
        "inventory/summary/",
        InventorySummaryView.as_view(),
        name="inventory-summary",
    ),

    path(
        "inventory/value/",
        InventoryValueView.as_view(),
        name="inventory-value",
    ),

    # Financial Analytics
    path(
        "financial/",
        FinancialOverviewView.as_view(),
        name="financial-overview",
    ),

    # Customer Analytics
    path(
        "customers/",
        CustomerOverviewView.as_view(),
        name="customer-overview",
    ),

    # Supplier Analytics
    path(
        "suppliers/",
        SupplierOverviewView.as_view(),
        name="supplier-overview",
    ),

    # Business Intelligence
    path(
        "business/fast-moving/",
        FastMovingMedicinesView.as_view(),
        name="fast-moving",
    ),

    path(
        "business/slow-moving/",
        SlowMovingMedicinesView.as_view(),
        name="slow-moving",
    ),

    path(
        "business/dead-stock/",
        DeadStockView.as_view(),
        name="dead-stock",
    ),

    # Forecast
    path(
        "forecast/",
        SalesForecastView.as_view(),
        name="forecast",
    ),
]