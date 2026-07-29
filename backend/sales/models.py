import uuid
from common.constants import PAYMENT_METHODS
from django.db import models


class Sale(models.Model):

    SALE_TYPES = [
        ("Cash", "Cash"),
        ("Credit", "Credit"),
        ("Insurance", "Insurance"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    sale_number = models.CharField(
        max_length=30,
        unique=True,
    )

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales",
    )

    prescription = models.ForeignKey(
        "prescriptions.Prescription",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales",
    )

    cashier = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="sales",
    )

    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.PROTECT,
        related_name="sales",
        null=True,
        blank=True,
    )

    # warehouse = models.ForeignKey(
    #     "warehouses.Warehouse",
    #     on_delete=models.PROTECT,
    #     related_name="sales",
    #     null=True,
    #     blank=True,
    # )
    sale_type = models.CharField(
    max_length=20,
    choices=SALE_TYPES,
    default="Cash",
    )

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )

    receipt_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "sales"
        ordering = ["-created_at"]

    def __str__(self):
        return self.sale_number

class SaleItem(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
    )
    rfid_tag = models.ForeignKey(
        "rfid.RFIDTag",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="sale_items",
    )
    payment_method = models.CharField(
    max_length=20,
    choices=PAYMENT_METHODS,
)

    batch = models.ForeignKey(
        "batches.Batch",
        on_delete=models.PROTECT,
        related_name="sale_items",
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    cost_price = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    )
    expiry_date = models.DateField()

    profit = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default=0,
    )
    discount = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default=0,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "sale_items"

    def __str__(self):
        return self.medicine.medicine_name