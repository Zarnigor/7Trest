from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password
from warehouse.models import Warehouse

ROLE_CHOICES = (
    ('super_admin', 'Super Admin'),
    ('admin', 'Admin'),
    ('main_career', 'Main Career'),
    ('career', 'Career'),
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='career')
    warehouse = models.ForeignKey(Warehouse, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)  # activate after email verification
    is_staff = models.BooleanField(default=True)
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users')
    date_joined = models.DateTimeField(default=timezone.now)

    pin_hash = models.CharField(max_length=128, blank=True, null=True)

    email_otp = models.CharField(max_length=8, blank=True, null=True)
    email_otp_expires = models.DateTimeField(null=True, blank=True)

    login_otp = models.CharField(max_length=8, blank=True, null=True)
    login_otp_expires = models.DateTimeField(null=True, blank=True)

    language = models.CharField(max_length=10, default='uz')  # 'uz', 'ru', 'en'
    notifications_enabled = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def set_pin(self, raw_pin):
        self.pin_hash = make_password(raw_pin)
        self.save(update_fields=['pin_hash'])

    def check_pin(self, raw_pin):
        if not self.pin_hash:
            return False
        return check_password(raw_pin, self.pin_hash)

    def generate_email_otp(self, length=6, ttl_minutes=15):
        otp = get_random_string(length=length, allowed_chars='0123456789')
        self.email_otp = otp
        self.email_otp_expires = timezone.now() + timezone.timedelta(minutes=ttl_minutes)
        self.save(update_fields=['email_otp', 'email_otp_expires'])
        return otp

    def generate_login_otp(self, length=6, ttl_minutes=5):
        otp = get_random_string(length=length, allowed_chars='0123456789')
        self.login_otp = otp
        self.login_otp_expires = timezone.now() + timezone.timedelta(minutes=ttl_minutes)
        self.save(update_fields=['login_otp', 'login_otp_expires'])
        return otp

    def clear_otps(self):
        self.email_otp = None
        self.email_otp_expires = None
        self.login_otp = None
        self.login_otp_expires = None
        self.save(update_fields=['email_otp', 'email_otp_expires', 'login_otp', 'login_otp_expires'])
