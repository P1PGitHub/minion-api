from rest_framework import serializers

from . import models
from projects import serializers as project_serializers
from reports import serializers as report_serializers


class NotificationSerializer(serializers.ModelSerializer):

    project = project_serializers.ProjectSimpleSerializer
    report = report_serializers.ReportSerializer

    class Meta:
        model = models.Notification
        fields = "__all__"
