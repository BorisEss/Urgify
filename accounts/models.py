from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from accounts.utils import get_formatted_uuid
import hospital.models


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError(_('User must have an email'))
        if not password:
            raise ValueError(_('User must have a password'))

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
    Pending = 1
    ACCEPTED = 2
    EXPIRED = 3
    STATUS = (
        (Pending, _('Pending')),
        (ACCEPTED, _('Accepted')),
        (EXPIRED, _('Expired')),
    )
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=Pending)
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(
        hospital.models.Department,
        null=True,
        on_delete=models.CASCADE,
        related_name='invitees'
    )

    def get_invite_hash(self) -> str:
        return settings.HASHER.encode(self.pk)

    @staticmethod
    def get_invite_object_from_hash(invite_hash: settings.HASHER):
        return get_object_or_404(MemberInvite, pk=settings.HASHER.decode(invite_hash)[0])
