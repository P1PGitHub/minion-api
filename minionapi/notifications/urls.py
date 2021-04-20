from django.urls import path

from . import views

app_name = "notifications"
urlpatterns = [
    path("", views.CurrentUserNotificationList.as_view(),
         name="user-current"),
    path("dismiss_all/", views.NotificationDismissAll.as_view(), name="dismiss-all"),
    path("dismissed/", views.DismissedUserNotificationList.as_view(),
         name="user-dimissed"),
    path("new/", views.NotificationCreate.as_view(),
         name="create"),
    path("<pk>/dismiss/", views.NotificationDismiss.as_view(), name="dismiss"),
]
