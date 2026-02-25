from django.urls import path
from .views import RewardProfileView, RewardHistoryView, LeaderboardView

urlpatterns = [
    path('me/', RewardProfileView.as_view(), name='my-reward'),
    path('history/', RewardHistoryView.as_view(), name='reward-history'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]