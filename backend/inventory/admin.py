from django.contrib import admin
from .models import InventoryTransaction,Inventory


# @admin.register(InventoryTransaction)
# class InventoryTransactionAdmin(admin.ModelAdmin):

#     list_display = (
#         "transaction_type",
#         "medicine",
#         "batch",
#         "quantity",
#         "performed_by",
#         "transaction_date",
#     )

#     search_fields = (
#         "medicine__medicine_name",
#         "batch__batch_number",
#         "reference_number",
#     )

#     list_filter = (
#         "transaction_type",
#         "transaction_date",
#     )

#     ordering = (
#         "-transaction_date",
#     )
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):

    list_display = (
        "medicine",
        "batch",
        "quantity",
        "available_quantity",
        "reserved_quantity",
        "minimum_level",
        "maximum_level",
        "last_updated",
    )

    search_fields = (
        "medicine__medicine_name",
        "batch__batch_number",
    )

    list_filter = (
        "medicine__category",
    )