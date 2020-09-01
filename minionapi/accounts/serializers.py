from rest_framework import serializers

from . import models


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = "__all__"
        read_only_fields = ["id"]
        write_only_fields = ["password"]

    def create(self, validated_data):
        account = models.Account.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        try:
            account.team = validated_data["team"]
        except KeyError:
            account.team = None

        account.set_password(validated_data["password"])
        account.save()
        return account


class AccountSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = [
            "id",
            "last_login",
            "email",
            "first_name",
            "last_name",
            "active"
        ]
