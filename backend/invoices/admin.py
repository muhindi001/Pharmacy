from django.contrib import admin

from .models import Invoice, Receipt


class ReceiptInline(admin.TabularInline):
    model = Receipt
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "customer",
        "total",
        "status",
        "invoice_date",
    )

    search_fields = (
        "invoice_number",
    )

    list_filter = (
        "status",
    )

    inlines = [
        ReceiptInline,
    ]