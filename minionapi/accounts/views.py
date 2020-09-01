from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers


class AccountDetail(generics.RetrieveAPIView):
    serializer_class = serializers.AccountSerializer

    permissions = [IsAuthenticated]

    def get_object(self):
        return models.Account.objects.get(pk=self.request.user.id)


class AccountSimpleDetail(generics.RetrieveAPIView):
    serializer_class = serializers.AccountSimpleSerializer

    permissions = [IsAuthenticated]

    def get_object(self):
        return models.Account.objects.get(pk=self.request.user.id)


class AccountCreate(generics.CreateAPIView):

    model = models.Account()
    serializer_class = serializers.AccountSerializer
