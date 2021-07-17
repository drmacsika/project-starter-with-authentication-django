from allauth.account.utils import get_next_redirect_url
from allauth.account.views import EmailVerificationSentView, SignupView
from django.urls import reverse_lazy


class CustomSignupView(SignupView):
    success_url = "reverse_lazy('accounts:email_verification_sent')"

    def get_success_url(self):
        ret = get_next_redirect_url(
            self.request, self.redirect_field_name) or self.success_url
        return ret


class CustomEmailVerificationSentView(EmailVerificationSentView):
    template_name = "accounts/verification_sent.html"
