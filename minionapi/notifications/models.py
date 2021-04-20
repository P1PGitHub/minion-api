from datetime import datetime

from django.db import models
import uuid


class Notification(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey("accounts.Account", on_delete=models.CASCADE,
                             related_name="notifications", related_query_name="notification")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, blank=True, null=True)

    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)

    send_email = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(blank=True, null=True)

    is_dismissed = models.BooleanField(default=False)
    dismissed_at = models.DateTimeField(blank=True, null=True)

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, blank=True, null=True)
    report = models.ForeignKey(
        "reports.Report", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self):
        return self.title

    def dismiss(self):
        self.is_dismissed = True
        self.dismissed_at = datetime.now()
        self.save()
