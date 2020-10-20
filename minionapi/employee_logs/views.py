from datetime import datetime, timedelta, timezone

from django.apps import apps
from django.shortcuts import render
from rest_framework import generics

from . import models
from . import serializers
from accounts import serializers as account_serializers


class WorkEntryList(generics.ListAPIView):

    serializer_class = serializers.WorkEntrySerializer

    def get_queryset(self):
        request_date = datetime.strptime(self.kwargs.get(
            "date"), "%Y%m%d%H%M").replace(tzinfo=timezone.utc)
        request_end = request_date + timedelta(days=1)

        return models.WorkEntry.objects.filter(start__gte=request_date).filter(end__lte=request_end).filter(user=self.request.user).order_by("-start")


class WorkEntryRangeList(generics.ListAPIView):

    serializer_class = serializers.WorkEntrySerializer

    def get_queryset(self):
        request_start = datetime.strptime(self.kwargs.get(
            "start"), "%Y%m%d%H%M").replace(tzinfo=timezone.utc)
        request_end = datetime.strptime(self.kwargs.get(
            "end"), "%Y%m%d%H%M").replace(tzinfo=timezone.utc) + timedelta(days=1)

        return models.WorkEntry.objects.filter(start__gte=request_start).filter(end__lte=request_end).filter(user=self.request.user).order_by("-start")


class WorkEntryCreate(generics.CreateAPIView):

    serializer_class = serializers.WorkEntrySerializer


class WorkEntryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.WorkEntrySerializer
    queryset = models.WorkEntry.objects.all()


class WorkEntryTeamList(generics.ListAPIView):

    serializer_class = account_serializers.AccountSimpleSerializer

    def get_queryset(self):
        return apps.get_model("accounts", "account").objects.filter(team=self.request.user.team)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        request_start = datetime.strptime(
            self.kwargs.get("start"), "%Y%m%d%H%M"
        ).replace(tzinfo=timezone.utc)
        request_end = datetime.strptime(self.kwargs.get(
            "end"), "%Y%m%d%H%M"
        ).replace(tzinfo=timezone.utc) + timedelta(days=1)

        for index, user in enumerate(res.data):
            user_obj = apps.get_model("accounts", "account").objects.get(
                pk=user["id"]
            )
            res.data[index].update({"work_entries": serializers.WorkEntrySimpleSerializer(
                models.WorkEntry.objects.filter(
                    user=user_obj.id
                ).filter(
                    start__gte=request_start
                ).filter(
                    end__lte=request_end
                ).order_by("-start"),
                many=True
            ).data})
        return res
