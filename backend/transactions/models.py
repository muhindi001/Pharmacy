import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from customers.models import Customer
from payments.models import Payment
from sales.models import Sale


class Transaction(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    )

    TRANSACTION_TYPES = (
        ("SALE", "Sale"),
        ("PURCHASE", "Purchase"),
        ("REFUND", "Refund"),
        ("EXPENSE", "Expense"),
        ("INCOME", "Income"),
        ("TRANSFER", "Transfer"),
        ("ADJUSTMENT", "Adjustment"),
    )

    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("BANK", "Bank Transfer"),
        ("MPESA", "M-Pesa"),
        ("AIRTEL", "Airtel Money"),
        ("TIGO", "Tigo Pesa"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    transaction_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )

    sale = models.ForeignKey(
        Sale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SUCCESS",
    )

    transaction_date = models.DateTimeField(
        default=timezone.now,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-transaction_date"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def save(self, *args, **kwargs):

        if not self.transaction_number:

            today = timezone.now().strftime("%Y%m%d")

            count = (
                Transaction.objects.filter(
                    transaction_number__startswith=f"TRX-{today}"
                ).count()
                + 1
            )

            self.transaction_number = (
                f"TRX-{today}-{count:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_number