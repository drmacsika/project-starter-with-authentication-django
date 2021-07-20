from allauth.account.views import (ConfirmEmailView, EmailVerificationSentView,
                                   LoginView, LogoutView, PasswordChangeView,
                                   PasswordResetDoneView,
                                   PasswordResetFromKeyDoneView,
                                   PasswordResetFromKeyView, PasswordResetView,
                                   PasswordSetView, SignupView)
from django.http import request
from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView

from accounts.views import (CustomPasswordChangeView,
                            CustomPasswordResetFromKeyView,
                            CustomPasswordResetView, CustomPasswordSetView,
                            CustomSignupView)

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', SignupView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('confirm-email/', EmailVerificationSentView.as_view(template_name="accounts/verification_sent.html"),
         name='email_verification_sent'),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", ConfirmEmailView.as_view(
        template_name='accounts/email_confirm.html'), name='confirm_email'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path("password/change/", CustomPasswordChangeView.as_view(),
         name="change_password"),
    path("password/set/", CustomPasswordSetView.as_view(), name="set_password"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="reset_password"),
    path(
        "password/reset/done/", PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", CustomPasswordResetFromKeyView.as_view(), name="reset_password_from_key",
    ),
    path(
        "password/reset/key/done/", PasswordResetFromKeyDoneView.as_view(template_name='accounts/password_reset_from_key_done.html'), name="reset_password_from_key_done",
    ),


    # Permanently redirect all default django allauth URLS to the custom URLS we created
    # This is essential for security because it prevents users or bots from
    # getting access to the default authentication urls created by allauth

    path('accounts/login/',
         RedirectView.as_view(url=reverse_lazy('accounts:login'), permanent=True)),
    path('accounts/signup/',
         RedirectView.as_view(url=reverse_lazy('accounts:signup'), permanent=True)),
    path('accounts/logout/',
         RedirectView.as_view(url=reverse_lazy('accounts:logout'), permanent=True)),
    path('accounts/confirm-email/',
         RedirectView.as_view(url=reverse_lazy('accounts:email_verification_sent'), permanent=True)),
    path('accounts/password/change/',
         RedirectView.as_view(url=reverse_lazy('accounts:change_password'), permanent=True)),
    path('accounts/password/set/',
         RedirectView.as_view(url=reverse_lazy('accounts:set_password'), permanent=True)),
    path('accounts/password/reset/',
         RedirectView.as_view(url=reverse_lazy('accounts:reset_password'), permanent=True)),
    path('accounts/password/reset/done/',
         RedirectView.as_view(url=reverse_lazy('accounts:reset_password_done'), permanent=True)),
    path('accounts/password/reset/key/done/',
         RedirectView.as_view(url=reverse_lazy('accounts:reset_password_from_key_done'), permanent=True)),
    path('accounts/email/',
         RedirectView.as_view(url=reverse_lazy('home'), permanent=False)),
    path('accounts/inactive/',
         RedirectView.as_view(url=reverse_lazy('home'), permanent=False)),
]


'''
urlpatterns = [
    path("inactive/", views.account_inactive, name="account_inactive"),
    # E-mail
    path("email/", views.email, name="account_email"),

]


'''
