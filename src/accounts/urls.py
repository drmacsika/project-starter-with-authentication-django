from allauth.account.views import (ConfirmEmailView, EmailVerificationSentView,
                                   LoginView, LogoutView, PasswordChangeView,
                                   PasswordResetDoneView,
                                   PasswordResetFromKeyDoneView,
                                   PasswordResetFromKeyView, PasswordResetView,
                                   PasswordSetView, SignupView)
from django.urls import path, re_path, reverse_lazy

from accounts.views import (CustomEmailVerificationSentView,
                            CustomPasswordResetFromKeyView,
                            CustomPasswordResetView, CustomSignupView,
                            password_change_view, password_set_view)

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', SignupView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('confirm-email/', EmailVerificationSentView.as_view(
        template_name='accounts/verification_sent.html'), name='email_verification_sent'),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", ConfirmEmailView.as_view(
        template_name='accounts/email_confirm.html'), name='confirm_email'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("password/change/", password_change_view, name="change_password"),
    path("password/set/", password_set_view, name="set_password"),
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

]


'''
urlpatterns = [
    path("inactive/", views.account_inactive, name="account_inactive"),
    # E-mail
    path("email/", views.email, name="account_email"),
    
]


'''
