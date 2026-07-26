from django.contrib import admin

from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):

    list_display = (
        "medicine_name",
        "generic_name",
        "buying_price",
        "selling_price",
        "category",
        "unit",
        "qty",
        "expiry_date",
        "is_active",
    )

    list_filter = (
        "category",
        "unit",
        "is_active",
    )

    search_fields = (
        "medicine_name",
        "generic_name",
    )

    ordering = (
        "medicine_name",
    )