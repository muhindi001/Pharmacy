import re

from django.db import models


def generate_category_sku():
    prefix = "SKU"
    last_category = Category.objects.filter(id__startswith=prefix).order_by("id").last()
    if last_category and last_category.id:
        match = re.search(r"(\d+)$", last_category.id)
        if match:
            return f"{prefix}{int(match.group(1)) + 1:02d}"
    return f"{prefix}01"


class Category(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_category_sku,
        editable=False
    )

    category_name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "categories"
        ordering = ["category_name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_category_sku()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name