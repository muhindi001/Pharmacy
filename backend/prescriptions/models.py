import uuid

from django.db import models


class Prescription(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Dispensed", "Dispensed"),
        ("Cancelled", "Cancelled"),
        ("Expired", "Expired"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    prescription_number = models.CharField(
        max_length=30,
        unique=True,
    )

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="prescriptions",
    )

    doctor_name = models.CharField(
        max_length=200,
    )

    doctor_license_number = models.CharField(
        max_length=100,
    )

    hospital_name = models.CharField(
        max_length=200,
    )

    diagnosis = models.TextField(
        blank=True,
        null=True,
    )

    date_issued = models.DateField()

    expiry_date = models.DateField()

    notes = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    verified_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_prescriptions",
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "prescriptions"
        ordering = ["-created_at"]

    def __str__(self):
        return self.prescription_number


class PrescriptionItem(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items",
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="prescription_items",
    )

    dosage = models.CharField(
        max_length=100,
    )

    frequency = models.CharField(
        max_length=100,
    )

    duration = models.CharField(
        max_length=100,
    )

    quantity = models.PositiveIntegerField()

    instructions = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "prescription_items"

    def __str__(self):
        return self.medicine.medicine_name