from rest_framework import serializers


class StripePaymentIntentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=0)
    currency = serializers.CharField()
    payment_method_types = serializers.ListField()
