from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        if not user.is_active:
            raise serializers.ValidationError("Account is not active")

        if not user.is_verified:
            raise serializers.ValidationError("Account not verified")

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
        return data



    
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data['is_active'] = False
        return User.objects.create_user(**validated_data)
    

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         email = data.get("email")
#         password = data.get("password")

#         user = authenticate(email=email, password=password)

#         if not user:
#             raise serializers.ValidationError("Invalid email or password")

#         if not user.is_active:
#             raise serializers.ValidationError("Account is not active")

#         if not user.is_verified:
#             raise serializers.ValidationError("Email not verified")

#         data["user"] = user
#         return data
    




class OTPVerifySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp_code = serializers.CharField(max_length=6)



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)