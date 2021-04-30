from api.user.permission import UserListPermission
from auth_api.models import Profile
from django.contrib.auth.hashers import make_password
from rest_framework import mixins, routers, serializers, viewsets
from rest_framework.viewsets import GenericViewSet

from .serialiser import ProfileCreationSerializer, ProfileSerializer


# ViewSets define the view behavior.
class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [UserListPermission]


class UserCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreationSerializer
    permission_classes = [UserListPermission]
