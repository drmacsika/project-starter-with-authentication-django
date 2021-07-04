from allauth.account.views import (EmailVerificationSentView, LoginView,
                                   LogoutView, SignupView)
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', SignupView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('confirm-email/', EmailVerificationSentView.as_view(
        template_name='accounts/verification_sent.html'), name='signup_confirm_email'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
