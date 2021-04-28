from api.user.permission import UserListPermission
from auth_api.models import Profile
from django.contrib.auth.hashers import make_password
from rest_framework import mixins, routers, serializers, viewsets
from rest_framework.viewsets import GenericViewSet

from .serialiser import ProfileSerializer


# ViewSets define the view behavior.
class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [UserListPermission]
