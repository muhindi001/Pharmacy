from django.urls import path

from .views import (
    CustomerHistoryExportExcelView,
    CustomerHistoryExportPDFView,
    CustomerSaleHistoryView,
    CustomerStatisticsView,
    CustomerMedicineHistoryView,
    CustomerStatementView,
)

urlpatterns = [

    path(
        "<str:customer_id>/history/",
        CustomerSaleHistoryView.as_view(),
        name="customer-history",
    ),
    path(
        "<str:customer_id>/history/export/pdf/",
        CustomerHistoryExportPDFView.as_view(),
        name="customer-history-export-pdf",
    ),
    path(
        "<str:customer_id>/history/export/excel/",
        CustomerHistoryExportExcelView.as_view(),
        name="customer-history-export-excel",
    ),
    path(
        "<str:customer_id>/history/statistics/",
        CustomerStatisticsView.as_view(),
        name="customer-history-statistics",
    ),
    path(
        "<str:customer_id>/history/medicines/",
        CustomerMedicineHistoryView.as_view(),
        name="customer-history-medicines",
    ),
    path(
        "<str:customer_id>/history/statement/",
        CustomerStatementView.as_view(),
        name="customer-history-statement",
    ),

    path(
        "<str:customer_id>/statistics/",
        CustomerStatisticsView.as_view(),
        name="customer-statistics",
    ),

    path(
        "<str:customer_id>/medicines/",
        CustomerMedicineHistoryView.as_view(),
        name="customer-medicines",
    ),

    path(
        "<str:customer_id>/statement/",
        CustomerStatementView.as_view(),
        name="customer-statement",
    ),
]