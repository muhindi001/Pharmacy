from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import InventoryReportService
from .services import SalesReportService
from rest_framework.permissions import IsAuthenticated
from .services import PurchaseReportService
from .services import (
    CustomerReportService,
    SupplierReportService,
)
from .services import FinancialReportService
from django.http import HttpResponse
from .pdf import PDFReportGenerator
from .excel import ExcelReportGenerator
from .exports import ReportExportService
from .services import SalesReportService

class BaseReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_filters(self, request):

        return {
            "start_date": request.query_params.get("start_date"),
            "end_date": request.query_params.get("end_date"),
            "customer": request.query_params.get("customer"),
            "cashier": request.query_params.get("cashier"),
            "payment_method": request.query_params.get("payment_method"),
            "status": request.query_params.get("status"),
        }


class DailySalesReportView(BaseReportAPIView):

    def get(self, request):

        filters = self.get_filters(request)

        data = SalesReportService.daily_sales(**filters)

        return Response(data)


class MonthlySalesReportView(BaseReportAPIView):

    def get(self, request):

        filters = self.get_filters(request)

        data = SalesReportService.monthly_sales(**filters)

        return Response(data)


class YearlySalesReportView(BaseReportAPIView):

    def get(self, request):

        filters = self.get_filters(request)

        data = SalesReportService.yearly_sales(**filters)

        return Response(data)


class SalesSummaryReportView(BaseReportAPIView):

    def get(self, request):

        filters = self.get_filters(request)

        data = SalesReportService.sales_summary(**filters)

        return Response(data)


class SalesByProductReportView(BaseReportAPIView):

    def get(self, request):

        filters = self.get_filters(request)

        data = SalesReportService.sales_by_product(
            start_date=filters["start_date"],
            end_date=filters["end_date"],
        )

        return Response(data)


class SalesByCategoryReportView(BaseReportAPIView):

    def get(self, request):

        filters = self.get_filters(request)

        data = SalesReportService.sales_by_category(
            start_date=filters["start_date"],
            end_date=filters["end_date"],
        )

        return Response(data)


class TopSellingMedicinesReportView(BaseReportAPIView):

    def get(self, request):

        filters = self.get_filters(request)

        limit = request.query_params.get("limit", 10)

        data = SalesReportService.top_selling_medicines(
            limit=int(limit),
            start_date=filters["start_date"],
            end_date=filters["end_date"],
        )

        return Response(data)

# Inventory view
class CurrentStockReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        search = request.query_params.get("search")
        category = request.query_params.get("category")

        queryset = InventoryReportService.current_stock(
            search=search,
            category=category,
        )

        data = []

        for item in queryset:

            data.append({
                "id": str(item.id),
                "medicine": item.medicine.medicine_name,
                "generic_name": item.medicine.generic_name,
                "category": item.medicine.category.name,
                "batch": item.batch.batch_number if item.batch else None,
                "quantity": item.quantity,
                "buying_price": item.medicine.buying_price,
                "selling_price": item.medicine.selling_price,
                "expiry_date": item.batch.expiry_date if item.batch else None,
            })

        return Response(data)
class InventoryValuationReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = InventoryReportService.inventory_valuation()

        return Response(data)
class LowStockReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = InventoryReportService.low_stock()

        data = []

        for item in queryset:

            data.append({
                "medicine": item.medicine.medicine_name,
                "quantity": item.quantity,
                "minimum_level": item.minimum_level,
            })

        return Response(data)
class OutOfStockReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = InventoryReportService.out_of_stock()

        data = []

        for item in queryset:

            data.append({
                "medicine": item.medicine.medicine_name,
                "batch": item.batch.batch_number if item.batch else None,
            })

        return Response(data)
class ExpiringMedicinesReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        days = int(request.query_params.get("days", 30))

        queryset = InventoryReportService.expiring_medicines(days)

        data = []

        for item in queryset:

            data.append({
                "medicine": item.medicine.medicine_name,
                "batch": item.batch.batch_number,
                "expiry_date": item.batch.expiry_date,
                "quantity": item.quantity,
            })

        return Response(data)
class ExpiredMedicinesReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = InventoryReportService.expired_medicines()

        data = []

        for item in queryset:

            data.append({
                "medicine": item.medicine.medicine_name,
                "batch": item.batch.batch_number,
                "expiry_date": item.batch.expiry_date,
                "quantity": item.quantity,
            })

        return Response(data)
class StockMovementReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        data = InventoryReportService.stock_movement(
            start_date=start_date,
            end_date=end_date,
        )

        return Response(data)
class InventorySummaryReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = InventoryReportService.inventory_summary()

        return Response(data)
    
# Purchase Report Views
class PurchaseSummaryReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = PurchaseReportService.purchase_summary(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
            supplier=request.query_params.get("supplier"),
            status=request.query_params.get("status"),
            payment_status=request.query_params.get("payment_status"),
        )

        return Response(data)
class DailyPurchaseReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = PurchaseReportService.daily_purchases(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )

        return Response(data)
class MonthlyPurchaseReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = PurchaseReportService.monthly_purchases(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )

        return Response(data)
class YearlyPurchaseReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = PurchaseReportService.yearly_purchases(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )

        return Response(data)
class PurchasesBySupplierReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = PurchaseReportService.purchases_by_supplier(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )

        return Response(data)
class PurchaseCostAnalysisReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = PurchaseReportService.purchase_cost_analysis(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )

        return Response(data)
class TopPurchasedMedicinesReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        limit = int(request.query_params.get("limit", 10))

        data = PurchaseReportService.top_purchased_medicines(
            limit=limit,
        )

        return Response(data)
class OutstandingPurchasesReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = PurchaseReportService.outstanding_purchases()

        data = []

        for purchase in queryset:

            data.append({
                "purchase_number": purchase.purchase_number,
                "supplier": purchase.supplier.supplier_name,
                "total": purchase.total,
                "paid_amount": purchase.paid_amount,
                "balance": purchase.balance,
                "status": purchase.status,
            })

        return Response(data)
class SearchPurchaseReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        query = request.query_params.get("search", "")

        queryset = PurchaseReportService.search(query)

        data = []

        for purchase in queryset:

            data.append({
                "purchase_number": purchase.purchase_number,
                "invoice_number": purchase.invoice_number,
                "supplier": purchase.supplier.supplier_name,
                "purchase_date": purchase.purchase_date,
                "total": purchase.total,
                "status": purchase.status,
            })

        return Response(data)

class CustomerSummaryReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = CustomerReportService.customer_summary()

        return Response(data)


class CustomerPurchaseHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = CustomerReportService.purchase_history(

            customer=request.query_params.get("customer"),

            start_date=request.query_params.get("start_date"),

            end_date=request.query_params.get("end_date"),

        )

        return Response(data)


class TopCustomersReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        limit = int(request.query_params.get("limit", 10))

        data = CustomerReportService.top_customers(limit)

        return Response(data)


class OutstandingCustomerCreditView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = CustomerReportService.outstanding_credit()

        return Response(data)


class SearchCustomerReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = CustomerReportService.search(

            request.query_params.get("search", "")

        )

        return Response(data)

class SupplierSummaryReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            SupplierReportService.supplier_summary()

        )


class SupplierPurchaseHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            SupplierReportService.supplier_purchase_history(

                supplier=request.query_params.get("supplier"),

                start_date=request.query_params.get("start_date"),

                end_date=request.query_params.get("end_date"),

            )

        )


class TopSuppliersReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        limit = int(request.query_params.get("limit", 10))

        return Response(

            SupplierReportService.top_suppliers(limit)

        )


class OutstandingSuppliersReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            SupplierReportService.outstanding_suppliers()

        )


class SearchSupplierReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            SupplierReportService.search(

                request.query_params.get("search", "")

            )

        )

class RevenueReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.revenue(

                request.query_params.get("start_date"),

                request.query_params.get("end_date"),

            )

        )


class ProfitLossReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.profit_loss(

                request.query_params.get("start_date"),

                request.query_params.get("end_date"),

            )

        )


class CashFlowReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.cash_flow(

                request.query_params.get("start_date"),

                request.query_params.get("end_date"),

            )

        )


class PaymentMethodReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.payment_methods(

                request.query_params.get("start_date"),

                request.query_params.get("end_date"),

            )

        )


class TaxSummaryReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.tax_summary(

                request.query_params.get("start_date"),

                request.query_params.get("end_date"),

            )

        )


class ReceivablesReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.receivables()

        )


class PayablesReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.payables()

        )


class FinancialDashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            FinancialReportService.dashboard()

        )

class SalesPDFView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        report = SalesReportService.top_selling_medicines()

        headers = [

            "Medicine",

            "Quantity",

            "Revenue",

            "Profit",

        ]

        rows = []

        for item in report:

            rows.append([

                item["medicine__medicine_name"],

                item["quantity"],

                item["revenue"],

                item["profit"],

            ])

        pdf = PDFReportGenerator.generate(

            "Top Selling Medicines",

            headers,

            rows,

        )

        response = HttpResponse(

            pdf,

            content_type="application/pdf",

        )

        response["Content-Disposition"] = (

            'attachment; filename="sales_report.pdf"'

        )

        return response
class SalesExcelView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        report = SalesReportService.top_selling_medicines()

        headers = [

            "Medicine",

            "Generic Name",

            "Quantity",

            "Revenue",

            "Profit",

        ]

        rows = []

        for item in report:

            rows.append([

                item["medicine__medicine_name"],

                item["medicine__generic_name"],

                item["quantity"],

                item["revenue"],

                item["profit"],

            ])

        excel = ExcelReportGenerator.generate(

            "Top Selling Medicines",

            headers,

            rows,

        )

        response = HttpResponse(

            excel,

            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        )

        response[
            "Content-Disposition"
        ] = 'attachment; filename="sales_report.xlsx"'

        return response

class SalesPDFExportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        report = SalesReportService.top_selling_medicines()

        headers = [
            "Medicine",
            "Generic Name",
            "Quantity",
            "Revenue",
            "Profit",
        ]

        rows = []

        for item in report:

            rows.append([
                item["medicine__medicine_name"],
                item["medicine__generic_name"],
                item["quantity"],
                item["revenue"],
                item["profit"],
            ])

        return ReportExportService.export_pdf(
            title="Top Selling Medicines",
            headers=headers,
            rows=rows,
            filename="top_selling_medicines",
        )
class SalesExcelExportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        report = SalesReportService.top_selling_medicines()

        headers = [
            "Medicine",
            "Generic Name",
            "Quantity",
            "Revenue",
            "Profit",
        ]

        rows = []

        for item in report:

            rows.append([
                item["medicine__medicine_name"],
                item["medicine__generic_name"],
                item["quantity"],
                item["revenue"],
                item["profit"],
            ])

        return ReportExportService.export_excel(
            title="Top Selling Medicines",
            headers=headers,
            rows=rows,
            filename="top_selling_medicines",
        )
class SalesCSVExportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        report = SalesReportService.top_selling_medicines()

        headers = [
            "Medicine",
            "Generic Name",
            "Quantity",
            "Revenue",
            "Profit",
        ]

        rows = []

        for item in report:

            rows.append([
                item["medicine__medicine_name"],
                item["medicine__generic_name"],
                item["quantity"],
                item["revenue"],
                item["profit"],
            ])

        return ReportExportService.export_csv(
            headers=headers,
            rows=rows,
            filename="top_selling_medicines",
        )
