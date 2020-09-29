from rest_framework.serializers import ModelSerializer

from . import models


class WorkEntrySerializer(ModelSerializer):

    class Meta:
        model = models.WorkEntry
        fields = "__all__"


class WorkEntrySimpleSerializer(ModelSerializer):

    class Meta:
        model = models.WorkEntry
        fields = [
            "id",
            "company_name",
            "client_name",
            "start",
            "end",
            "description",
            "resolved"
        ]
