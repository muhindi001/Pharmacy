from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Warehouse,
    WarehouseTransfer,
)

from .serializers import (
    WarehouseSerializer,
    WarehouseTransferSerializer,
)

from .services import (
    WarehouseService,
    WarehouseTransferService,
    WarehouseInventoryService,
    WarehouseReportService,
)
from django_filters.rest_framework import DjangoFilterBackend

from .filters import (
    WarehouseFilter,
    WarehouseTransferFilter,
)


class WarehouseViewSet(viewsets.ModelViewSet):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseFilter

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):

        warehouse = self.get_object()

        return Response(
            WarehouseService.warehouse_summary(warehouse)
        )

    @action(detail=True, methods=["get"])
    def stock(self, request, pk=None):

        warehouse = self.get_object()

        inventory = WarehouseReportService.stock_by_warehouse(
            warehouse
        )

        data = [
            {
                "medicine": item.medicine.medicine_name,
                "quantity": item.quantity,
            }
            for item in inventory
        ]

        return Response(data)

    @action(detail=True, methods=["get"])
    def low_stock(self, request, pk=None):

        warehouse = self.get_object()

        inventory = WarehouseReportService.low_stock(
            warehouse
        )

        data = [
            {
                "medicine": item.medicine.medicine_name,
                "quantity": item.quantity,
            }
            for item in inventory
        ]

        return Response(data)

    @action(detail=True, methods=["get"])
    def valuation(self, request, pk=None):

        warehouse = self.get_object()

        value = WarehouseReportService.total_stock_value(
            warehouse
        )

        return Response({
            "warehouse": warehouse.warehouse_name,
            "stock_value": value,
        })


class WarehouseTransferViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseTransferFilter

    queryset = (
        WarehouseTransfer.objects
        .select_related(
            "from_warehouse",
            "to_warehouse",
        )
        .prefetch_related("items")
    )

    serializer_class = WarehouseTransferSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):

        transfer = self.get_object()

        WarehouseTransferService.approve_transfer(
            transfer
        )

        return Response({
            "message": "Transfer approved."
        })

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):

        transfer = self.get_object()

        WarehouseTransferService.complete_transfer(
            transfer,
            request=request,
        )

        return Response({
            "message": "Transfer completed."
        })

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):

        transfer = self.get_object()

        WarehouseTransferService.cancel_transfer(
            transfer
        )

        return Response({
            "message": "Transfer cancelled."
        })


class WarehouseInventoryViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def receive(self, request):

        inventory = WarehouseInventoryService.receive_stock(
            warehouse_id=request.data["warehouse"],
            medicine_id=request.data["medicine"],
            quantity=request.data["quantity"],
        )

        return Response(
            {
                "message": "Stock received successfully.",
                "inventory_id": inventory.id,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def issue(self, request):

        inventory = WarehouseInventoryService.remove_stock(
            warehouse_id=request.data["warehouse"],
            medicine_id=request.data["medicine"],
            quantity=request.data["quantity"],
        )

        return Response(
            {
                "message": "Stock issued successfully.",
                "inventory_id": inventory.id,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def adjust(self, request):

        inventory = WarehouseInventoryService.adjust_stock(
            warehouse_id=request.data["warehouse"],
            medicine_id=request.data["medicine"],
            quantity=request.data["quantity"],
            reason=request.data.get("reason", ""),
            request=request,
        )

        return Response(
            {
                "message": "Stock adjusted successfully.",
                "inventory_id": inventory.id,
            },
            status=status.HTTP_200_OK,
        )
