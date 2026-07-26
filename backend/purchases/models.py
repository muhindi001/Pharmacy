import uuid
from django.db import models


class Purchase(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Ordered", "Ordered"),
        ("Partially Received", "Partially Received"),
        ("Received", "Received"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Partial", "Partial"),
        ("Paid", "Paid"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    purchase_number = models.CharField(
        max_length=30,
        unique=True,
    )

    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.PROTECT,
        related_name="purchases",
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    purchase_date = models.DateField()

    expected_delivery = models.DateField(
        null=True,
        blank=True,
    )

    received_date = models.DateField(
        null=True,
        blank=True,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Draft",
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

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="created_purchases",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-purchase_date"]
        db_table = "purchases"

    def __str__(self):
        return self.purchase_number

class PurchaseItem(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items",
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
    )

    batch_number = models.CharField(
        max_length=100,
    )

    manufacturing_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField()

    quantity = models.PositiveIntegerField()

    free_quantity = models.PositiveIntegerField(
        default=0,
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "purchase_items"

    def __str__(self):
        return self.batch_number