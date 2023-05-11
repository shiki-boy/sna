from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from apps.user.views import (
    UserInfoView, SnaRegisterView, SnaVerifyEmailView
)

router = DefaultRouter()
# router.register('profile', UserProfileViewset)
urlpatterns = router.urls

app_name = 'apps.auth'

urlpatterns += [
    path(f"", include("dj_rest_auth.urls")),

    path('register/', SnaRegisterView.as_view(), name='register'),

    re_path(r'registration/account-confirm-email/(?P<key>[-:\w]+)',
            SnaVerifyEmailView.as_view(), name='account_confirm_email'),

    path('user-info/', UserInfoView.as_view(), name='user-info'),
]
