"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from apps.user.views import SnaVerifyEmailView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include(("apps.user.urls", "user"), namespace="auth-api")),
    path("api/friend/", include(("apps.friend.urls", "friend"), namespace="friend-api")),

    re_path(
        r"api/auth/registration/account-confirm-email/",
        SnaVerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^change-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$",
        TemplateView.as_view(template_name="index.html"),
        name="password_reset_confirm",
    ),

    # catch all the rest
    # re_path(r"^.*$", TemplateView.as_view(template_name="index.html")),
]
