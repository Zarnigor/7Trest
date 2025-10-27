from .models import Warehouse
from django.contrib.auth.password_validation import validate_password
from warehouse.serializer import WarehouseSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.utils import timezone
from users.models import User


class CreateUserByAdminSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'warehouse']

    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user
        user = User.objects.create(**validated_data)
        user.is_active = False
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'role', 'warehouse', 'is_active', 'language', 'notifications_enabled']

class EmailOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'User not found.'})

        if not user.login_otp or user.login_otp != otp:
            print(user.login_otp, otp)
            raise serializers.ValidationError({'otp': 'Invalid OTP code.'})

        if user.login_otp_expires and timezone.now() > user.login_otp_expires:
            raise serializers.ValidationError({'otp': 'OTP code expired.'})

        attrs['user'] = user
        return attrs

class SetPinSerializer(serializers.Serializer):
    pin = serializers.CharField(min_length=4, max_length=8)

class LoginSendSmsSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginVerifySmsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=8)


class UpdateSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['language', 'notifications_enabled']


class UpdateProfileSerializer(serializers.ModelSerializer):
    pin_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'pin_code']

    def validate_password(self, value):
        if value:
            validate_password(value)
        return value

    def update(self, instance, validated_data):
        pwd = validated_data.pop('pin_code', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if pwd:
            instance.set_password(pwd)
        instance.save()
        return instance

User = get_user_model()

class CheckPinSerializer(serializers.Serializer):
    email = serializers.EmailField()
    pin_code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        pin_code = attrs.get("pin_code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Bunday email bilan foydalanuvchi topilmadi.")

        if not user.pin_hash:
            raise serializers.ValidationError("Foydalanuvchi uchun PIN kod o‘rnatilmagan.")

        if not check_password(pin_code, user.pin_hash):
            raise serializers.ValidationError("PIN kod noto‘g‘ri.")

        refresh = RefreshToken.for_user(user)

        return {
            "user_id": user.id,
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

from .utils import send_email_otp

class ForgotPinSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email bilan foydalanuvchi topilmadi.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)
        otp = user.generate_email_otp()
        send_email_otp(to_email=user.email, otp=otp)

        return {"detail": "Tasdiqlov kodi emailingizga yuborildi."}
