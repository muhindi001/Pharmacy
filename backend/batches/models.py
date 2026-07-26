import uuid

from django.db import models


class Batch(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Low Stock", "Low Stock"),
        ("Expired", "Expired"),
        ("Out of Stock", "Out of Stock"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="batches",
    )

    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.PROTECT,
        related_name="batches",
    )

    batch_number = models.CharField(
        max_length=100,
        unique=True,
    )

    purchase_date = models.DateField()

    expiry_date = models.DateField()

    quantity = models.PositiveIntegerField()

    remaining_quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available",
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "batches"
        ordering = ["-purchase_date"]

    def __str__(self):
        return f"{self.batch_number} - {self.medicine.medicine_name}"