from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class ProjectStatusChoicesList(APIView):

    permissions = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        choice_list = []
        for choice in models.STATUS_CHOICES:
            choice_list.append({"value": choice[0], "text": choice[1]})
        return Response(status=200, data=choice_list)


class UpdateStatusChoicesList(APIView):

    permissisions = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        choice_list = []
        for choice in models.UPDATE_STATUS_CHOICES:
            choice_list.append({'value': choice[0], 'text': choice[1]})
        return Response(status=200, data=choice_list)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 25


class ProjectListCreate(generics.ListCreateAPIView):

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permissions = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permissions = [IsAuthenticated]


class MemberRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    queryset = models.Member.objects.all()
    permissions = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.MemberNestedSerializer
        else:
            return serializers.MemberSerializer


class TaskRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    queryset = models.Task.objects.all()
    permissions = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.TaskNestedSerializer
        else:
            return serializers.TaskSerializer


class TaskMemberListCreate(generics.ListCreateAPIView):

    permissions = [IsAuthenticated]

    def get_queryset(self):
        task = get_object_or_404(models.Task, pk=self.kwargs.get("pk"))
        return models.TaskMember.objects.filter(task=task)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.TaskMemberNestedSerializer
        else:
            return serializers.TaskMemberSerializer

    def perform_create(self, serializer):
        task = get_object_or_404(models.Task, pk=self.kwargs.get("pk"))
        return serializer.save(task=task)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = serializers.TaskMemberNestedSerializer(instance)
        return Response(instance_serializer.data)


class TaskMemberRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    queryset = models.TaskMember.objects.all()
    permissions = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.TaskMemberNestedSerializer
        else:
            return serializers.TaskMemberSerializer


class TaskAssignSelf(APIView):

    permissions = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        task = get_object_or_404(models.Task, pk=kwargs["pk"])
        task_member_query = models.TaskMember.objects.filter(
            task=task, account=self.request.user)
        if not len(task_member_query):
            task_member = models.TaskMember.objects.create(
                task=task, account=self.request.user)
            return Response(status=200, data=serializers.TaskMemberSerializer(task_member).data)
        return Response(status=200, data=serializers.TaskMemberSerializer(task_member_query[0]).data)


class TaskComplete(APIView):

    permissions = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        task = get_object_or_404(models.Task, pk=kwargs["pk"])
        if not task.completed:
            task.complete(self.request.user)
        return Response(status=200, data=serializers.TaskSerializer(task).data)


class TaskUncomplete(APIView):

    permissions = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        task = get_object_or_404(models.Task, pk=kwargs["pk"])
        if task.completed:
            task.uncomplete(self.request.user)
        return Response(status=200, data=serializers.TaskSerializer(task).data)


class UpdateListCreate(generics.ListCreateAPIView):

    queryset = models.Update.objects.all()
    permissions = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.UpdateProjectNestedSerializer
        else:
            return serializers.UpdateSerializer


class UpdateStatusList(generics.ListAPIView):

    permissions = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.UpdateProjectNestedSerializer

    def get_queryset(self):
        return models.Update.objects.filter(status=self.kwargs.get("status").upper())


class UpdateRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    queryset = models.Update.objects.all()
    permissions = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.UpdateNestedSerializer
        else:
            return serializers.UpdateSerializer


class UserProjectList(generics.ListAPIView):

    serializer_class = serializers.ProjectSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        project_members = models.Member.objects.filter(
            account=self.request.user
        )
        project_id_list = []
        for mem in project_members:
            project_id_list.append(mem.project.pk)
        return models.Project.objects.filter(pk__in=project_id_list, active=True)


class UserTaskList(generics.ListAPIView):

    serializer_class = serializers.TaskProjectNestedSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        task_members = models.TaskMember.objects.filter(
            account=self.request.user)
        task_id_list = []
        for mem in task_members:
            task_id_list.append(mem.task.pk)
        return models.Task.objects.filter(pk__in=task_id_list, completed=False, project__active=True)


class UserUpdatesList(generics.ListAPIView):

    serializer_class = serializers.UpdateProjectNestedSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        project_members = models.Member.objects.filter(
            account=self.request.user)
        project_id_list = []
        for mem in project_members:
            project_id_list.append(mem.project.pk)
        return models.Update.objects.filter(project__pk__in=project_id_list).order_by("-created_at")[:10]


class UserUpdatesStatusList(generics.ListAPIView):

    serializer_class = serializers.UpdateProjectNestedSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        project_members = models.Member.objects.filter(
            account=self.request.user)
        project_id_list = []
        for mem in project_members:
            project_id_list.append(mem.project.pk)
        return models.Update.objects.filter(project__pk__in=project_id_list, status=self.kwargs.get("status").upper()).order_by("-created_at")[:10]


class ProjectClientListCreate(generics.ListCreateAPIView):

    permissions = [IsAuthenticated]
    serializer_class = serializers.ClientSerializer

    def get_queryset(self):
        project = get_object_or_404(
            models.Project, pk=self.kwargs.get("project_id"))
        return models.Client.objects.filter(project=project)

    def perform_create(self, serializer):
        project = get_object_or_404(
            models.Project, pk=self.kwargs.get("project_id"))
        serializer.save(project=project)


class ProjectMemberListCreate(generics.ListCreateAPIView):

    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.Member.objects.filter(project=self.kwargs.get("project_id"))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.MemberNestedSerializer
        else:
            return serializers.MemberSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(
            models.Project, pk=self.kwargs.get("project_id"))
        return serializer.save(project=project)


class ProjectUpdateListCreate(generics.ListCreateAPIView):

    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.Update.objects.filter(project=self.kwargs.get("project_id"))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.UpdateNestedSerializer
        else:
            return serializers.UpdateSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(
            models.Project, pk=self.kwargs.get("project_id"))

        serializer.save(project=project, created_by=self.request.user)


class ProjectTaskListCreate(generics.ListCreateAPIView):

    permissions = [IsAuthenticated]

    def get_queryset(self):
        return models.Task.objects.filter(project=self.kwargs.get("project_id"))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.TaskNestedSerializer
        else:
            return serializers.TaskSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(
            models.Project, pk=self.kwargs.get("project_id"))
        return serializer.save(project=project, created_by=self.request.user)


class ProjectRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectNestedSerializer
    permissions = [IsAuthenticated]
