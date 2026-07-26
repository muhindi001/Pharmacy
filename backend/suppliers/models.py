import uuid

from django.db import models


class Supplier(models.Model):

    PAYMENT_TERMS = [
        ("Cash", "Cash"),
        ("7 Days", "7 Days"),
        ("15 Days", "15 Days"),
        ("30 Days", "30 Days"),
        ("60 Days", "60 Days"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    supplier_name = models.CharField(
        max_length=150,
    )

    company_name = models.CharField(
        max_length=200,
    )

    contact_person = models.CharField(
        max_length=150,
    )

    phone_number = models.CharField(
        max_length=20,
    )

    email = models.EmailField(
        unique=True,
    )

    address = models.TextField()

    tax_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    payment_terms = models.CharField(
        max_length=20,
        choices=PAYMENT_TERMS,
        default="Cash",
    )

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
        db_table = "suppliers"
        ordering = ["supplier_name"]

    def __str__(self):
        return self.supplier_name