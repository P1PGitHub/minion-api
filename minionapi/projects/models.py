from django.db import models
from django.utils import timezone


STATUS_CHOICES = (
    ("PROPOSED", 'Proposed'),
    ("IN PROGRESS", 'In Progress'),
    ("AWAITING CUSTOMER", 'Awaiting Customer'),
    ("AWAITING SUPPORT", 'Awaiting Support'),
    ("UNDER REVIEW", 'Under Review'),
    ("COMPLETED", 'Completed'),
    ("CANCELLED", 'Cancelled')
)

UPDATE_STATUS_CHOICES = (
    ("URGENT", "Urgent"),
    ("INFO", "Informational"),
    ("REMARK", "Remark"),
    ("POSITIVE", "Positive")
)


class Project(models.Model):

    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField(blank=True)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="PROPOSED")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["active", "-created_at"]

    def __str__(self):
        return self.summary

    def save(self, *args, **kwargs):
        new_instance = not bool(self.pk)
        self.active = not self.status in ["COMPLETED", "CANCELLED"]
        super(Project, self).save(*args, **kwargs)
        if new_instance:
            Update.objects.create(
                project=self, title="New project has been created.",
                message=self.description)
            Member.objects.create(project=self, account=self.created_by)


class Client(models.Model):

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="clients", related_query_name="client")
    client_id = models.PositiveIntegerField(verbose_name="Client ID")
    client_name = models.CharField(max_length=255)
    primary = models.BooleanField(default=False)

    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=24, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["primary", "client_name"]
        unique_together = ["client_id", "project"]

    def __str__(self):
        return f"{self.client_name} - {self.project.summary}"

    def save(self, *args, **kwargs):
        new_instance = not bool(self.pk)
        super(Client, self).save(*args, **kwargs)
        if new_instance:
            Update.objects.create(
                project=self.project,
                title=f"Client {self.client_name} has been added to this project.",
                created_by=self.created_by)
        if self.primary:
            other_clients = Client.objects.filter(
                project=self.project).exclude(pk=self.pk)
            for client in other_clients:
                if client.primary:
                    client.primary = False
                    client.save()


class Member(models.Model):

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members", related_query_name="member")
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["account__last_name", "account__first_name"]
        unique_together = ["project", "account"]

    def __str__(self):
        return f"{self.account.full_name} - {self.project.summary}"

    def save(self, *args, **kwargs):
        new_instance = not bool(self.pk)
        super(Member, self).save(*args, **kwargs)
        if new_instance:
            Update.objects.create(
                project=self.project, title=f"{self.account.short_name} has joined this project.")


class Update(models.Model):

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="updates", related_query_name="update")
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=32, choices=UPDATE_STATUS_CHOICES, default="INFO")
    edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.project.summary}"

    def save(self, *args, **kwargs):
        new_instance = not bool(self.pk)
        self.edited = not new_instance
        super(Update, self).save(*args, **kwargs)


class Task(models.Model):

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks", related_query_name="task")
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    completed_by = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, blank=True, null=True, related_name="completed_tasks", related_query_name="completed_task")
    index = models.SmallIntegerField(default=-1)

    def __str__(self):
        return f"{self.title} - {self.project}"

    def save(self, *args, **kwargs):
        new_instance = not bool(self.pk)
        super(Task, self).save(*args, **kwargs)
        if new_instance:
            Update.objects.create(
                project=self.project,
                title=f"Task '{self.title}' has been added.",
                message=self.message,
                created_by=self.created_by
            )

    def complete(self, user):
        task_member = TaskMember.objects.filter(task=self, account=user)
        if not len(task_member):
            TaskMember.objects.create(task=self, account=user)
        self.completed = True
        self.completed_at = timezone.now()
        self.completed_by = user
        Update.objects.create(
            title=f"{user.short_name} has completed Task '{self.title}'",
            project=self.project,
            created_by=user,
            status="POSITIVE"
        )
        self.save()

    def uncomplete(self, user):
        if self.completed:
            Update.objects.create(
                title=f"{user.short_name} has marked Task '{self.title}' as incomplete",
                project=self.project,
                created_by=user,
                status="INFO"
            )
            self.completed = False
            self.completed_at = None
            self.completed_by = None
            self.save()

    class Meta:
        ordering = ["index", "-created_at"]


class TaskMember(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name="members", related_query_name="member")
    account = models.ForeignKey(
        "accounts.Account", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Task Member"
        verbose_name_plural = "Task Members"
        ordering = ["account__last_name", "account__first_name"]
        unique_together = ["task", "account"]

    def __str__(self):
        return f"{self.account.full_name} - {self.task.title}"
