from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response
from Reward.models import RewardProfile,RewardHistory
from .serializers import RewardHistoryserializers,RewardProfileserializers
from rest_framework import status

class RewardProfileView(APIView):
    def get(self, request):
        user = request.user
        reward, created = RewardProfile.objects.get_or_create(user=user)
        serializer = RewardProfileserializers(reward)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RewardHistoryView(APIView):
    def get(self, request):
        user = request.user
        history = RewardHistory.objects.filter(user=user).order_by('-created_at')
        serializer = RewardHistoryserializers(history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaderboardView(APIView):
    def get(self, request):
        top_users = RewardProfile.objects.select_related('user').order_by('-points')[:10]

        data = []
        rank = 1

        for profile in top_users:
            data.append({
                "rank": rank,
                "user_id": profile.user.id,
                "email": profile.user.email,
                "points": profile.points,
                "badge": profile.badge,
                "level": profile.level,
            })
            rank += 1

        return Response(data, status=status.HTTP_200_OK)
