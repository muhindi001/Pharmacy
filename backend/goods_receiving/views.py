from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .filters import GoodsReceiptFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import GoodsReceipt
from .serializers import GoodsReceiptSerializer
from .services import GoodsReceivingService


class GoodsReceiptViewSet(viewsets.ModelViewSet):

    queryset = GoodsReceipt.objects.prefetch_related(
        "items",
        "items__medicine"
    ).select_related(
        "supplier",
        "warehouse",
        "purchase",
        "received_by"
    )

    serializer_class = GoodsReceiptSerializer

    permission_classes = [IsAuthenticated]

    filterset_class = GoodsReceiptFilter

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "supplier",
        "warehouse",
    ]
    
    filterset_fields = [
    "status",
    "supplier",
    "warehouse",
]

    search_fields = [
        "grn_number",
        "invoice_number",
        "delivery_note",
    ]

    ordering_fields = [
        "received_date",
        "created_at",
    ]

    ordering = [
        "-received_date",
    ]

    @action(
        detail=True,
        methods=["post"],
        url_path="receive"
    )
    def receive_stock(self, request, pk=None):

        receipt = self.get_object()

        try:

            GoodsReceivingService.receive(
                receipt=receipt,
                user=request.user,
                request=request
            )

            serializer = self.get_serializer(receipt)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "detail": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=["post"]
    )
    def cancel(self, request, pk=None):

        receipt = self.get_object()

        if receipt.status == "RECEIVED":
            return Response(
                {
                    "detail": "Received GRN cannot be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        receipt.status = "CANCELLED"
        receipt.save()

        return Response(
            {
                "detail": "Goods receipt cancelled."
            }
        )

    @action(
        detail=True,
        methods=["post"]
    )
    def reopen(self, request, pk=None):

        receipt = self.get_object()

        if receipt.status != "CANCELLED":
            return Response(
                {
                    "detail": "Only cancelled receipts can be reopened."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        receipt.status = "PENDING"
        receipt.save()

        return Response(
            {
                "detail": "Goods receipt reopened."
            }
        )