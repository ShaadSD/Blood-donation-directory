from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .models import EmergencyRequest, UserProfile, DonationHistory
from .serializers import EmergencyRequestserializers, UserProfileserializers, DonationHistoryserializers
from rest_framework.permissions import IsAuthenticated
from Reward.models import RewardHistory, RewardProfile
from datetime import timedelta
from django.utils import timezone



class UserProfileView(APIView):

    def post(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


        serializer = UserProfileserializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            reward, created = RewardProfile.objects.get_or_create(user=user)

            reward.points+=10
            reward.save()

            RewardHistory.objects.create(
                user=user,
                action="Profile Complete",
                points=10
            )
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        try:
            profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileserializers(profile)
        return Response(serializer.data, status=200)


    def put(self, request):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileserializers(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)




class DonorSearchView(APIView):
    def get(self, request):
        blood_group = request.query_params.get('blood_group')
        district = request.query_params.get('district')
        is_available = request.query_params.get('is_available')

        donors = UserProfile.objects.all()

        if blood_group:
            donors = donors.filter(blood_group=blood_group)
        if district:
            donors = donors.filter(district=district)
        if is_available:
            donors = donors.filter(is_available=is_available)


        serializer = UserProfileserializers(donors, many=True)
        return Response(serializer.data)



class EmergencyRequestView(APIView):

    def post(self, request):
        user_id = request.query_params.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


        serializer = EmergencyRequestserializers(data=request.data)
        if serializer.is_valid():
            serializer.save(requester=user, status='Open')
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        requests = EmergencyRequest.objects.all().order_by('-created_at')
        serializer = EmergencyRequestserializers(requests, many=True)
        return Response(serializer.data)



class AcceptEmergencyRequestView(APIView):
    def post(self, request, request_id):
        user = request.user

        try:
            profile = UserProfile.objects.get(user=user)
            emergency = EmergencyRequest.objects.get(id=request_id)
        except:
            return Response({"error": "Not found"}, status=404)

        if emergency.status != 'Open':
            return Response({"error": "Request already assigned"}, status=400)

        emergency.assigned_donor = user
        emergency.status = 'assigned'
        emergency.save()


        reward, created = RewardProfile.objects.get_or_create(user=user)
        reward.points += 20
        reward.save()

        RewardHistory.objects.create(
            user=user,
            action="Emergency Accept",
            points=20
        )

        return Response({"message": "Request accepted successfully"})



class DonationHistoryView(APIView):

    def post(self, request):
        serializer = DonationHistoryserializers(data=request.data)
        if serializer.is_valid():

            donation = serializer.save()

            
            donation.next_eligible_date = donation.donation_date + timedelta(days=90)
            donation.save()

            user = donation.donor

            reward, created = RewardProfile.objects.get_or_create(user=user)

           
            reward.points += 50

            donation_count = DonationHistory.objects.filter(donor=user).count()

   
            if donation_count == 1:
                reward.points += 100
                RewardHistory.objects.create(
                    user=user,
                    action="First Donation Bonus",
                    points=100
                )

        
            if donation_count >= 20:
                reward.badge = "Hero Donor"
            elif donation_count >= 10:
                reward.badge = "Gold Donor"
            elif donation_count >= 5:
                reward.badge = "Silver Donor"
            elif donation_count >= 1:
                reward.badge = "Bronze Donor"

       
            if reward.points >= 600:
                reward.level = "Super Donor"
            elif reward.points >= 300:
                reward.level = "Level 3"
            elif reward.points >= 100:
                reward.level = "Level 2"
            else:
                reward.level = "Level 1"

            reward.save()

   
            RewardHistory.objects.create(
                user=user,
                action="Blood Donation",
                points=50
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        history = DonationHistory.objects.filter(donor=user)
        serializer = DonationHistoryserializers(history, many=True)
        return Response(serializer.data)