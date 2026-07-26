import uuid

from django.db import models


class Payment(models.Model):

    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("Card", "Card"),
        ("Mobile Money", "Mobile Money"),
        ("Bank Transfer", "Bank Transfer"),
        ("Insurance", "Insurance"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Partial", "Partial"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
        ("Cancelled", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    payment_number = models.CharField(
        max_length=30,
        unique=True,
    )

    sale = models.ForeignKey(
        "sales.Sale",
        on_delete=models.CASCADE,
        related_name="payments",
    )

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )

    cashier = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="payments",
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        default="TZS",
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    provider = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending",
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "payments"
        ordering = ["-payment_date"]

    def __str__(self):
        return self.payment_number