from datetime import datetime
import os

from django.conf import settings
from rest_framework import serializers

from . import models


class CustomerServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerService
        fields = "__all__"


class CustomerServiceSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerService
        fields = ["client_name", "company_name", "author",
                  "report_type", "id", "billable", "description",
                  "created_at"]


class InventoryCheckOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InventoryCheckOut
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Report
        fields = "__all__"


class SignatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Signature
        fields = "__all__"


class TimeEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TimeEntry
        fields = "__all__"


class CustomerServiceNestedSerializer(serializers.ModelSerializer):

    inventory_checkouts = InventoryCheckOutSerializer(
        many=True, required=False, allow_null=True)
    time_records = serializers.SerializerMethodField(
        required=False, allow_null=True)
    signature = SignatureSerializer(required=False, allow_null=True)
    signatureID = serializers.PrimaryKeyRelatedField(
        queryset=models.Signature.objects.all(),
        source='signature',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = models.CustomerService
        fields = "__all__"

    def get_time_records(self, instance):
        time_records = instance.time_records.all().order_by("start")
        if len(time_records):
            return TimeEntrySerializer(time_records, many=True).data
        else:
            return []
