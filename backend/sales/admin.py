from django.contrib import admin

from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = (
        "medicine",
        "batch",
        "quantity",
        "payment_method",
        "unit_price",
        "discount",
        "tax",
        "total",
    )
    readonly_fields = ("total",)
    autocomplete_fields = ("medicine", "batch")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = "Items"

    list_display = (
        "sale_number",
        "customer",
        "cashier",
        "sale_type",
        "item_count",
        "total",
        "status",
        "created_at",
    )

    list_filter = (
        "sale_type",
        "status",
    )

    search_fields = (
        "sale_number",
    )

    inlines = [
        SaleItemInline,
    ]