from rest_framework import serializers

from .models import (
    RFIDReader,
    RFIDTag,
    RFIDScan,
    RFIDMovement,
)


class RFIDReaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = RFIDReader
        fields = "__all__"


class RFIDTagSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True
    )

    class Meta:
        model = RFIDTag
        fields = "__all__"


class RFIDScanSerializer(serializers.ModelSerializer):

    tag_uid = serializers.CharField(
        source="tag.uid",
        read_only=True
    )

    reader_name = serializers.CharField(
        source="reader.name",
        read_only=True
    )

    class Meta:
        model = RFIDScan
        fields = "__all__"


class RFIDMovementSerializer(serializers.ModelSerializer):

    tag_uid = serializers.CharField(
        source="tag.uid",
        read_only=True
    )

    class Meta:
        model = RFIDMovement
        fields = "__all__"