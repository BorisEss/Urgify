from rest_framework import serializers
from stripe_pay import models


class StripePaymentIntentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PreOrderPayment
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at', 'payment_intent_id')

    def create(self, validated_data):
        return models.PreOrderPayment.objects.create(**validated_data)

    def validate_payment_method_types(self, value):
        return [value]

    def validate_amount(self, value):
        """ Needs to make time 100 because stripe 1$ from front is 0.01 for stripe"""
        return value * 100
