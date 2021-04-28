from rest_framework import permissions


class UserListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" and view.action == "list":
            return request.user.is_staff
        if request.method == "GET" and view.action == "retrieve":
            return True
        if request.method == "POST":
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET" and view.action == "retrieve":
            try:
                return request.user.profile.id == obj.id or request.user.is_staff
            except AttributeError:
                return False
        return False
