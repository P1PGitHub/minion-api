from django.urls import path

from . import views

app_name = "employee_logs"
urlpatterns = [
    path("entry/", views.WorkEntryCreate.as_view(), name="entry-create"),
    path("entry/<date>/", views.WorkEntryListCreate.as_view(),
         name="entry-list-create")
]
