from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.AccountDetail.as_view(), name="current"),
    path("simple/", views.AccountSimpleDetail.as_view(), name="current-simple"),
    path("new/", views.AccountCreate.as_view(), name="new")
]
