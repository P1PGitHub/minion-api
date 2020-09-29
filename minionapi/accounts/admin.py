from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class AccountAdmin(UserAdmin):

    list_filter = ["staff", ]
    list_display = ["full_name", "email", "team"]
    filter_horizontal = []
    ordering = ["team", "last_name", "first_name"]

    fieldsets = [
        (None, {
            "fields": ("email", "password")}
         ),
        ("Personal Info", {
            "fields": ("first_name", "last_name")}
         ),
        ("Connectwise", {
            "fields": ("cw_public", "cw_private")}
         ),
        ("Additional Account Info", {
            "fields": ("team", "active", "staff", "admin", "report_admin", "last_login")}
         )]
    add_fieldsets = [
        (None, {
            "fields": ("email", "password1", "password2")}
         ),
        ("Personal Info", {
            "fields": ("first_name", "last_name")}
         ),
        ("Connectwise", {
            "fields": ("cw_public", "cw_private")}
         ),
        ("Additional Account Info", {
            "fields": ("team", "active", "staff", "admin", "last_login")}
         )]


admin.site.register(models.Account, AccountAdmin)
