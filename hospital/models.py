from django.db import models
from django.utils.translation import gettext as _
from autoslug import AutoSlugField
from phone_field import PhoneField

from hospital import utils
from accounts.utils import get_formatted_uuid


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hospital(Base):
    """
    We use CaseInsensitiveCharField because we do not want
    to be differences between test and Test names
    """
    user = models.ForeignKey('accounts.User', default=None, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    logo = models.ImageField(upload_to=utils.upload_img)

    def __str__(self):
        return self.name


class Department(Base):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    hospital = models.ForeignKey(Hospital, related_name='departments', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'hospital')

    def __str__(self):
        return self.name


class Employee(Base):
    FINANCE = 1
    PATIENTS = 2
    EDITOR = 3
    ATTRIBUTION_CHOICES = (
        (FINANCE, _('Finance')),
        (PATIENTS, _('Patients')),
        (EDITOR, _('Editor')),
    )
    ACTIVE = 1
    PENDING = 2
    PATIENT_STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (PENDING, _('Pending')),
    )
    id = models.CharField(primary_key=True, default=get_formatted_uuid, editable=False, max_length=255)
    phone = PhoneField(blank=True, null=True)
    attribution = models.PositiveSmallIntegerField(choices=ATTRIBUTION_CHOICES)
    status = models.PositiveSmallIntegerField(choices=PATIENT_STATUS_CHOICES, default=PENDING)
    department = models.ForeignKey(Department, related_name='employee', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', related_name='employee', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'department')

    def __str__(self):
        return self.user.first_name
