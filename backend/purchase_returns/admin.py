from django.contrib import admin

from .models import PurchaseReturn, PurchaseReturnItem


class PurchaseReturnItemInline(admin.TabularInline):
    model = PurchaseReturnItem
    extra = 0


@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):

    list_display = (
        "return_number",
        "purchase",
        "supplier",
        "return_type",
        "status",
        "total_amount",
        "return_date",
    )

    list_filter = (
        "status",
        "return_type",
        "supplier",
    )

    search_fields = (
        "return_number",
        "purchase__purchase_number",
    )

    inlines = [
        PurchaseReturnItemInline,
    ]