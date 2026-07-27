from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import (
    DashboardAnalyticsService,
    SalesAnalyticsService,
    InventoryAnalyticsService,
    FinancialAnalyticsService,
    CustomerAnalyticsService,
    SupplierAnalyticsService,
    BusinessIntelligenceService,
    ForecastService,
)

from .serializers import (
    DashboardAnalyticsSerializer,
    DailySalesSerializer,
    TopSellingSerializer,
    AverageSaleSerializer,
    InventorySummarySerializer,
    InventoryValueSerializer,
    FinancialOverviewSerializer,
    CustomerOverviewSerializer,
    SupplierOverviewSerializer,
    FastMovingSerializer,
    SlowMovingSerializer,
    DeadStockSerializer,
    ForecastSerializer,
)


class DashboardAnalyticsView(APIView):

    def get(self, request):
        data = DashboardAnalyticsService.dashboard()
        serializer = DashboardAnalyticsSerializer(data)
        return Response(serializer.data)


class DailySalesAnalyticsView(APIView):

    def get(self, request):
        data = SalesAnalyticsService.daily_sales()
        serializer = DailySalesSerializer(data, many=True)
        return Response(serializer.data)


class TopSellingMedicinesView(APIView):

    def get(self, request):
        data = SalesAnalyticsService.top_selling()
        serializer = TopSellingSerializer(data, many=True)
        return Response(serializer.data)


class AverageSaleView(APIView):

    def get(self, request):
        data = SalesAnalyticsService.average_sale()
        serializer = AverageSaleSerializer(data)
        return Response(serializer.data)


class InventorySummaryView(APIView):

    def get(self, request):
        data = InventoryAnalyticsService.stock_summary()
        serializer = InventorySummarySerializer(data)
        return Response(serializer.data)


class InventoryValueView(APIView):

    def get(self, request):
        data = InventoryAnalyticsService.inventory_value()
        serializer = InventoryValueSerializer(data)
        return Response(serializer.data)


class FinancialOverviewView(APIView):

    def get(self, request):
        data = FinancialAnalyticsService.overview()
        serializer = FinancialOverviewSerializer(data)
        return Response(serializer.data)


class CustomerOverviewView(APIView):

    def get(self, request):
        data = CustomerAnalyticsService.overview()
        serializer = CustomerOverviewSerializer(data)
        return Response(serializer.data)


class SupplierOverviewView(APIView):

    def get(self, request):
        data = SupplierAnalyticsService.overview()
        serializer = SupplierOverviewSerializer(data)
        return Response(serializer.data)


class FastMovingMedicinesView(APIView):

    def get(self, request):
        data = BusinessIntelligenceService.fast_moving()
        serializer = FastMovingSerializer(data, many=True)
        return Response(serializer.data)


class SlowMovingMedicinesView(APIView):

    def get(self, request):
        data = BusinessIntelligenceService.slow_moving()
        serializer = SlowMovingSerializer(data, many=True)
        return Response(serializer.data)


class DeadStockView(APIView):

    def get(self, request):
        data = BusinessIntelligenceService.dead_stock()
        serializer = DeadStockSerializer(data, many=True)
        return Response(serializer.data)


class SalesForecastView(APIView):

    def get(self, request):
        days = request.query_params.get("days", 30)

        try:
            days = int(days)
        except ValueError:
            return Response(
                {"detail": "days must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = ForecastService.sales_forecast(days)
        serializer = ForecastSerializer(data)
        return Response(serializer.data)