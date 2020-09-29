from django.db import models


class WorkEntry(models.Model):

    company_id = models.PositiveIntegerField(verbose_name="Company ID")
    company_name = models.CharField(
        max_length=255, verbose_name="Company Name")
    client_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Client Name"
    )

    start = models.DateTimeField()
    end = models.DateTimeField()

    description = models.TextField()
    summary = models.TextField()
    resolved = models.BooleanField(default=True)
    followup = models.TextField(blank=True, null=True)

    user = models.ForeignKey(
        "accounts.account",
        models.SET_NULL,
        null=True,
        related_name="work_entries",
        related_query_name="work_entry"
    )
    team = models.ForeignKey(
        "teams.team",
        models.CASCADE,
        related_name="work_entries",
        related_query_name="work_entry",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Work Entry"
        verbose_name_plural = "Work Entries"

    def __str__(self):
        return self.description
