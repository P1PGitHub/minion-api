from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.CustomerService)
admin.site.register(models.InventoryCheckOut)
admin.site.register(models.Report)
admin.site.register(models.Signature)
admin.site.register(models.TimeEntry)
