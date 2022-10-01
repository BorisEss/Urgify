from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PreOrderPayment(Base):
    USD = 'usd'
    CURRENCY_CHOICES = (
        (USD, 'usd'),
    )
    CARD = 'card'
    PAYMENT_TYPE_CHOICES = (
        (CARD, 'card'),
    )
    amount = models.PositiveSmallIntegerField()
    invoices = models.PositiveSmallIntegerField()
    months = models.PositiveSmallIntegerField()
    email = models.EmailField(unique=True)
    payment_intent_id = models.CharField(max_length=255)
    hospital_name = models.CharField(max_length=255, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=USD)
    payment_method_types = models.CharField(max_length=4, choices=PAYMENT_TYPE_CHOICES, default=CARD)
