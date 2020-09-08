from datetime import datetime
import os

from django.conf import settings
from django.db import models
from django.utils.text import slugify


REPORT_CHOICES = [
    ("CUSTOMER_SERVICE", "Customer Service")
]


SERVICE_CHOICES = [
    ("INSTALL", "Installation"),
    ("SALES", "Sales"),
    ("SERVICE", "Service Trip"),
    ("TRAINING", "Training")
]


def folder(instance, filename):
    formatted_filename = datetime.now().strftime("%Y%m%d-%H%M%S.png")
    file_path = os.path.join("uploads", "signatures", slugify(
        instance.company), slugify(instance.client), formatted_filename)
    return file_path


class Signature(models.Model):

    ref = models.CharField(max_length=1024)
    company = models.CharField(max_length=255)
    client = models.CharField(max_length=255)

    def __str__(self):
        return self.file.name


class Report(models.Model):

    client_name = models.CharField(max_length=255, verbose_name="Client Name")
    company_id = models.PositiveIntegerField(verbose_name="Company ID")
    company_name = models.CharField(
        max_length=255, verbose_name="Company Name")
    report_type = models.CharField(max_length=255, choices=REPORT_CHOICES)
    draft = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        "accounts.account",
        models.SET_NULL,
        null=True,
        related_name="reports",
        related_query_name="report"
    )
    last_edited_by = models.ForeignKey(
        "accounts.account",
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="edited_reports",
        related_query_name="edited_report",
        verbose_name="Last Edited By"
    )

    def __str__(self):
        return f"{self.company_name} - {self.report_type}"


class CustomerService(Report):

    service_type = models.CharField(
        max_length=255, choices=SERVICE_CHOICES, verbose_name="Service Type")
    description = models.TextField()

    billable = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    pictures = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    satisfied = models.BooleanField(default=False)
    tested = models.BooleanField(default=False)

    summary = models.TextField()

    signature = models.ForeignKey(
        Signature,
        models.SET_NULL,
        related_name="customer_service_reports",
        related_query_name="customer_service_report",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.company_name} - {self.description}"

    class Meta:
        verbose_name = "Customer Service"
        verbose_name_plural = "Customer Service Reports"


class TimeEntry(models.Model):

    report = models.ForeignKey(
        Report, models.CASCADE, related_name="time_records", related_query_name="time_record")
    start = models.DateTimeField()
    end = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(
        "accounts.Account",
    )

    def __str__(self):
        return f"({self.start.strftime('%Y-%m-%d %H:%M')}) {self.report}"

    class Meta:
        verbose_name = "Time Entry"
        verbose_name_plural = "Time Entries"


class InventoryCheckOut(models.Model):

    report = models.ForeignKey(
        Report, models.CASCADE, related_name="inventory_checkouts", related_query_name="inventory_checkout"
    )
    description = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} ({self.serial})"

    class Meta:
        verbose_name = "Inventory Check Out"
        verbose_name_plural = "Inventory Check Outs"
