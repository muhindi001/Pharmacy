import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        PHARMACIST = "PHARMACIST", "Pharmacist"
        CASHIER = "CASHIER", "Cashier"
        INVENTORY = "INVENTORY", "Inventory Officer"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        SUSPENDED = "SUSPENDED", "Suspended"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
    )

    phone_number = PhoneNumberField(
        blank=True,
        null=True,
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    role = models.ForeignKey(
        "roles.Role",
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    two_factor_enabled = models.BooleanField(
        default=False,
    )

    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    @classmethod
    def get_user(cls, user_id):
        if not user_id:
            return None

        if isinstance(user_id, uuid.UUID):
            return cls.objects.filter(pk=user_id).first()

        try:
            return cls.objects.filter(pk=uuid.UUID(str(user_id))).first()
        except (ValueError, ValidationError, TypeError):
            return None
        
