from django.contrib import admin

from .models import (
    Warehouse,
    WarehouseTransfer,
    WarehouseTransferItem,
)


class WarehouseTransferItemInline(admin.TabularInline):
    model = WarehouseTransferItem
    extra = 0
    autocomplete_fields = ["medicine"]


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):

    list_display = (
        "warehouse_name",
        "code",
        "warehouse_type",
        "manager",
        "phone",
        "status",
        "created_at",
    )

    list_filter = (
        "warehouse_type",
        "status",
    )

    search_fields = (
        "warehouse_name",
        "code",
        "manager",
        "phone",
        "email",
    )

    ordering = (
        "warehouse_name",
    )


@admin.register(WarehouseTransfer)
class WarehouseTransferAdmin(admin.ModelAdmin):

    list_display = (
        "transfer_number",
        "from_warehouse",
        "to_warehouse",
        "transfer_date",
        "status",
    )

    list_filter = (
        "status",
        "transfer_date",
    )

    search_fields = (
        "transfer_number",
    )

    autocomplete_fields = (
        "from_warehouse",
        "to_warehouse",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = [
        WarehouseTransferItemInline,
    ]


@admin.register(WarehouseTransferItem)
class WarehouseTransferItemAdmin(admin.ModelAdmin):

    list_display = (
        "transfer",
        "medicine",
        "quantity",
    )

    search_fields = (
        "transfer__transfer_number",
        "medicine__medicine_name",
    )

    autocomplete_fields = (
        "transfer",
        "medicine",
    )
