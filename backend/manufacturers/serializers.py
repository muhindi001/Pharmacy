from rest_framework import serializers
from .models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):

    medicines_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Manufacturer

        fields = "__all__"