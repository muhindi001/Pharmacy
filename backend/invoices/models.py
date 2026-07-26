import uuid

from django.db import models


class Invoice(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Unpaid", "Unpaid"),
        ("Partially Paid", "Partially Paid"),
        ("Paid", "Paid"),
        ("Cancelled", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
    )

    sale = models.OneToOneField(
        "sales.Sale",
        on_delete=models.CASCADE,
        related_name="invoice",
    )

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
    )

    payment = models.ForeignKey(
        "payments.Payment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
    )

    invoice_date = models.DateTimeField(
        auto_now_add=True,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft",
    )

    qr_code = models.ImageField(
        upload_to="invoice_qr/",
        null=True,
        blank=True,
    )

    pdf = models.FileField(
        upload_to="invoice_pdf/",
        null=True,
        blank=True,
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
        db_table = "invoices"
        ordering = ["-created_at"]

    def __str__(self):
        return self.invoice_number


class Receipt(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    receipt_number = models.CharField(
        max_length=30,
        unique=True,
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="receipts",
    )

    payment = models.ForeignKey(
        "payments.Payment",
        on_delete=models.CASCADE,
        related_name="receipts",
    )

    cashier = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="receipts",
    )

    payment_method = models.CharField(
        max_length=50,
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    receipt_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "receipts"
        ordering = ["-receipt_date"]

    def __str__(self):
        return self.receipt_number