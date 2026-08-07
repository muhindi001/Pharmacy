from audit.services import AuditService
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from .import_export import (
    export_csv,
    export_excel,
    export_pdf,
    import_medicines,
)
from .models import Medicine
from .serializers import MedicineSerializer


class MedicineViewSet(viewsets.ModelViewSet):

    serializer_class = MedicineSerializer
    parser_classes = [MultiPartParser, JSONParser]

    queryset = Medicine.objects.filter(
        is_deleted=False
    ).select_related("category")

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "medicine_name",
    ]

    filterset_fields = [
        "category",
        "unit",
        "is_active",
        "expiry_date",
    ]

    ordering_fields = [
        "medicine_name",
        "buying_price",
        "selling_price",
        "qty",
        "expiry_date",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "medicine_name",
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medicine = serializer.save()

        AuditService.log(
            action="CREATE",
            module="Medicine",
            description=f"Created medicine {medicine.medicine_name}",
            user=request.user,
            object_id=medicine.pk,
            request=request,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @action(detail=False, methods=["POST"])
    def import_file(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "No file provided."}, status=400)

        imported, updated = import_medicines(file)
        return Response({"imported": imported, "updated": updated})

    @action(detail=False, methods=["GET"])
    def export_csv(self, request):
        return export_csv()

    @action(detail=False, methods=["GET"])
    def export_excel(self, request):
        return export_excel()

    @action(detail=False, methods=["GET"])
    def export_pdf(self, request):
        return export_pdf()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        medicine = serializer.save()

        AuditService.log(
            action="UPDATE",
            module="Medicine",
            description=f"Updated medicine {medicine.medicine_name}",
            user=request.user,
            object_id=medicine.pk,
            request=request,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        medicine = self.get_object()
        name = medicine.medicine_name
        pk = medicine.pk

        medicine.is_deleted = True
        medicine.is_active = False
        medicine.save(update_fields=["is_deleted", "is_active", "updated_at"])

        AuditService.log(
            action="DELETE",
            module="Medicine",
            description=f"Deleted medicine {name}",
            user=request.user,
            object_id=pk,
            request=request,
        )

        return Response(status=204)