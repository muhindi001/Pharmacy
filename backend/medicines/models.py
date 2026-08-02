import re

from django.db import models


def generate_medicine_sku():
    prefix = "SKU"
    max_number = 0

    for medicine_id in Medicine.objects.filter(id__startswith=prefix).values_list("id", flat=True):
        match = re.search(r"(\d+)$", str(medicine_id))
        if match:
            try:
                max_number = max(max_number, int(match.group(1)))
            except ValueError:
                continue

    next_number = max_number + 1
    width = max(2, len(str(next_number)))
    return f"{prefix}{next_number:0{width}d}"


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
    manufacturer = models.ForeignKey(
        "manufacturers.Manufacturer",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="medicines",
    )

    has_rfid = models.BooleanField(
        default=False
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
    
manufacturer = models.ForeignKey(
    "manufacturers.Manufacturer",
    on_delete=models.PROTECT,
    related_name="medicines",
    null=True,
    blank=True,
)