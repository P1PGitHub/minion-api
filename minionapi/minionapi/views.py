from django.views.generic.base import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HomeView(TemplateView):
    template_name = "home.html"


class HelloView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        return Reponse("Hello")
