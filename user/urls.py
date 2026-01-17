from django.contrib import admin
from django.urls import path,include
from .views import UserRegistrationApiView, VerifyOTPApiView,LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserRegistrationApiView.as_view(),name = 'register'),
    path('OTP/verify/',VerifyOTPApiView.as_view(),name = 'otp'),
    path("login/", LoginAPIView.as_view(), name="jwt-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]