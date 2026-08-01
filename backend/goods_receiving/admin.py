from django.contrib import admin

from .models import GoodsReceipt
from .models import GoodsReceiptItem


class GoodsReceiptItemInline(admin.TabularInline):
    model = GoodsReceiptItem
    extra = 0


@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(admin.ModelAdmin):

    list_display = (
        "grn_number",
        "supplier",
        "warehouse",
        "received_date",
        "status",
        "received_by",
    )

    list_filter = (
        "status",
        "warehouse",
        "supplier",
        "received_date",
    )

    search_fields = (
        "grn_number",
        "invoice_number",
        "delivery_note",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        GoodsReceiptItemInline,
    ]


@admin.register(GoodsReceiptItem)
class GoodsReceiptItemAdmin(admin.ModelAdmin):

    list_display = (
        "receipt",
        "medicine",
        "batch_number",
        "accepted_quantity",
        "inventory_updated",
    )

    list_filter = (
        "inventory_updated",
    )

    search_fields = (
        "batch_number",
        "medicine__medicine_name",
    )