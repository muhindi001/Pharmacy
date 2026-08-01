import uuid

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView

from customers.models import Customer
from reports.exports import ReportExportService

from .serializers import CustomerSaleHistorySerializer
from .services import CustomerHistoryService
from .filters import CustomerSaleHistoryFilter


def get_customer_for_lookup(customer_id):
    raw_value = str(customer_id)

    try:
        uuid.UUID(raw_value)
        customer = Customer.objects.filter(pk=raw_value).first()
        if customer:
            return customer
    except (ValueError, AttributeError, TypeError, ValidationError):
        customer = None

    if raw_value.isdigit():
        numeric_id = int(raw_value)
        code_match = f"CUST{numeric_id:06d}"
        customer = Customer.objects.filter(customer_code=code_match).first()
        if customer:
            return customer

    customer = Customer.objects.filter(customer_code=raw_value).first()
    if customer:
        return customer

    raise Http404("Customer not found")


class CustomerSaleHistoryView(ListAPIView):

    serializer_class = CustomerSaleHistorySerializer

    permission_classes = [
        IsAuthenticated
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = CustomerSaleHistoryFilter

    search_fields = [
        "invoice_number",
    ]

    ordering_fields = [
        "created_at",
        "total",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):

        customer = get_customer_for_lookup(
            self.kwargs["customer_id"]
        )

        return CustomerHistoryService.sales(customer)


class CustomerStatisticsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, customer_id):

        customer = get_customer_for_lookup(customer_id)

        data = CustomerHistoryService.statistics(
            customer
        )

        return Response(data)


class CustomerMedicineHistoryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, customer_id):

        customer = get_customer_for_lookup(customer_id)

        queryset = CustomerHistoryService.sales(
            customer
        )

        serializer = CustomerSaleHistorySerializer(
            queryset,
            many=True
        )

        return Response(serializer.data)


class CustomerHistoryExportPDFView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, customer_id):
        customer = get_customer_for_lookup(customer_id)
        queryset = CustomerHistoryService.sales(customer)

        headers = ["Invoice", "Date", "Total", "Status"]
        rows = [
            [
                sale.invoice_number,
                sale.created_at.date().isoformat(),
                str(sale.total),
                sale.status,
            ]
            for sale in queryset
        ]

        title = f"Customer History - {customer.first_name} {customer.last_name}".strip()
        filename = f"customer-history-{customer.customer_code or customer.id}"

        return ReportExportService.export_pdf(
            title=title,
            headers=headers,
            rows=rows,
            filename=filename,
        )


class CustomerHistoryExportExcelView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, customer_id):
        customer = get_customer_for_lookup(customer_id)
        queryset = CustomerHistoryService.sales(customer)

        headers = ["Invoice", "Date", "Total", "Status"]
        rows = [
            [
                sale.invoice_number,
                sale.created_at.date().isoformat(),
                str(sale.total),
                sale.status,
            ]
            for sale in queryset
        ]

        filename = f"customer-history-{customer.customer_code or customer.id}"
        title = f"Customer History - {customer.first_name} {customer.last_name}".strip()

        return ReportExportService.export_excel(
            title=title,
            headers=headers,
            rows=rows,
            filename=filename,
        )


class CustomerStatementView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, customer_id):

        customer = get_customer_for_lookup(customer_id)

        sales = CustomerHistoryService.sales(
            customer
        )

        statistics = CustomerHistoryService.statistics(
            customer
        )

        serializer = CustomerSaleHistorySerializer(
            sales,
            many=True
        )

        return Response({

            "customer": f"{customer.first_name} {customer.last_name}".strip(),

            "statistics": statistics,

            "sales": serializer.data,

        })