from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode

UserModel = get_user_model()

# Create your views here.
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        redirect_to = request.GET.get("redirect_to")
        if redirect_to:
            return HttpResponseRedirect(redirect_to)
        return HttpResponse(status=204)
    return HttpResponse(status=400)
