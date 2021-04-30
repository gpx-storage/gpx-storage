from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

UserModel = get_user_model()


def send_email_activation_to_new_user(request, user, redirect_to=None):
    current_site = get_current_site(request)
    mail_subject = "Activate your account."
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = f"http://{current_site.domain}{reverse('activate', args=[uid, token])}"
    if redirect_to != None:
        url += f"?redirect_to={redirect_to}"
    message = render_to_string(
        "api/acc_active_email.html",
        {"user": user, "url": url},
    )
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
