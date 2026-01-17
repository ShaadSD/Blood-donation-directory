from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer,OTPVerifySerializer
from .utils import generate_otp
from .models import OTPVerification
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.is_verified = False
            user.save()

            otp = generate_otp()

            OTPVerification.objects.create(
                user=user,
                otp_code=otp
            )

            email = EmailMultiAlternatives(
                subject="Your OTP Code",
                body=f"Your OTP is {otp}",
                to=[user.email],
            )
            email.send()

            return Response({
                "message": "OTP sent to your email",
                "user_id": user.id
            })

        return Response(serializer.errors, status=400)
    



class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class VerifyOTPApiView(APIView):

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            otp = OTPVerification.objects.filter(
                user_id=user_id,
                otp_code=otp_code,
                is_used=False
            ).latest("created_at")
        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=400)

        if timezone.now() > otp.created_at + timedelta(minutes=5):
            return Response({"error": "OTP expired"}, status=400)

        user = otp.user
        user.is_active = True
        user.is_verified = True
        user.save()

        otp.is_used = True
        otp.save()

        return Response({"message": "Account verified successfully"})
    






