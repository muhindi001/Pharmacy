import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from categories.models import Category

from .import_export import import_medicines
from .models import Medicine


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


class MedicineImportTests(TestCase):
    def test_import_medicines_accepts_stock_in_excel_columns(self):
        category = Category.objects.create(category_name="Pain Relief")
        csv_data = (
            "medicine_name,generic_name,category,unit,qty,buying_price,selling_price,expiry_date\n"
            "Paracetamol,Acetaminophen,Pain Relief,Tablet,100,10.00,15.00,2035-01-01\n"
        ).encode("utf-8")
        uploaded_file = SimpleUploadedFile("medicines.csv", csv_data, content_type="text/csv")

        imported, updated = import_medicines(uploaded_file)

        self.assertEqual(imported, 1)
        self.assertEqual(updated, 0)
        self.assertTrue(Medicine.objects.filter(medicine_name="Paracetamol").exists())
        medicine = Medicine.objects.get(medicine_name="Paracetamol")
        self.assertEqual(medicine.category, category)
        self.assertEqual(medicine.qty, 100)
        self.assertEqual(float(medicine.buying_price), 10.00)


class MedicineSerializerPayloadTests(TestCase):
    def test_serializer_handles_missing_required_fields_and_missing_category(self):
        payload = {
            "medicine_name": "Amoxicillin 500mg",
            "category": 1,
            "unit": "Capsule",
            "purchase_price": 500,
            "selling_price": 800,
            "status": "ACTIVE",
        }

        serializer = MedicineSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        medicine = serializer.save()

        self.assertEqual(medicine.generic_name, "Amoxicillin 500mg")
        self.assertEqual(float(medicine.buying_price), 500.00)
        self.assertIsNotNone(medicine.category)
        self.assertTrue(medicine.is_active)
        self.assertIsNotNone(medicine.expiry_date)
