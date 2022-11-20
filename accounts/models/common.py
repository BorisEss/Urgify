from django.db import models
from autoslug import AutoSlugField

from accounts.models import User, upload_img


# Temporary table for storing users waiting list
class WaitingList(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Account(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    logo = models.ImageField(upload_to=upload_img)

    def __str__(self):
        return self.name
