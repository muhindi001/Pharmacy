from django.contrib import admin

from .models import Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):

    list_display = (
        "batch_number",
        "medicine",
        "supplier",
        "purchase_date",
        "expiry_date",
        "quantity",
        "remaining_quantity",
        "status",
    )

    search_fields = (
        "batch_number",
        "medicine__medicine_name",
        "supplier__supplier_name",
    )

    list_filter = (
        "status",
        "purchase_date",
        "expiry_date",
    )

    ordering = (
        "-purchase_date",
    )