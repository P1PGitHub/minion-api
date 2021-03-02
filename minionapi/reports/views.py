import base64
from datetime import datetime, timedelta
import json
import os


import dateutil.parser
from django.apps import apps
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers
from . import utilities


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 25


class ReportDetail(generics.RetrieveDestroyAPIView):

    serializer_class = serializers.ReportSerializer
    permissions = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(models.Report, id=self.kwargs.get("report_id"))

    def delete(self, *args, **kwargs):
        report = self.get_object()
        print(report.draft)
        print(report.author.id)
        print(self.request.user.id)
        print(self.request.user.report_admin)
        if (report.draft == True and (report.author == self.request.user or self.request.user.report_admin)):
            return super().delete(*args, **kwargs)
        else:
            return Response(status=403)


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


class StaleReportList(generics.ListAPIView):

    serializer_class = serializers.ReportSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        stale_date = datetime.now() - timedelta(days=self.request.user.team.stale_report_age)
        return models.Report.objects.filter(author=self.request.user, created_at__lte=stale_date, draft=True)


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
        report = serializer.save(author=self.request.user)
        return report


class CustomerServiceSimpleDraftsList(generics.ListAPIView):

    serializer_class = serializers.CustomerServiceSimpleSerializer
    permissions = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return models.CustomerService.objects.filter(
            team=self.request.user.team
        ).filter(draft=True).order_by("-created_at")


class CustomerServiceRecentDraftsList(generics.ListAPIView):

    serializer_class = serializers.CustomerServiceSimpleSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.CustomerService.objects.filter(
            author=self.request.user
        ).filter(draft=True).order_by("-created_at")[:5]


class CustomerServiceRecentList(generics.ListAPIView):

    serializer_class = serializers.CustomerServiceSimpleSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.CustomerService.objects.filter(
            author=self.request.user
        ).filter(draft=False).order_by("-created_at")[:5]


class CustomerServiceRetrieveUpdate(generics.RetrieveUpdateAPIView):

    serializer_class = serializers.CustomerServiceNestedSerializer
    permissions = [IsAuthenticated]
    queryset = models.CustomerService.objects.all()

    def update(self, request, *args, **kwargs):
        update_response = super().update(request, *args, **kwargs)
        report = update_response.data

        if not report["draft"]:
            spread_data = utilities.build_spread(report["id"])
            utilities.email_spread(
                spread_data["report"], spread_data["spread_file"],
                [self.request.user.email]
            )

        return update_response


class CustomerServiceSimpleList(generics.ListAPIView):

    serializer_class = serializers.CustomerServiceSimpleSerializer
    permissions = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        print(self.request.user)
        print(self.request.user.team)
        return models.CustomerService.objects.filter(
            team=self.request.user.team
        ).filter(
            draft=False
        ).order_by("-created_at")


class CustomerServiceQuery(APIView):

    permissions = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        body_data = json.loads(request.body)
        print(body_data)
        customer_service_reports = models.CustomerService.objects.filter(
            created_at__gte=body_data['dates']['start'], team=self.request.user.team) | models.CustomerService.objects.filter(updated_at__gte=body_data['dates']['start'], team=self.request.user.team)
        if body_data['author']:
            customer_service_reports = customer_service_reports.filter(
                author=body_data['author']
            )
        if body_data["client"]:
            customer_service_reports = customer_service_reports.filter(
                company_id=body_data['client']
            )
        if not body_data["drafts"]:
            customer_service_reports = customer_service_reports.filter(
                draft=False
            )

        return Response(status=200, data=serializers.CustomerServiceSimpleSerializer(customer_service_reports.order_by("-created_at"), many=True).data)


class InventoryCheckOutListCreate(generics.ListCreateAPIView):

    serializer_class = serializers.InventoryCheckOutSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.InventoryCheckOut.objects.filter(report=self.kwargs.get("report_id")).order_by("-created_at")[:5]

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
