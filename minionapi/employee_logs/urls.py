from django.urls import path

from . import views

app_name = "employee_logs"
urlpatterns = [
    path("entry/", views.WorkEntryCreate.as_view(), name="entry-create"),
    path("entry/team/<start>/<end>/",
         views.WorkEntryTeamList.as_view(), name="entry-team-list"
         ),
    path("entry/team/<start>/<end>/download/", views.WorkEntryTeamRangeDownload.as_view(),
         name="entry-team-list-download"
         ),
    path("entry/<date>/", views.WorkEntryList.as_view(),
         name="entry-list-create"
         ),
    path("entry/range/<start>/<end>/", views.WorkEntryRangeList.as_view(),
         name="entry-list-range-create"
         ),
    path("entry/range/<start>/<end>/download/", views.WorkEntryRangeDownload.as_view(),
         name="entry-list-range-download"
         ),
    path("entry/id/<pk>/", views.WorkEntryRetrieveUpdateDestroy.as_view(),
         name="entry-retrieve-update-destroy"
         )
]
