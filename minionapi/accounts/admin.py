from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class AccountAdmin(UserAdmin):
    pass


admin.site.register(models.Account, AccountAdmin)
