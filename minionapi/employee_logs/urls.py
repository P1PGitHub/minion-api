from django.urls import path

from . import views

app_name = "employee_logs"
urlpatterns = [
    path("entry/<date>/", views.WorkEntryListCreate.as_view(),
         name="entry-list-create")
]
