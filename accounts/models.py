from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.shortcuts import get_object_or_404

from accounts.utils import get_formatted_uuid


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    id = models.CharField(primary_key=True, default=get_formatted_uuid, editable=False, max_length=255)
    email = models.EmailField(max_length=50, unique=True, null=True)
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # in this keys email and password are prompted by default

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'auth_user'


# Temporary table for storing users waiting list
class WaitingList(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MemberInvite(models.Model):
    INVITED = 1
    ACCEPTED = 2
    EXPIRED = 3
    DECLINED = 4
    STATUS = (
        (INVITED, 'Invited'),
        (ACCEPTED, 'Accepted'),
        (EXPIRED, 'Expired'),
        (DECLINED, 'Declined'),
    )
    invitee = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    status = models.PositiveSmallIntegerField(choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_invite_url(self, uri: str) -> str:
        invite_hash = settings.HASHER.encode(self.pk)
        return f'{uri}accept-invite/{invite_hash}/'

    @staticmethod
    def get_invite_object_from_hash(invite_hash: settings.HASHER):
        return get_object_or_404(MemberInvite, pk=settings.HASHER.decode(invite_hash)[0])
