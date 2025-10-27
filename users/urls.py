from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserViewSet,
    EmailVerifyView, SetPinView,
    LoginSendEmailView, CheckPinAPIView,
    ForgotPinAPIView
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/email-verify-token/', EmailVerifyView.as_view(), name='email-verify'),
    path('auth/set-pin/', SetPinView.as_view(), name='set-pin'),
    path('auth/login-send-sms/', LoginSendEmailView.as_view(), name='login-send-sms'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/check-pin/', CheckPinAPIView.as_view(), name='check-pin'),
    path('auth/forgot-pin/', ForgotPinAPIView.as_view(), name='forgot-pin'),
]
