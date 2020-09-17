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
    time_records = TimeEntrySerializer(
        many=True, required=False, allow_null=True)
    signature = SignatureSerializer(required=False, allow_null=True)
    signatureID = serializers.PrimaryKeyRelatedField(
        queryset=models.Signature.objects.all(),
        required=True,
        source='signature',
        write_only=True
    )

    class Meta:
        model = models.CustomerService
        fields = "__all__"
