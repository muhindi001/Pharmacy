import uuid

import uuid

from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"