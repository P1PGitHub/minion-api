from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework import generics

from . import models
from . import serializers


class WorkEntryList(generics.ListAPIView):

    serializer_class = serializers.WorkEntrySerializer

    def get_queryset(self):
        request_date = datetime.strptime(self.kwargs.get(
            "date"), "%Y%m%d%H%M")
        request_end = request_date + timedelta(days=1)

        return models.WorkEntry.objects.filter(start__gte=request_date).filter(end__lte=request_end).filter(user=self.request.user).order_by("-start")


class WorkEntryRangeList(generics.ListAPIView):

    serializer_class = serializers.WorkEntrySerializer

    def get_queryset(self):
        request_start = datetime.strptime(self.kwargs.get(
            "start"), "%Y%m%d%H%M")
        request_end = datetime.strptime(self.kwargs.get(
            "end"), "%Y%m%d%H%M") + timedelta(days=1)

        return models.WorkEntry.objects.filter(start__gte=request_date).filter(end__lte=request_end).filter(user=self.request.user).order_by("-start")


class WorkEntryCreate(generics.CreateAPIView):

    serializer_class = serializers.WorkEntrySerializer


class WorkEntryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.WorkEntrySerializer
    queryset = models.WorkEntry.objects.all()