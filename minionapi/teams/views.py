from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

from accounts import models as account_models
from accounts import serializers as account_serializers


class AccountTeamDetail(generics.RetrieveAPIView):
    serializer_class = serializers.TeamSerializer

    def get_object(self):
        return models.Team.objects.get(pk=self.request.user.team)


class TeamIDDetail(generics.RetrieveAPIView):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()


class TeamSlugDetail(generics.RetrieveAPIView):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()
    lookup_field = "slug"


class TeamActiveUsersList(generics.ListAPIView):
    serializer_class = account_serializers.AccountSimpleSerializer

    def get_queryset(self):
        return account_models.Account.objects.filter(active=True).filter(team=self.request.user.team)


class TeamAllUsersList(generics.ListAPIView):
    serializer_class = account_serializers.AccountSimpleSerializer

    def get_queryset(self):
        return account_models.Account.objects.filter(team=self.request.user.team)
