from django.urls import path
from .views import (
UserProfileView,
DonorSearchView,
EmergencyRequestView,
AcceptEmergencyRequestView,
DonationHistoryView
)


urlpatterns = [
    path('profile/', UserProfileView.as_view()),
    path('donors/search/', DonorSearchView.as_view()),
    path('emergency/', EmergencyRequestView.as_view()),
    path('emergency/<int:request_id>/accept/', AcceptEmergencyRequestView.as_view()),
    path('donation-history/', DonationHistoryView.as_view()),
]