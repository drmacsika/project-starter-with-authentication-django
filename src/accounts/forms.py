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


# from allauth.account.forms import SignupForm
# from django import forms

# class CustomSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=30, label='First Name')
#     last_name = forms.CharField(max_length=30, label='Last Name')
#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
#         return user


# from django import forms
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model, authenticate, login
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from .models import Profile, EmailActivation
# from django.utils.safestring import mark_safe
# from django.utils.translation import gettext_lazy as _
# from django.urls import reverse
# from datetime import date
# # from django.utils.encoding import force_bytes
# # from django.utils.http import urlsafe_base64_encode
# # from django.contrib.auth.tokens import default_token_generator
# # from django.contrib.sites.shortcuts import get_current_site
# # from django.core.mail import EmailMultiAlternatives
# # from django.template import loader

# User = get_user_model()


# class UserAdminCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, and no repeated password."""

#     def validate_password(self):
#         if len(self) < 8:
#             raise ValidationError(
#                 _('Password requires minimum 8 characters.'),
#                 code='invalid',
#             )
#         if self.isdigit():
#             raise ValidationError(
#                 _("Your password can't be entirely numeric."),
#                 code='invalid',
#             )
#         if self.isalpha():
#             raise ValidationError(
#                 _('Your password must contain at least one number and/or special character.'),
#                 code='invalid',
#             )

#     password1 = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput,
#         strip=True,
#         validators=[validate_password],
#     )

#     def validate_fullname(self):
#         fullname = self.split()
#         if len(fullname) <= 1:
#             raise ValidationError(
#                 _('Kindly enter more than one name, please.'),
#                 code='invalid',
#                 params={'value': self},
#             )
#         for x in fullname:
#             if x.isalpha() is False or len(x) < 2:
#                 raise ValidationError(
#                     _('Please enter your name correctly.'),
#                     code='invalid',
#                     params={'value': self},
#                 )

#     name = forms.CharField(
#         label=_("Full Name"),
#         widget=forms.TextInput,
#         strip=True,
#         validators=[validate_fullname],
#     )

#     class Meta:
#         model = User
#         fields = ('name', 'email',)

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserAdminCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.email = user.email.lower()
#         user.name = user.name.title()
#         if commit:
#             user.save()
#         return user


# class UserAdminChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ('name', 'email', 'password', 'active', 'admin')

#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]


# class RegisterForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, and no repeated password."""
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }

#     name = forms.CharField(
#         label=_("Full Name"),
#         widget=forms.TextInput,
#         strip=True,
#         help_text=_(""),
#     )

#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=True,
#         widget=forms.PasswordInput,
#         help_text=_(""),
#         validators=[UserAdminCreationForm.validate_password],
#     )

#     class Meta:
#         model = User
#         fields = ('name', 'email',)

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(RegisterForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.email = user.email.lower().strip()
#         user.name = user.name.title()
#         user.active = False # Send email confirmation via post save signals
#         if commit:
#             user.save()
#         return user


# class ReactivateEmailForm(forms.Form):
#     email = forms.EmailField(max_length=254)

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         qs = EmailActivation.objects.email_exists(email)
#         if not qs.exists():
#             link1 = reverse("contact:contact_home")
#             reconfirm_msg2 = "Kindly <a href='{resend_link}' class='text-info'>contact us to learn more</a>.".format(
#                 resend_link=link1)
#             msg3 = "This email hasn't been registered before or is already activated. " + reconfirm_msg2
#             raise forms.ValidationError(_(mark_safe(msg3)), code='invalid')
#         return email


# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def __init__(self, request, *args, **kwargs):
#         self.request = request
#         super(LoginForm, self).__init__(*args, **kwargs)

#     def clean(self):
#         request = self.request
#         data = self.cleaned_data
#         email = data.get("email")
#         password = data.get("password")
#         user = authenticate(request, username=email, password=password)
#         if user is None:
#             raise forms.ValidationError("Incorrect email address or password!")
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             not_active = qs.filter(active=False)
#             if not_active.exists():
#                 link = reverse("signup_reconfirm_email")
#                 reconfirm_msg = "<a href='{resend_link}' class='text-secondary'>resend confirmation email</a>".format(resend_link=link)
#                 confirm_email = EmailActivation.objects.filter(email=email)
#                 is_confirmable = confirm_email.confirmable().exists()
#                 if is_confirmable:
#                     msg1 = "Your account is not yet confirmed. Kindly check your mail to confirm your account or you can " + reconfirm_msg.lower() + "."
#                     raise forms.ValidationError(mark_safe(msg1))
#                 confirmed_email_exists = EmailActivation.objects.email_exists(email).exists()
#                 if confirmed_email_exists:
#                     msg2 = "Your account is not yet confirmed. Kindly " + reconfirm_msg + " before you can login."
#                     raise forms.ValidationError(_(mark_safe(msg2)), code='invalid')
#                 if not is_confirmable or confirmed_email_exists:
#                     link1 = reverse("contact:contact_home")
#                     reconfirm_msg2 = "Kindly <a href='{resend_link}' class='text-secondary'>contact us for assistance</a>.".format(resend_link=link1)
#                     msg3 = "Your account is inactive. " + reconfirm_msg2
#                     raise forms.ValidationError(_(mark_safe(msg3)), code='invalid')
#         else:
#             link2 = reverse("signup")
#             reconfirm_msg3 = '<a href="{resend_link}" class="text-secondary">join sikademy to login</a>.'.format(resend_link=link2)
#             msg4 = "This email address is not registered yet. Kindly " + reconfirm_msg3
#             raise forms.ValidationError(_(mark_safe(msg4)), code='invalid')
#         login(request, user)
#         self.user = user
#         return data


# class AccountForm(forms.ModelForm):
#     name = forms.CharField(
#         label=_("Full Name"),
#         widget=forms.TextInput,
#         strip=True,
#         help_text=_(""),
#     )
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ('name', 'email',)

#     def __init__(self, *args, **kwargs):
#         super(AccountForm, self).__init__(*args, **kwargs)
#         self.fields['email'].disabled = True


# class ProfileForm(forms.ModelForm):
#     birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(date.today().year - 4, date.today().year - 100, -1), empty_label=("Choose Year", "Choose Month", "Choose Day")))

#     class Meta:
#         model = Profile
#         fields = ('profile_image', 'username', 'bio', 'location', 'occupation', 'birth_date', 'gender', 'language',
#                   'occupation', 'name_of_organization', 'job_position', 'website', 'linkedin_url', 'github_profile',
#                   'twitter_profile', 'instagram_profile', 'youtube_channel_url'
#                   )


# # class PasswordResetForm(forms.Form):
# #     email = forms.EmailField(label=_("Email"), max_length=254)
# #
# #     def send_mail(self, subject_template_name, email_template_name,
# #                   context, from_email, to_email, html_email_template_name=None):
# #         """
# #         Send a django.core.mail.EmailMultiAlternatives to `to_email`.
# #         """
# #         # Email subject *must not* contain newlines
# #         # body = loader.get_template(email_template_name).render(context)
# #
# #         subject = "Sikademy Password Reset"
# #         from_email = 'Sikademy Password Reset <accounts@sikademy.com>'
# #         to_email = [to_email]
# #         text_content = loader.get_template("accounts/password_reset_email.txt").render(context)
# #         html_content = loader.get_template("accounts/password_reset_email.html").render(context)
# #
# #         email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
# #         if html_email_template_name is not None:
# #             html_email = html_content
# #             email_message.attach_alternative(html_email, 'text/html')
# #
# #         email_message.send()
# #
# #     def get_users(self, email):
# #         """Given an email, return matching user(s) who should receive a reset.
# #
# #         This allows subclasses to more easily customize the default policies
# #         that prevent inactive users and users with unusable passwords from
# #         resetting their password.
# #         """
# #         active_users = User._default_manager.filter(**{
# #             '%s__iexact' % User.get_email_field_name(): email,
# #             'is_active': True,
# #         })
# #         return (u for u in active_users if u.has_usable_password())
# #
# #     def save(self, domain_override=None,
# #              subject_template_name='registration/password_reset_subject.txt',
# #              email_template_name='registration/password_reset_email.html',
# #              use_https=False, token_generator=default_token_generator,
# #              from_email=None, request=None, html_email_template_name=None,
# #              extra_email_context=None):
# #         """
# #         Generate a one-use only link for resetting password and send it to the
# #         user.
# #         """
# #         email = self.cleaned_data["email"]
# #         for user in self.get_users(email):
# #             if not domain_override:
# #                 current_site = get_current_site(request)
# #                 site_name = current_site.name
# #                 domain = current_site.domain
# #             else:
# #                 site_name = domain = domain_override
# #             context = {
# #                 'email': email,
# #                 'domain': domain,
# #                 'site_name': site_name,
# #                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
# #                 'user': user,
# #                 'token': token_generator.make_token(user),
# #                 'protocol': 'https' if use_https else 'http',
# #             }
# #             if extra_email_context is not None:
# #                 context.update(extra_email_context)
# #             self.send_mail(
# #                 subject_template_name, email_template_name, context, from_email,
# #                 email, html_email_template_name=html_email_template_name,
# #             )
