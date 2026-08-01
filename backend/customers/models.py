import uuid

from django.db import models


def generate_customer_code():
    last_customer = Customer.objects.order_by("-created_at").first()

    if not last_customer or not last_customer.customer_code:
        return "CUST000001"

    number = int(last_customer.customer_code.replace("CUST", ""))
    return f"CUST{number + 1:06d}"


class Customer(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Blocked", "Blocked"),
    ]

    LOYALTY_TIERS = [
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    customer_code = models.CharField(
        max_length=30,
        unique=True,
        default=generate_customer_code,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    national_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    insurance_provider = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    insurance_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    emergency_contact_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    loyalty_card_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )

    loyalty_points = models.PositiveIntegerField(
        default=0,
    )

    loyalty_tier = models.CharField(
        max_length=20,
        choices=LOYALTY_TIERS,
        default="Bronze",
    )

    reward_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active",
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
        db_table = "customers"
        ordering = ["first_name", "last_name"]

    def save(self, *args, **kwargs):
        if not self.customer_code:
            self.customer_code = generate_customer_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"