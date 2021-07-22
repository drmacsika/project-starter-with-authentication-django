from allauth.account.adapter import DefaultAccountAdapter, get_adapter
from allauth.account.app_settings import (AUTHENTICATION_METHOD,
                                          AuthenticationMethod)
from allauth.account.forms import (EmailAwarePasswordResetTokenGenerator,
                                   ResetPasswordForm)
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.utils import build_absolute_uri
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy

from .models import CustomUser

default_token_generator = EmailAwarePasswordResetTokenGenerator()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomResetPasswordForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get(
            "token_generator", default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse_lazy(
                "accounts:reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )
            url = build_absolute_uri(request, path)

            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
            }

            if AUTHENTICATION_METHOD != AuthenticationMethod.EMAIL:
                context["username"] = user_username(user)
            get_adapter(request).send_mail(
                "accounts/email/password_reset_key", email, context
            )
        return self.cleaned_data["email"]
