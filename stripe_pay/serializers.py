from rest_framework import serializers
from stripe_pay import models


class StripePaymentIntentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    hospital_name = serializers.CharField(max_length=255)
    amount = serializers.IntegerField(min_value=0)
    currency = serializers.ChoiceField(choices=('usd',))
    payment_method_types = serializers.ChoiceField(choices=('card',))

    def validate_payment_method_types(self, value):
        return [value]

    def validate_email(self, value):
        if models.PreOrderPayment.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_hospital_name(self, value):
        if models.PreOrderPayment.objects.filter(email=value).exists():
            raise serializers.ValidationError('Hospital with this name already exists')
        return value

    def validate_amount(self, value):
        """ Needs to make time 100 because stripe 1$ from front is 0.01 for stripe"""
        return value * 100
