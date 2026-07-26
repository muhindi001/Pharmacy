from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
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
    parser_classes = [MultiPartParser]

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
        "generic_name_sku",
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

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()