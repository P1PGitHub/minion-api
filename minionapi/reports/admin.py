from django.contrib import admin

from . import models
from . import utilities

# Register your models here.


class CustomerServiceAdmin(admin.ModelAdmin):
    list_display = (
        'team',
        'company_name',
        'client_name',
        'company_id',
        "draft",
        'billable',
        'author',
        'service_type',
    )

    list_filter = (
        'draft',
        'service_type'
    )

    save_as = True
    save_on_top = True

    search_fields = (
        'author__first_name',
        'author__last_name',
        'author__email',
        'team__name',
        'description',
        'summary',
        'client_name',
        'company_id'
    )

    def save_model(self, request, obj, form, change):
        obj.edited_by = request.user
        super().save_model(request, obj, form, change)

        if not obj.draft:
            spread_data = utilities.build_spread(obj.id)
            utilities.email_spread(
                spread_data["report"], spread_data["spread_file"],
                [request.user.email],
                updated_model=True
            )


admin.site.register(models.CustomerService, CustomerServiceAdmin)
admin.site.register(models.InventoryCheckOut)
admin.site.register(models.Report)
admin.site.register(models.Signature)
admin.site.register(models.TimeEntry)
