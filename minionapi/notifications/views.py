from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from . import models, serializers


class CurrentUserNotificationList(generics.ListAPIView):

    permissions = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user, is_dismissed=False)


class DismissedUserNotificationList(generics.ListAPIView):

    permissions = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user, is_dismissed=True)[:50]


class NotificationCreate(generics.CreateAPIView):

    permissions = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer


class NotificationDismiss(APIView):

    permissions = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notif = get_object_or_404(models.Notification, pk=kwargs["pk"])
        notif.dismiss()
        return Response(status=200, data=serializers.NotificationSerializer(notif).data)


class NotificationDismissAll(APIView):

    permissions = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifs = models.Notification.objects.filter(
            user=request.user, is_dismissed=False)
        for notif in notifs:
            notif.dismiss()

        return Response(status=200, data=serializers.NotificationSerializer(notifs, many=True).data)
