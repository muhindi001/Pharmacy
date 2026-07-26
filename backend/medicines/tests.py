import io

from django.test import TestCase

from categories.models import Category

from .models import Medicine
from .views import FlexibleJSONParser


class MedicineModelTests(TestCase):
    def test_medicine_ids_follow_sku_format(self):
        category = Category.objects.create(category_name="Pain Relief")

        medicine = Medicine.objects.create(
            medicine_name="Paracetamol",
            generic_name="Acetaminophen",
            buying_price=10.00,
            selling_price=15.00,
            category=category,
            unit="Tablet",
            qty=100,
            expiry_date="2030-01-01",
        )

        self.assertRegex(medicine.id, r"^SKU\d{2}$")
        self.assertEqual(medicine.medicine_uuid, medicine.id)


class FlexibleJSONParserTests(TestCase):
    def test_parser_accepts_single_quoted_python_dict(self):
        parser = FlexibleJSONParser()
        stream = io.BytesIO(
            b"{'medicine_name': 'Paracetamol', 'generic_name': 'Acetaminophen', 'buying_price': 10.0, 'selling_price': 15.0, 'category': 'SKU01', 'unit': 'Tablet', 'qty': 100, 'expiry_date': '2030-01-01', 'is_active': True}"
        )

        data = parser.parse(stream, media_type="application/json", parser_context={})

        self.assertEqual(data["medicine_name"], "Paracetamol")
        self.assertEqual(data["unit"], "Tablet")
        self.assertTrue(data["is_active"])
