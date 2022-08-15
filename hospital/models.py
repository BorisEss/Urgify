from django.db import models
from django.utils.translation import gettext as _
from autoslug import AutoSlugField
from phone_field import PhoneField

from hospital import utils
from accounts.models import User


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hospital(Base):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    logo = models.ImageField(upload_to=utils.upload_img)


class Department(Base):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    hospital = models.ForeignKey(Hospital, related_name='departments', on_delete=models.CASCADE)


class Employee(Base):
    PENDING = 1
    ACTIVE = 2
    STATUS_CHOICES = (
        (PENDING, _('Pending')),
        (ACTIVE, _('Active')),
    )
    Finance = 1
    Patients = 2
    Editor = 3
    ATTRIBUTION_CHOICES = (
        (Finance, _('Finance')),
        (Patients, _('Patients')),
        (Finance, _('Editor')),
    )
    email = models.EmailField(max_length=50, unique=True, null=True)
    phone = PhoneField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(blank=True, null=True, choices=STATUS_CHOICES)
    attribution = models.PositiveSmallIntegerField(choices=ATTRIBUTION_CHOICES)
    department = models.ForeignKey(Department, related_name='employee', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='employee', on_delete=models.CASCADE)
