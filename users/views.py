from rest_framework import viewsets
from rest_framework.decorators import action
from .models import User
from .serializers import (
    CreateUserByAdminSerializer, UserListSerializer,
    EmailOTPVerifySerializer, SetPinSerializer,
    LoginSendSmsSerializer, LoginVerifySmsSerializer,
    UpdateSettingsSerializer, UpdateProfileSerializer,
    ForgotPinSerializer
)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import CheckPinSerializer
from .utils import send_email_otp

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('warehouse')

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateUserByAdminSerializer
        return UserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        otp = user.generate_email_otp()
        send_email_otp(user.email, otp)
        return Response(UserListSerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def send_invite(self, request, pk=None):
        user = self.get_object()
        otp = user.generate_email_otp()
        send_email_otp(user.email, otp)
        return Response({'detail': 'Invite sent'}, status=status.HTTP_200_OK)


class EmailVerifyView(generics.GenericAPIView):
    serializer_class = EmailOTPVerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.validated_data['user']

        # Foydalanuvchini aktivlashtiramiz
        user.is_active = True
        user.email_otp = None
        user.email_otp_expires = None
        user.save(update_fields=['is_active', 'email_otp', 'email_otp_expires'])

        # Token yaratamiz
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'detail': 'Email verified successfully.',
            'refresh': str(refresh),
            'access': str(access),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': getattr(user, 'role', ''),
            }
        }, status=status.HTTP_200_OK)



class SetPinView(generics.GenericAPIView):
    serializer_class = SetPinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        pin = s.validated_data['pin']
        request.user.set_pin(pin)
        return Response({'detail': 'PIN set'}, status=status.HTTP_200_OK)


class LoginSendEmailView(generics.GenericAPIView):
    serializer_class = LoginSendSmsSerializer  # yoki LoginSendEmailSerializer deb nomlasang ham bo‘ladi
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        email = s.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        otp = user.generate_login_otp()
        send_email_otp(user.email, otp)
        return Response({'detail': 'Email sent'}, status=status.HTTP_200_OK)


class CheckPinView(generics.GenericAPIView):
    def post(self, request):
        pin = request.data.get('pin')
        if not pin:
            return Response({'detail': 'Pin required'}, status=400)
        if request.user.check_pin(pin):
            return Response({'detail': 'OK'}, status=200)
        return Response({'detail': 'Invalid PIN'}, status=400)


class SettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CheckPinAPIView(APIView):
    """
    Email + PIN orqali login (token olish)
    """
    serializer_class = CheckPinSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CheckPinSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPinAPIView(generics.GenericAPIView):
    serializer_class = ForgotPinSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)
