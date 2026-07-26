import re

from django.db import models


def generate_medicine_sku():
    prefix = "SKU"
    last_medicine = Medicine.objects.filter(id__startswith=prefix).order_by("id").last()
    if last_medicine and last_medicine.id:
        match = re.search(r"(\d+)$", last_medicine.id)
        if match:
            return f"{prefix}{int(match.group(1)) + 1:02d}"
    return f"{prefix}01"


class Medicine(models.Model):

    UNIT_CHOICES = [
        ("Tablet", "Tablet"),
        ("Capsule", "Capsule"),
        ("Bottle", "Bottle"),
        ("Box", "Box"),
        ("Tube", "Tube"),
        ("Injection", "Injection"),
        ("Syrup", "Syrup"),
        ("Sachet", "Sachet"),
        ("Piece", "Piece"),
    ]

    id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_medicine_sku,
        editable=False,
    )

    medicine_uuid = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
        null=True,
    )

    medicine_name = models.CharField(
        max_length=255,
    )

    generic_name = models.CharField(
        max_length=255,
    )

    buying_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="medicines",
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
    )

    qty = models.PositiveIntegerField(
        default=0,
    )

    expiry_date = models.DateField()

    is_active = models.BooleanField(
        default=True,
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
        db_table = "medicines"
        ordering = ["medicine_name"]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_medicine_sku()
        if not self.medicine_uuid:
            self.medicine_uuid = self.id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.medicine_name