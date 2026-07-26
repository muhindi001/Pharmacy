from django.contrib import admin

from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):

    list_display = (
        "purchase_number",
        "supplier",
        "invoice_number",
        "purchase_date",
        "received_date",
        "payment_status",
        "status",
        "subtotal",
        "discount",
        "tax",
        "total",
        "created_by",
    )

    list_filter = (
        "status",
        "payment_status",
        "purchase_date",
        "supplier",
    )

    search_fields = (
        "purchase_number",
        "invoice_number",
        "supplier__supplier_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        PurchaseItemInline,
    ]


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):

    list_display = (
        "purchase",
        "medicine",
        "batch_number",
        "quantity",
        "free_quantity",
        "unit_cost",
        "selling_price",
        "tax",
        "discount",
        "total",
        "expiry_date",
    )

    list_filter = (
        "expiry_date",
        "medicine",
    )

    search_fields = (
        "batch_number",
        "medicine__medicine_name",
        "purchase__purchase_number",
    )