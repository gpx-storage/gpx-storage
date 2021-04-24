from auth_api.custom_auth import CustomTokenAuthentication
from django.shortcuts import render
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import permissions, status, views
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class gpx_test(views.APIView):
    """
    test view with jwt
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({"test": "success"}, status=status.HTTP_200_OK)
