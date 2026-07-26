from django.urls import path

from .views import (
    DailySalesReportView,
    MonthlySalesReportView,
    YearlySalesReportView,
    SalesSummaryReportView,
    SalesByProductReportView,
    SalesByCategoryReportView,
    TopSellingMedicinesReportView,
)
from .views import (
    CurrentStockReportView,
    InventoryValuationReportView,
    LowStockReportView,
    OutOfStockReportView,
    ExpiringMedicinesReportView,
    ExpiredMedicinesReportView,
    StockMovementReportView,
    InventorySummaryReportView,
)
from .views import (
    PurchaseSummaryReportView,
    DailyPurchaseReportView,
    MonthlyPurchaseReportView,
    YearlyPurchaseReportView,
    PurchasesBySupplierReportView,
    PurchaseCostAnalysisReportView,
    TopPurchasedMedicinesReportView,
    OutstandingPurchasesReportView,
    SearchPurchaseReportView,
)

urlpatterns = [

    # ==========================
    # Sales Reports
    # ==========================

    path("sales/daily/",DailySalesReportView.as_view(),name="daily-sales-report",),
    path("sales/monthly/",MonthlySalesReportView.as_view(),name="monthly-sales-report",),
    path("sales/yearly/",YearlySalesReportView.as_view(),name="yearly-sales-report",),
    path("sales/summary/",SalesSummaryReportView.as_view(),name="sales-summary-report",),
    path("sales/products/",SalesByProductReportView.as_view(),name="sales-by-product-report",),
    path("sales/categories/",SalesByCategoryReportView.as_view(),name="sales-by-category-report",),
    path("sales/top-medicines/",TopSellingMedicinesReportView.as_view(),name="top-selling-medicines-report",),
    
    # ==========================
# Inventory Reports
# ==========================

path(
    "inventory/current-stock/",
    CurrentStockReportView.as_view(),
    name="inventory-current-stock",
),

path(
    "inventory/valuation/",
    InventoryValuationReportView.as_view(),
    name="inventory-valuation",
),

path(
    "inventory/low-stock/",
    LowStockReportView.as_view(),
    name="inventory-low-stock",
),

path(
    "inventory/out-of-stock/",
    OutOfStockReportView.as_view(),
    name="inventory-out-of-stock",
),

path(
    "inventory/expiring/",
    ExpiringMedicinesReportView.as_view(),
    name="inventory-expiring",
),

path(
    "inventory/expired/",
    ExpiredMedicinesReportView.as_view(),
    name="inventory-expired",
),

path(
    "inventory/movement/",
    StockMovementReportView.as_view(),
    name="inventory-movement",
),

path(
    "inventory/summary/",
    InventorySummaryReportView.as_view(),
    name="inventory-summary",
),

# ==========================
# Purchase Reports
# ==========================

path(
    "purchases/summary/",
    PurchaseSummaryReportView.as_view(),
    name="purchase-summary-report",
),

path(
    "purchases/daily/",
    DailyPurchaseReportView.as_view(),
    name="daily-purchase-report",
),

path(
    "purchases/monthly/",
    MonthlyPurchaseReportView.as_view(),
    name="monthly-purchase-report",
),

path(
    "purchases/yearly/",
    YearlyPurchaseReportView.as_view(),
    name="yearly-purchase-report",
),

path(
    "purchases/suppliers/",
    PurchasesBySupplierReportView.as_view(),
    name="purchases-by-supplier-report",
),

path(
    "purchases/cost-analysis/",
    PurchaseCostAnalysisReportView.as_view(),
    name="purchase-cost-analysis-report",
),

path(
    "purchases/top-medicines/",
    TopPurchasedMedicinesReportView.as_view(),
    name="top-purchased-medicines-report",
),

path(
    "purchases/outstanding/",
    OutstandingPurchasesReportView.as_view(),
    name="outstanding-purchases-report",
),

path(
    "purchases/search/",
    SearchPurchaseReportView.as_view(),
    name="search-purchase-report",
),
]