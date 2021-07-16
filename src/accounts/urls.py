from allauth.account.views import (ConfirmEmailView, EmailVerificationSentView,
                                   LoginView, LogoutView, SignupView)
from django.urls import path, re_path, reverse_lazy

from accounts.views import CustomEmailVerificationSentView, CustomSignupView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', SignupView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('confirm-email/', EmailVerificationSentView.as_view(
        template_name='accounts/verification_sent.html'), name='email_verification_sent'),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", ConfirmEmailView.as_view(
        template_name='accounts/email_confirm.html'), name='confirm_email'),

    path('logout/', LogoutView.as_view(), name='logout'),
]


'''
urlpatterns = [
    path("signup/", views.signup, name="account_signup"),
    path("login/", views.login, name="account_login"),
    path("logout/", views.logout, name="account_logout"),
    path(
        "password/change/",
        views.password_change,
        name="account_change_password",
    ),
    path("password/set/", views.password_set, name="account_set_password"),
    path("inactive/", views.account_inactive, name="account_inactive"),
    # E-mail
    path("email/", views.email, name="account_email"),
    path(
        "confirm-email/",
        views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="account_confirm_email",
    ),
    # password reset
    path("password/reset/", views.password_reset, name="account_reset_password"),
    path(
        "password/reset/done/",
        views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
]


'''
