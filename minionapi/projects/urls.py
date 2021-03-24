from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.ProjectListCreate.as_view(), name="project-list"),
    path("<pk>/", views.ProjectRetrieveUpdateDelete.as_view(),
         name="project-retrieve"),
    path("<project_id>/clients/", views.ProjectClientListCreate.as_view(),
         name="project-clients-list"),
    path("<project_id>/members/", views.ProjectMemberListCreate.as_view(),
         name="project-members-list"),
    path("<project_id>/updates/", views.ProjectUpdateListCreate.as_view(),
         name="project-updates-list"),
    path("<project_id>/tasks/", views.ProjectTaskListCreate.as_view(),
         name="project-tasks-list"),
    path("clients/<pk>/", views.ClientRetrieveUpdateDelete.as_view(),
         name="client-retrieve"),
    path("members/<pk>/", views.MemberRetrieveUpdateDelete.as_view(),
         name="member-retrieve"),
    path("tasks/user/", views.UserTaskList.as_view(), name="user-tasks-list"),
    path("tasks/<pk>/", views.TaskRetrieveUpdateDelete.as_view(),
         name="task-retrieve"),
    path("tasks/<pk>/complete/", views.TaskComplete.as_view(), name="task-complete"),
    path("tasks/<pk>/members/", views.TaskMemberListCreate.as_view(),
         name="task-members-list"),
    path("task_members/<pk>/", views.TaskMemberRetrieveUpdateDelete.as_view(),
         name="task-member-retrieve"),
    path("updates/<pk>/", views.UpdateRetrieveUpdateDelete.as_view(),
         name="update-retrieve"),
]
