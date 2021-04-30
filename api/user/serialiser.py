import django.contrib.auth.password_validation as validators
from api.user.fonctions import send_email_activation_to_new_user
from auth_api.models import Profile
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get("password")

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["id", "user", "is_two_factor_enabled"]


class ProfileCreationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    redirect_to = serializers.URLField(required=False)

    class Meta:
        model = Profile
        fields = ["id", "user", "is_two_factor_enabled", "redirect_to"]

    def create(self, validated_data):
        u = User.objects.create_user(
            username=validated_data["user"]["username"],
            email=validated_data["user"]["email"],
            password=validated_data["user"]["password"],
            is_active=False,
        )
        send_email_activation_to_new_user(self.context["request"], u, validated_data["redirect_to"])
        return Profile.objects.create(user=u)
