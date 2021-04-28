from django.contrib.auth.models import User
from django.urls import include, path, re_path
from django.urls.conf import include, path
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    re_path(r"^totp/create/$", views.TOTPCreateView.as_view(), name="totp-create"),
    re_path(r"^totp/login/(?P<token>[0-9]{6})/$", views.TOTPVerifyView.as_view(), name="totp-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/login/", views.CustomAuthToken.as_view()),
]
