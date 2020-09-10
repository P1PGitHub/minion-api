import base64
from datetime import datetime
import os

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class ReportDetail(generics.RetrieveDestroyAPIView):

    serializer_class = serializers.ReportSerializer
    permissions = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(models.Report, id=self.kwargs.get("report_id"))


class ReportList(generics.ListAPIView):

    serializer_class = serializers.ReportSerializer
    permissions = [IsAuthenticated]
    queryset = models.Report.objects.all()


class ReportPublish(APIView):

    permissions = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        print(kwargs)
        report = get_object_or_404(models.Report, id=kwargs["report_id"])
        report.draft = False
        report.save()
        return Response(status=200, data=serializers.ReportSerializer(report).data)


class CustomerServiceList(generics.ListCreateAPIView):

    serializer_class = serializers.CustomerServiceSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.CustomerService.objects.filter(
            team=self.request.user.team
        ).filter(
            draft=False
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CustomerServiceDraftsList(generics.ListAPIView):

    serializer_class = serializers.CustomerServiceSimpleSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.CustomerService.objects.filter(
            author=self.request.user
        ).filter(draft=True).order_by("-created_at")[:10]


class CustomerServiceRecentList(generics.ListAPIView):

    serializer_class = serializers.CustomerServiceSimpleSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.CustomerService.objects.filter(
            author=self.request.user
        ).filter(draft=False).order_by("-created_at")[:10]


class CustomerServiceRetrieveUpdate(generics.RetrieveUpdateAPIView):

    serializer_class = serializers.CustomerServiceNestedSerializer
    permissions = [IsAuthenticated]
    queryset = models.CustomerService.objects.all()


class CustomerServiceSimpleList(generics.ListAPIView):

    serializer_class = serializers.CustomerServiceSimpleSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        print(self.request.user.team)
        return models.CustomerService.objects.filter(
            team=self.request.user.team
        ).filter(
            draft=False
        ).order_by("-created_at")


class InventoryCheckOutListCreate(generics.ListCreateAPIView):

    serializer_class = serializers.InventoryCheckOutSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.InventoryCheckOut.objects.filter(report=self.kwargs.get("report_id")).order_by("-created_at")[:10]

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super(InventoryCheckOutListCreate, self).get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        print(request.data)
        for inventory in request.data:
            inventory["report"] = kwargs["report_id"]
        return super(InventoryCheckOutListCreate, self).create(request)


class InventoryClear(APIView):

    permissions = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        models.InventoryCheckOut.objects.filter(
            report=self.kwargs["report_id"]).delete()
        return Response(status=204)


class SignatureRetreiveDelete(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.SignatureSerializer
    permissions = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(models.Signature, id=self.kwargs["signature_id"])


class SignatureCreate(generics.CreateAPIView):

    serializer_class = serializers.SignatureSerializer
    permissions = [IsAuthenticated]


class TimeEntryListCreate(generics.ListCreateAPIView):

    serializer_class = serializers.TimeEntrySerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.TimeEntry.objects.filter(report=self.kwargs.get("report_id"))

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super(TimeEntryListCreate, self).get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        print(request.data)
        if isinstance(request.data, list):
            for inventory in request.data:
                inventory["report"] = kwargs["report_id"]
        else:
            request.data["report"] = kwargs["report_id"]
        return super(TimeEntryListCreate, self).create(request)


class TimeEntryClear(APIView):

    permissions = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        models.TimeEntry.objects.filter(
            report=self.kwargs["report_id"]).delete()
        return Response(status=204)
