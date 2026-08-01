from django.test import TestCase

from customers.models import Customer


class CustomerCodeGenerationTests(TestCase):

    def test_customer_code_is_generated_when_missing(self):
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Doe",
            phone_number="+1234567890",
        )

        self.assertTrue(customer.customer_code)
        self.assertRegex(customer.customer_code, r"^CUST\d{6}$")
