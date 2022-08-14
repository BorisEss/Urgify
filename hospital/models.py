from django.db import models
from autoslug import AutoSlugField

from hospital import utils


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
