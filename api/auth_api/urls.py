from django.contrib.auth.models import User
from django.urls import include, path, re_path
from django.urls.conf import include, path
from rest_framework import routers, serializers, viewsets

from . import views


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    re_path(r"^totp/create/$", views.TOTPCreateView.as_view(), name="totp-create"),
    re_path(r"^totp/login/(?P<token>[0-9]{6})/$", views.TOTPVerifyView.as_view(), name="totp-login"),
    path("get-token/", views.CustomAuthToken.as_view()),
]
