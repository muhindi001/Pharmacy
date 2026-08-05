from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from batches.models import Batch
from categories.models import Category
from medicines.models import Medicine
from suppliers.models import Supplier

from .models import StockAlert


class StockAlertAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="stockadmin",
            email="stockadmin@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(category_name="Pain Relief")
        supplier = Supplier.objects.create(
            supplier_name="Pharma Supply",
            company_name="Pharma Supply Co.",
            contact_person="Jane Doe",
            phone_number="1234567890",
            email="supplier@example.com",
            address="123 Main St",
            payment_terms="Cash",
        )
        medicine = Medicine.objects.create(
            medicine_name="Panadol",
            generic_name="Paracetamol",
            buying_price=10.00,
            selling_price=15.00,
            category=category,
            unit="Tablet",
            qty=100,
            expiry_date="2030-01-01",
        )
        batch = Batch.objects.create(
            medicine=medicine,
            supplier=supplier,
            batch_number="B-1001",
            purchase_date="2025-01-01",
            expiry_date="2030-01-01",
            quantity=100,
            remaining_quantity=12,
            purchase_price=8.00,
            selling_price=15.00,
        )
        StockAlert.objects.create(
            medicine=medicine,
            batch=batch,
            alert_type="Low Stock",
            message="Only 12 units remaining.",
            status="New",
        )

    def test_stock_alert_list_returns_json_payload(self):
        url = reverse("stock-alerts-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["alert_type"], "Low Stock")
        self.assertEqual(data["results"][0]["message"], "Only 12 units remaining.")
        self.assertEqual(data["results"][0]["medicine_name"], "Panadol")
        self.assertEqual(data["results"][0]["batch_number"], "B-1001")

    def test_inventory_alert_list_alias_returns_json_payload(self):
        url = reverse("inventory-alerts-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["alert_type"], "Low Stock")

    def test_batch_below_five_units_creates_low_stock_alert(self):
        category = Category.objects.create(category_name="Antibiotics")
        supplier = Supplier.objects.create(
            supplier_name="Second Supplier",
            company_name="Second Supplier Co.",
            contact_person="John Smith",
            phone_number="2345678901",
            email="second@example.com",
            address="456 Side St",
            payment_terms="Cash",
        )
        medicine = Medicine.objects.create(
            medicine_name="Amoxicillin",
            generic_name="Amoxycillin",
            buying_price=12.00,
            selling_price=20.00,
            category=category,
            unit="Capsule",
            qty=50,
            expiry_date="2031-01-01",
        )

        batch = Batch.objects.create(
            medicine=medicine,
            supplier=supplier,
            batch_number="B-2002",
            purchase_date="2025-02-01",
            expiry_date="2031-02-01",
            quantity=50,
            remaining_quantity=4,
            purchase_price=9.00,
            selling_price=19.00,
        )

        alert = StockAlert.objects.filter(
            medicine=medicine,
            batch=batch,
            alert_type="Low Stock",
        ).first()

        self.assertIsNotNone(alert)
        self.assertIn("below 5 units", alert.message)
        self.assertEqual(alert.status, "New")
