from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "action",
            "module",
            "object_id",
            "description",
            "username",
            "full_name",
            "ip_address",
            "user_agent",
            "metadata",
            "created_at",
        )

    def get_full_name(self, obj):

        if obj.user:
            return obj.user.get_full_name()

        return None