from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    RFIDReader,
    RFIDTag,
    RFIDScan,
    RFIDMovement,
)

from .serializers import (
    RFIDReaderSerializer,
    RFIDTagSerializer,
    RFIDScanSerializer,
    RFIDMovementSerializer,
)

from .services import (
    RFIDTagService,
    RFIDScanService,
    RFIDReceivingService,
    RFIDSaleService,
    RFIDReturnService,
    RFIDTransferService,
    RFIDBulkScanService,
    RFIDAuditService,
)


class RFIDReaderViewSet(viewsets.ModelViewSet):
    queryset = RFIDReader.objects.all()
    serializer_class = RFIDReaderSerializer
    permission_classes = [IsAuthenticated]


class RFIDTagViewSet(viewsets.ModelViewSet):
    queryset = RFIDTag.objects.select_related(
        "medicine",
        "inventory",
    )

    serializer_class = RFIDTagSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def register(self, request):

        tag = RFIDTagService.register_tag(
            medicine=request.data["medicine"],
            inventory=request.data["inventory"],
            uid=request.data["uid"],
            batch=request.data.get("batch"),
            quantity=request.data.get("quantity", 1),
        )

        serializer = self.get_serializer(tag)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RFIDScanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RFIDScan.objects.select_related(
        "tag",
        "reader",
    )

    serializer_class = RFIDScanSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def scan(self, request):

        scan = RFIDScanService.scan_tag(
            uid=request.data["uid"],
            reader_id=request.data["reader"],
            scan_type=request.data["scan_type"],
            user=request.user,
        )

        serializer = self.get_serializer(scan)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def bulk_scan(self, request):

        scans = RFIDBulkScanService.bulk_scan(
            uids=request.data["uids"],
            reader_id=request.data["reader"],
            scan_type=request.data["scan_type"],
            user=request.user,
        )

        serializer = self.get_serializer(
            scans,
            many=True,
        )

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def receive(self, request):

        inventory = RFIDReceivingService.receive(
            uid=request.data["uid"],
            qty=request.data.get("quantity", 1),
        )

        return Response({
            "message": "Inventory updated successfully.",
            "inventory": inventory.id,
        })

    @action(detail=False, methods=["post"])
    def sale(self, request):

        tag = RFIDSaleService.sell(
            uid=request.data["uid"],
        )

        return Response({
            "message": "Sale completed.",
            "tag": tag.uid,
        })

    @action(detail=False, methods=["post"])
    def return_item(self, request):

        tag = RFIDReturnService.return_item(
            uid=request.data["uid"],
        )

        return Response({
            "message": "Return processed.",
            "tag": tag.uid,
        })

    @action(detail=False, methods=["post"])
    def transfer(self, request):

        RFIDTransferService.transfer(
            uid=request.data["uid"],
            from_location=request.data["from_location"],
            to_location=request.data["to_location"],
        )

        return Response({
            "message": "Transfer completed."
        })

    @action(detail=False, methods=["post"])
    def audit(self, request):

        result = RFIDAuditService.audit(
            scanned_uids=request.data["uids"]
        )

        return Response(result)


class RFIDMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RFIDMovement.objects.select_related(
        "tag"
    )

    serializer_class = RFIDMovementSerializer
    permission_classes = [IsAuthenticated]