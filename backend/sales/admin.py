from django.contrib import admin

from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = (
        "sale_number",
        "customer",
        "cashier",
        "sale_type",
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