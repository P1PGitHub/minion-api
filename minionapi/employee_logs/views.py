from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework import generics

from . import models
from . import serializers


class WorkEntryListCreate(generics.ListCreateAPIView):

    def get_queryset(self):
        request_date = datetime.strptime(self.kwargs.get(
            "date"), "%Y%m%d%H%M")
        request_end = request_date + timedelta(days=1)

        return models.WorkEntry.objects.filter(start__gte=request_date).filter(end__lte=request_end).filter(user=self.request.user).order_by("-start")

    def get_serializer_class(self):
        if (self.request.method == "GET"):
            return serializers.WorkEntrySimpleSerializer
        else:
            return serializers.WorkEntrySerializer


class WorkEntryCreate(generics.CreateAPIView):

    serializer_class = serializers.WorkEntrySerializer


class WorkEntryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.WorkEntrySerializer
    queryset = models.WorkEntry.objects.all()