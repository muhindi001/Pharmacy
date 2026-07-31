from datetime import date

from rest_framework import serializers

from batches.models import Batch
from categories.models import Category
from medicines.models import Medicine
from suppliers.models import Supplier

from .models import Inventory, InventoryTransaction


class InventoryTransactionSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    batch_number = serializers.CharField(
        source="batch.batch_number",
        read_only=True,
    )

    class Meta:
        model = InventoryTransaction
        fields = "__all__"

        read_only_fields = (
            "id",
            "transaction_date",
            "created_at",
            "updated_at",
        )


class InventorySerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    batch_number = serializers.CharField(
        source="batch.batch_number",
        read_only=True,
    )

    @staticmethod
    def resolve_medicine(value):
        if value in (None, "", "null", "None"):
            return None

        if isinstance(value, int):
            value = str(value)

        if isinstance(value, str):
            medicine = Medicine.objects.filter(id=value).first()
            if medicine is None:
                medicine = Medicine.objects.filter(
                    medicine_name__iexact=value
                ).first()
            if medicine is None and value.isdigit():
                medicine = Medicine.objects.filter(id__icontains=value).order_by("id").first()
            return medicine

        return None

    @staticmethod
    def resolve_batch(value, medicine=None):
        if value in (None, "", "null", "None"):
            if medicine is not None:
                batch = Batch.objects.filter(medicine=medicine).order_by("-purchase_date", "-created_at").first()
                if batch is not None:
                    return batch
            return None

        try:
            return Batch.objects.get(pk=value)
        except (Batch.DoesNotExist, TypeError, ValueError):
            if isinstance(value, str):
                batch = Batch.objects.filter(batch_number__iexact=value).first()
                if batch is not None:
                    return batch
            if medicine is not None:
                batch = Batch.objects.filter(medicine=medicine).order_by("-purchase_date", "-created_at").first()
                if batch is not None:
                    return batch
            return None

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.copy()

            medicine_value = data.get("medicine")
            medicine = self.resolve_medicine(medicine_value)
            if medicine is not None:
                data["medicine"] = medicine.pk
            elif medicine_value is not None:
                default_category = Category.objects.order_by("id").first() or Category.objects.create(
                    category_name="General",
                    description="Auto-created default category",
                )
                default_supplier = Supplier.objects.order_by("id").first() or Supplier.objects.create(
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
                medicine = Medicine.objects.create(
                    medicine_name=str(medicine_value),
                    generic_name=str(medicine_value),
                    buying_price=0,
                    selling_price=0,
                    category=default_category,
                    unit="Capsule",
                    qty=0,
                    expiry_date=date.today(),
                )
                data["medicine"] = medicine.pk

            batch_value = data.get("batch")
            batch = self.resolve_batch(batch_value, medicine)
            if batch is not None:
                data["batch"] = str(batch.pk)
            elif medicine is not None:
                supplier = Supplier.objects.order_by("id").first() or Supplier.objects.create(
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
                batch = Batch.objects.create(
                    medicine=medicine,
                    supplier=supplier,
                    batch_number=f"AUTO-{date.today().strftime('%Y%m%d')}-{medicine.pk}",
                    purchase_date=date.today(),
                    expiry_date=date.today(),
                    quantity=0,
                    remaining_quantity=0,
                    purchase_price=0,
                    selling_price=0,
                    status="Available",
                )
                data["batch"] = str(batch.pk)

        return super().to_internal_value(data)

    class Meta:
        model = Inventory
        fields = "__all__"