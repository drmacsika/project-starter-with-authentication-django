from allauth.account.views import (EmailVerificationSentView, LoginView,
                                   LogoutView, SignupView)
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('', include('accounts.urls', namespace='accounts'),),
    path('accounts/', include('allauth.urls'),),
]
