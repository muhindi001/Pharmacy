from django.test import TestCase

from .models import Category


class CategoryModelTests(TestCase):
    def test_category_ids_follow_sku_format(self):
        category = Category.objects.create(category_name="Pain Relief")

        self.assertRegex(category.id, r"^SKU\d{2}$")
