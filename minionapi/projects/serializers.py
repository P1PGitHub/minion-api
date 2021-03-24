from rest_framework import serializers

from . import models
from accounts import serializers as account_serializers


class ProjectSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = [
            "summary",
            "due_date",
            "status"
        ]


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "created_by"
        ]


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "created_by"
        ]


class ClientSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = [
            "project",
            "client_id",
            "client_name",
            "primary"
        ]


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Member
        fields = "__all__"
        read_only_fields = [
            "created_at"
        ]


class MemberSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Member
        fields = [
            "project",
            "account"
        ]


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Update
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "created_by"
        ]


class UpdateSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Update
        fields = [
            "project",
            "title"
        ]


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Task
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "created_by"
        ]


class TaskSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Task
        fields = [
            "project",
            "title",
            "completed",
            "parent_task",
            "index"
        ]


class TaskMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TaskMember
        fields = "__all__"


class TaskMemberNestedSerializer(serializers.ModelSerializer):

    account = account_serializers.AccountNameSerializer()

    class Meta:
        model = models.TaskMember
        fields = "__all__"
        read_only_fieds = [
            "created_at"
        ]


class TaskProjectNestedSerializer(serializers.ModelSerializer):

    project = ProjectSerializer()

    class Meta:
        model = models.Task
        fields = "__all__"
        read_only_fieds = ["created_at"]


class TaskNestedSerializer(serializers.ModelSerializer):

    members = TaskMemberNestedSerializer(many=True)

    class Meta:
        model = models.Task
        fields = "__all__"
        read_only_fieds = [
            "created_at",
            "created_by"
        ]


class MemberNestedSerializer(serializers.ModelSerializer):

    account = account_serializers.AccountNameSerializer()

    class Meta:
        model = models.Member
        exclude = ["project"]
        read_only_fields = [
            "account",
            "created_at"
        ]


class UpdateNestedSerializer(serializers.ModelSerializer):

    created_by = account_serializers.AccountNameSerializer()

    class Meta:
        model = models.Update
        exclude = ["project"]
        read_only_fields = [
            "created_by",
            "created_at"
        ]


class ProjectNestedSerializer(serializers.ModelSerializer):

    clients = ClientSerializer(many=True, read_only=True)
    members = MemberNestedSerializer(many=True, read_only=True)
    updates = UpdateNestedSerializer(many=True, read_only=True)
    tasks = TaskNestedSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = "__all__"
        read_only_fields = ["created_at", "created_by"]