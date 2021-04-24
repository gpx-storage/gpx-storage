from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_two_factor_enabled = models.BooleanField(default=False)


admin.site.register(Profile)
