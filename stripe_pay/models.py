from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PreOrderPayment(Base):
    payment_intent_id = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    hospital_name = models.CharField(max_length=255, unique=True)
