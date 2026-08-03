from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .serializers import PaymentSerializer


class PaymentSerializerTests(TestCase):
    def test_serializer_initializes_with_declared_fields(self):
        serializer = PaymentSerializer()

        self.assertIn("payment_method", serializer.fields)
        self.assertIn("sale_number", serializer.fields)
        self.assertIn("customer_name", serializer.fields)

    def test_status_success_is_normalized_to_paid(self):
        serializer = PaymentSerializer()

        self.assertEqual(serializer.validate_status("SUCCESS"), "Paid")

    def test_create_sets_cashier_from_request_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username="cashier",
            email="cashier@example.com",
            password="secret123",
        )
        request = APIRequestFactory().get("/")
        request.user = user
        serializer = PaymentSerializer(context={"request": request})

        with patch.object(PaymentSerializer, "_generate_payment_number", return_value="PAY-TEST"):
            with patch("rest_framework.serializers.ModelSerializer.create", return_value=object()) as mock_create:
                serializer.create({"payment_method": "CASH", "amount": 100, "status": "Paid"})

        self.assertEqual(mock_create.call_args[0][0]["cashier"], user)
