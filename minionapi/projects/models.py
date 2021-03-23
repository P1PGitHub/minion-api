from django.db import models


class Project(models.Model):

    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)

    def __str__(self):
        return self.summary


class Client(models.Model):

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="clients", related_query_name="client")
    client_id = models.PositiveIntegerField(verbose_name="Client ID")
    client_name = models.CharField(max_length=255)
    primary = models.BooleanField(default=False)

    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=24, blank=True)

    def __str__(self):
        return f"{self.client_name} - {self.project.summary}"


class Member(models.Model):

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members", related_query_name="member")
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.full_name} - {self.project.summary}"


class Update(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.project.summary}"


class Task(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    created_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True)
    parent_task = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True)
    index = models.SmallIntegerField(default=-1)

    def __str__(self):
        return f"{self.title} - {self.project}"


class TaskMember(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name="members", related_query_name="member")
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)

    class meta:
        verbose_name = "Task Member"
        verbose_name_plural = "Task Members"
