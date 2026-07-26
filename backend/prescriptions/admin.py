from django.contrib import admin

from .models import Prescription, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 0


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    list_display = (
        "prescription_number",
        "customer",
        "doctor_name",
        "status",
        "expiry_date",
    )

    search_fields = (
        "prescription_number",
        "doctor_name",
    )

    list_filter = (
        "status",
    )

    inlines = [
        PrescriptionItemInline,
    ]