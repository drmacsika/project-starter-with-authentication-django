from allauth.account.utils import (get_next_redirect_url,
                                   passthrough_next_redirect_url)
from allauth.account.views import (EmailVerificationSentView,
                                   PasswordChangeView,
                                   PasswordResetFromKeyView, PasswordResetView,
                                   PasswordSetView,
                                   RedirectAuthenticatedUserMixin, SignupView,
                                   sensitive_post_parameters_m)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View


class CustomSignupView(SignupView):
    success_url = "reverse_lazy('accounts:email_verification_sent')"

    def get_success_url(self):
        ret = get_next_redirect_url(
            self.request, self.redirect_field_name) or self.success_url
        return ret


class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    success_url = reverse_lazy("accounts:reset_password_done")

    def get_context_data(self, **kwargs):
        ret = super(PasswordResetView, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(
            self.request, reverse_lazy(
                "accounts:login"), self.redirect_field_name
        )
        # NOTE: For backwards compatibility
        ret["password_reset_form"] = ret.get("form")
        # (end NOTE)
        ret.update({"login_url": login_url})
        return ret


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'accounts/password_reset_from_key.html'
    success_url = reverse_lazy("accounts:reset_password_from_key_done")

    def get_context_data(self, **kwargs):
        ret = super(PasswordResetFromKeyView, self).get_context_data(**kwargs)
        ret["action_url"] = reverse_lazy(
            "accounts:reset_password_from_key",
            kwargs={
                "uidb36": self.kwargs["uidb36"],
                "key": self.kwargs["key"],
            },
        )
        return ret


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:change_password")

    def render_to_response(self, context, **response_kwargs):
        if not self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse_lazy("accounts:set_password"))
        return super(PasswordChangeView, self).render_to_response(
            context, **response_kwargs
        )


@method_decorator(login_required, name='dispatch')
class CustomPasswordSetView(PasswordSetView):
    template_name = "accounts/password_set.html"
    success_url = reverse_lazy("accounts:set_password")

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse_lazy("accounts:change_password"))
        return super(PasswordSetView, self).dispatch(request, *args, **kwargs)
