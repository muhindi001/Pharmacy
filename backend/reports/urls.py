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
from .views import (
    CustomerSummaryReportView,
    CustomerPurchaseHistoryView,
    TopCustomersReportView,
    OutstandingCustomerCreditView,
    SearchCustomerReportView,
    SupplierSummaryReportView,
    SupplierPurchaseHistoryView,
    TopSuppliersReportView,
    OutstandingSuppliersReportView,
    SearchSupplierReportView,
)
from .views import (
    RevenueReportView,
    ProfitLossReportView,
    CashFlowReportView,
    PaymentMethodReportView,
    TaxSummaryReportView,
    ReceivablesReportView,
    PayablesReportView,
    FinancialDashboardView,
)
from .views import SalesExcelView
from .views import (
    SalesPDFExportView,
    SalesExcelExportView,
    SalesCSVExportView,
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
# ==========================
# Customer Reports
# ==========================

path("customers/summary/", CustomerSummaryReportView.as_view()),
path("customers/history/", CustomerPurchaseHistoryView.as_view()),
path("customers/top/", TopCustomersReportView.as_view()),
path("customers/credit/", OutstandingCustomerCreditView.as_view()),
path("customers/search/", SearchCustomerReportView.as_view()),

# ==========================
# Supplier Reports
# ==========================

path("suppliers/summary/", SupplierSummaryReportView.as_view()),
path("suppliers/history/", SupplierPurchaseHistoryView.as_view()),
path("suppliers/top/", TopSuppliersReportView.as_view()),
path("suppliers/outstanding/", OutstandingSuppliersReportView.as_view()),
path("suppliers/search/", SearchSupplierReportView.as_view()),

# ==========================
# Financial Reports
# ==========================

path("financial/revenue/", RevenueReportView.as_view()),
path("financial/profit-loss/", ProfitLossReportView.as_view()),
path("financial/cash-flow/", CashFlowReportView.as_view()),
path("financial/payment-methods/", PaymentMethodReportView.as_view()),
path("financial/tax-summary/", TaxSummaryReportView.as_view()),
path("financial/receivables/", ReceivablesReportView.as_view()),
path("financial/payables/", PayablesReportView.as_view()),
path("financial/dashboard/", FinancialDashboardView.as_view()),

path(
    "exports/sales/excel/",
    SalesExcelView.as_view(),
    name="sales-excel",
),
# ==========================
# Export Reports
# ==========================

path(
    "exports/sales/pdf/",
    SalesPDFExportView.as_view(),
    name="sales-export-pdf",
),

path(
    "exports/sales/excel/",
    SalesExcelExportView.as_view(),
    name="sales-export-excel",
),

path(
    "exports/sales/csv/",
    SalesCSVExportView.as_view(),
    name="sales-export-csv",
),
]