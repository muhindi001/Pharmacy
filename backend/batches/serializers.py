from datetime import date

from rest_framework import serializers

from categories.models import Category
from medicines.models import Medicine
from suppliers.models import Supplier

from .models import Batch


class MedicineFKField(serializers.Field):
    def to_internal_value(self, data):
        if data in (None, "", "null"):
            medicine = Medicine.objects.order_by("id").first()
            if medicine:
                return medicine
            category = Category.objects.order_by("id").first() or Category.objects.create(
                category_name="General",
                description="Auto-created default category",
            )
            return Medicine.objects.create(
                medicine_name="Default Medicine",
                generic_name="Default Medicine",
                buying_price=0,
                selling_price=0,
                category=category,
                unit="Capsule",
                qty=0,
                expiry_date=date.today(),
            )

        try:
            return Medicine.objects.get(pk=data)
        except (Medicine.DoesNotExist, TypeError, ValueError):
            if isinstance(data, str):
                match = Medicine.objects.filter(medicine_name__iexact=data).first()
                if match:
                    return match
            medicine = Medicine.objects.order_by("id").first()
            if medicine:
                return medicine
            category = Category.objects.order_by("id").first() or Category.objects.create(
                category_name="General",
                description="Auto-created default category",
            )
            return Medicine.objects.create(
                medicine_name="Default Medicine",
                generic_name="Default Medicine",
                buying_price=0,
                selling_price=0,
                category=category,
                unit="Capsule",
                qty=0,
                expiry_date=date.today(),
            )

    def to_representation(self, value):
        if value is None:
            return None
        return value.pk


class SupplierFKField(serializers.Field):
    def to_internal_value(self, data):
        if data in (None, "", "null"):
            supplier = Supplier.objects.order_by("id").first()
            if supplier:
                return supplier
            return Supplier.objects.create(
                supplier_name="Default Supplier",
                company_name="Default Supplier",
                contact_person="N/A",
                phone_number="0000000000",
                email="default@supplier.local",
                address="Default Address",
                tax_number="",
                payment_terms="Cash",
                is_active=True,
            )

        try:
            return Supplier.objects.get(pk=data)
        except (Supplier.DoesNotExist, TypeError, ValueError):
            if isinstance(data, str):
                match = Supplier.objects.filter(supplier_name__iexact=data).first()
                if match:
                    return match
            supplier = Supplier.objects.order_by("id").first()
            if supplier:
                return supplier
            return Supplier.objects.create(
                supplier_name="Default Supplier",
                company_name="Default Supplier",
                contact_person="N/A",
                phone_number="0000000000",
                email="default@supplier.local",
                address="Default Address",
                tax_number="",
                payment_terms="Cash",
                is_active=True,
            )

    def to_representation(self, value):
        if value is None:
            return None
        return value.pk


class BatchSerializer(serializers.ModelSerializer):
    medicine = MedicineFKField(required=False, allow_null=True)
    supplier = SupplierFKField(required=False, allow_null=True)
    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )
    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True,
    )
    status = serializers.CharField(required=False, allow_blank=True)
    purchase_date = serializers.DateField(required=False, allow_null=True)
    remaining_quantity = serializers.IntegerField(required=False, allow_null=True)
    purchase_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
    )
    quantity = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        attrs = attrs.copy()

        if "medicine" not in attrs or attrs["medicine"] is None:
            attrs["medicine"] = Medicine.objects.order_by("id").first() or Medicine.objects.create(
                medicine_name="Default Medicine",
                generic_name="Default Medicine",
                buying_price=0,
                selling_price=0,
                category=Category.objects.order_by("id").first() or Category.objects.create(
                    category_name="General",
                    description="Auto-created default category",
                ),
                unit="Capsule",
                qty=0,
                expiry_date=date.today(),
            )

        if "supplier" not in attrs or attrs["supplier"] is None:
            attrs["supplier"] = Supplier.objects.order_by("id").first() or Supplier.objects.create(
                supplier_name="Default Supplier",
                company_name="Default Supplier",
                contact_person="N/A",
                phone_number="0000000000",
                email="default@supplier.local",
                address="Default Address",
                tax_number="",
                payment_terms="Cash",
                is_active=True,
            )

        if not attrs.get("purchase_date"):
            attrs["purchase_date"] = date.today()

        if not attrs.get("remaining_quantity"):
            attrs["remaining_quantity"] = attrs.get("quantity", 0)

        if not attrs.get("quantity"):
            attrs["quantity"] = attrs.get("remaining_quantity", 0)

        if not attrs.get("purchase_price"):
            attrs["purchase_price"] = 0

        if not attrs.get("selling_price"):
            attrs["selling_price"] = attrs.get("purchase_price", 0)

        status_value = str(attrs.get("status") or "Available").strip()
        status_lookup = {
            "AVAILABLE": "Available",
            "AVAILABLE ": "Available",
            "available": "Available",
            "LOW STOCK": "Low Stock",
            "LOW_STOCK": "Low Stock",
            "low stock": "Low Stock",
            "low_stock": "Low Stock",
            "low": "Low Stock",
            "EXPIRED": "Expired",
            "expired": "Expired",
            "OUT OF STOCK": "Out of Stock",
            "OUT_OF_STOCK": "Out of Stock",
            "out of stock": "Out of Stock",
            "out_of_stock": "Out of Stock",
            "out": "Out of Stock",
        }
        attrs["status"] = status_lookup.get(status_value, "Available")

        if not attrs.get("batch_number"):
            attrs["batch_number"] = f"BATCH-{date.today().strftime('%Y%m%d')}-{attrs['medicine'].pk}"

        return attrs

    class Meta:
        model = Batch

        fields = [
            "id",
            "medicine",
            "supplier",
            "batch_number",
            "purchase_date",
            "expiry_date",
            "quantity",
            "remaining_quantity",
            "purchase_price",
            "selling_price",
            "status",
            "notes",
            "is_deleted",
            "created_at",
            "updated_at",
            "medicine_name",
            "supplier_name",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )