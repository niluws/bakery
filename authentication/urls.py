from django.urls import path

from .views import (
    ActiveAccountAPIView,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    RefreshTokenAPIView,
    RegisterAPIView,
    VerifyEmailAPIView,
    LogAPIView,
)

app_name = 'authentication'

urlpatterns = [
    path('activate/<str:otp_code>/', ActiveAccountAPIView.as_view(), name='otp_code'),
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify_email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('logs/', LogAPIView.as_view(), name='logs'),
]
