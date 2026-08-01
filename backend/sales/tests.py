from django.test import TestCase

from accounts.models import User
from batches.models import Batch
from categories.models import Category
from customers.models import Customer
from medicines.models import Medicine
from sales.models import Sale
from sales.serializers import SaleSerializer
from suppliers.models import Supplier


class SalesPayloadTests(TestCase):

    def test_sale_create_accepts_minimal_payload(self):
        user = User.objects.create_user(
            username="cashier1",
            email="cashier@example.com",
            password="TestPass123!",
            first_name="Cash",
            last_name="ier",
        )

        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+12345678901",
        )

        category = Category.objects.create(
            category_name="Pain Relief",
        )

        medicine = Medicine.objects.create(
            medicine_name="Paracetamol",
            generic_name="Acetaminophen",
            buying_price=20,
            selling_price=30,
            category=category,
            unit="Tablet",
            expiry_date="2027-12-31",
        )

        supplier = Supplier.objects.create(
            supplier_name="Alpha Pharma",
            company_name="Alpha Pharma Ltd",
            contact_person="Jane Smith",
            phone_number="+12345678902",
            email="supplier@example.com",
            address="Main Road",
        )

        batch = Batch.objects.create(
            medicine=medicine,
            supplier=supplier,
            batch_number="BATCH-001",
            purchase_date="2026-01-01",
            expiry_date="2027-12-31",
            quantity=10,
            remaining_quantity=10,
            purchase_price=20,
            selling_price=30,
            status="Available",
        )

        payload = {
            "customer": str(customer.id),
            "cashier": str(user.id),
            "sale_type": "Cash",
            "items": [
                {
                    "medicine": str(medicine.id),
                    "batch": str(batch.id),
                    "quantity": 2,
                    "payment_method": "CASH",
                }
            ],
        }

        serializer = SaleSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        sale = serializer.save()
        self.assertEqual(sale.items.count(), 1)
