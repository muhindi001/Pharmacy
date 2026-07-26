from django.contrib import admin

from .models import SalesReturn, SalesReturnItem


class SalesReturnItemInline(admin.TabularInline):
    model = SalesReturnItem
    extra = 0


@admin.register(SalesReturn)
class SalesReturnAdmin(admin.ModelAdmin):

    list_display = (
        "return_number",
        "sale",
        "customer",
        "return_type",
        "total_amount",
        "status",
        "return_date",
    )

    search_fields = (
        "return_number",
        "sale__sale_number",
    )

    list_filter = (
        "status",
        "return_type",
    )

    inlines = [
        SalesReturnItemInline,
    ]