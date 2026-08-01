from django.contrib.auth import get_user_model
from rest_framework import serializers

from batches.models import Batch
from common.constants import PAYMENT_METHODS
from customers.models import Customer
from medicines.models import Medicine
from .models import Sale, SaleItem
from .services import process_sale

User = get_user_model()


class CustomerLookupField(serializers.PrimaryKeyRelatedField):
    queryset = Customer.objects.all()

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError:
            try:
                return Customer.objects.get(customer_code=data)
            except Customer.DoesNotExist:
                raise serializers.ValidationError("Customer not found.")


class CashierLookupField(serializers.PrimaryKeyRelatedField):
    queryset = User.objects.all()

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError:
            try:
                return User.objects.get(username=data)
            except User.DoesNotExist:
                try:
                    return User.objects.get(email=data)
                except User.DoesNotExist:
                    raise serializers.ValidationError("Cashier not found.")


class MedicineLookupField(serializers.PrimaryKeyRelatedField):
    queryset = Medicine.objects.all()

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError:
            try:
                return Medicine.objects.get(id=data)
            except Medicine.DoesNotExist:
                try:
                    return Medicine.objects.get(medicine_name=data)
                except Medicine.DoesNotExist:
                    raise serializers.ValidationError("Medicine not found.")


class BatchLookupField(serializers.PrimaryKeyRelatedField):
    queryset = Batch.objects.all()

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError:
            try:
                return Batch.objects.get(batch_number=data)
            except Batch.DoesNotExist:
                raise serializers.ValidationError("Batch not found.")


class SaleItemSerializer(serializers.ModelSerializer):

    medicine = MedicineLookupField(queryset=Medicine.objects.all())
    batch = BatchLookupField(queryset=Batch.objects.all())

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    payment_method = serializers.ChoiceField(
        choices=PAYMENT_METHODS,
        required=False,
        default="CASH",
    )

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "medicine",
            "medicine_name",
            "batch",
            "quantity",
            "payment_method",
            "unit_price",
            "cost_price",
            "discount",
            "tax",
            "profit",
            "expiry_date",
            "total",
        ]
        read_only_fields = [
            "id",
            "unit_price",
            "cost_price",
            "profit",
            "expiry_date",
            "total",
        ]


class SaleSerializer(serializers.ModelSerializer):

    customer = CustomerLookupField(queryset=Customer.objects.all())
    cashier = CashierLookupField(queryset=User.objects.all())

    items = SaleItemSerializer(
        many=True,
    )

    customer_name = serializers.SerializerMethodField()

    cashier_name = serializers.SerializerMethodField()

    class Meta:
        model = Sale

        fields = [
            "id",
            "sale_number",
            "invoice_number",
            "receipt_number",
            "reference_number",
            "customer",
            "customer_name",
            "prescription",
            "cashier",
            "cashier_name",
            "sale_type",
            "subtotal",
            "discount",
            "tax",
            "total",
            "notes",
            "status",
            "created_at",
            "updated_at",
            "items",
        ]

        read_only_fields = (
            "id",
            "sale_number",
            "invoice_number",
            "receipt_number",
            "subtotal",
            "discount",
            "tax",
            "total",
            "status",
            "created_at",
            "updated_at",
        )

    def get_customer_name(self, obj):

        if obj.customer:
            return f"{obj.customer.first_name} {obj.customer.last_name}"

        return None

    def get_cashier_name(self, obj):

        if obj.cashier:
            return obj.cashier.get_full_name() or obj.cashier.username

        return None

    def create(self, validated_data):

        items = validated_data.pop("items", [])
        request = self.context.get("request")

        if not items:
            raise serializers.ValidationError({"items": ["This field is required."]})

        return process_sale(
            validated_data,
            items,
            request=request,
        )

    def update(self, instance, validated_data):

        items_data = validated_data.pop("items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if items_data is not None:

            instance.items.all().delete()

            for item in items_data:

                SaleItem.objects.create(
                    sale=instance,
                    **item,
                )

        return instance