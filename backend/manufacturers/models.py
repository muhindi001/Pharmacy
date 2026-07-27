from django.db import models


class Manufacturer(models.Model):

    manufacturer_name = models.CharField(
        max_length=255,
        unique=True
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    license_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["manufacturer_name"]

    def __str__(self):
        return self.manufacturer_name