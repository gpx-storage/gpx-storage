from django.contrib.auth.models import User
from django.urls import include, path, re_path
from django.urls.conf import include, path
from rest_framework import routers, serializers, viewsets

from . import views

urlpatterns = [
    path("test/", views.gpx_test.as_view()),
]
