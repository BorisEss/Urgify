from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import (
    RegisterView, VerifyEmailView,
    ResendEmailVerificationView, ConfirmEmailView
)
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, UserDetailsView, PasswordResetConfirmView
)

from .views import GoogleLogin

urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),

    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-change/', PasswordChangeView.as_view(), name='rest_password_change'),

    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),

    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),

    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),

    path('google/login/callback/', GoogleLogin.as_view(), name='google_login'),
]
