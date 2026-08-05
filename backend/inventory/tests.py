from django.test import TestCase


class InventoryAPITests(TestCase):
    def test_inventory_list_endpoint_is_available(self):
        response = self.client.get("/api/inventory/")

        self.assertEqual(response.status_code, 200)
