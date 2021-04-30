from django.urls import include, path
from rest_framework import routers

from . import views
from .user.viewset import UserCreateViewSet, UserViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users/create", UserCreateViewSet)
router.register(r"users", UserViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
