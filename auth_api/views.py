from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import permissions, status, views
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from auth_api.custom_auth import CustomTokenAuthentication


def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        profile = user.profile
        if profile.is_two_factor_enabled:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "tmp": True, "email": user.email})

        to_ret = generate_jwt_token(user)
        return Response(to_ret)


class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        token, created = Token.objects.get_or_create(user=user)
        return Response({"otp_url": url, "tmp_token": token.key}, status=status.HTTP_201_CREATED)


class TOTPVerifyView(views.APIView):
    """
    Api to verify/enable a TOTP device
    """

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            return Response(
                dict(errors=["This user has not setup two factor authentication"]), status=status.HTTP_400_BAD_REQUEST
            )
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            profile = user.profile
            profile.is_two_factor_enabled = True
            profile.save()
            Token.objects.get(user=user).delete()
            return Response(generate_jwt_token(user), status=status.HTTP_200_OK)

        return Response(dict(errors=dict(token=["Invalid TOTP Token"])), status=status.HTTP_400_BAD_REQUEST)
