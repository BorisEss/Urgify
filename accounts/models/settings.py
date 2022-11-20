import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _


def get_formatted_uuid() -> str:
    """
    It generates a random UUID and returns it in uppercase hexadecimal format
    return: A random string of hexadecimal characters.
    """
    return uuid.uuid4().hex.upper()


def upload_img(instance, filename):
    random_string = get_random_string(6)
    ext = filename.split('.')[-1]
    class_name = instance.__class__.__name__
    return f'{class_name}/{instance.slug}/{random_string}.{ext}'


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
