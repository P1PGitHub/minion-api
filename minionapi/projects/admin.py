from django.contrib import admin

from . import models

admin.site.register(models.Project)
admin.site.register(models.Client)
admin.site.register(models.Member)
admin.site.register(models.Update)
admin.site.register(models.Task)
admin.site.register(models.TaskMember)
