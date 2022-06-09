from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_ulid.models import default, ULIDField


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
    id = ULIDField(primary_key=True, unique=True, editable=False,  default=default)
    email = models.EmailField(max_length=50, unique=True, null=True)
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # in this keys email and password are prompted by default

    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'
