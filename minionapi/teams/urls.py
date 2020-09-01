from django.urls import path

from . import views

app_name = "teams"
urlpatterns = [
    path("", views.AccountTeamDetail.as_view(), name="current"),
    path("id/<uuid:pk>/", views.TeamIDDetail.as_view(), name="id"),
    path("slug/<str:slug>/", views.TeamSlugDetail.as_view(), name="slug"),
    path("members/", views.TeamActiveUsersList.as_view(), name="members"),
    path("members/all/", views.TeamAllUsersList.as_view(), name="members")
]
