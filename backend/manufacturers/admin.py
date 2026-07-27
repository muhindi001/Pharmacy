from django.contrib import admin
from .models import Manufacturer


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):

    list_display = (
        "manufacturer_name",
        "country",
        "phone_number",
        "status",
    )

    search_fields = (
        "manufacturer_name",
        "code",
        "phone_number",
        "email",
    )

    list_filter = (
        "country",
        "status",
    )