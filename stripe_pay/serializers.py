from rest_framework import serializers


class StripePaymentIntentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=0)
    currency = serializers.ChoiceField(choices=('usd',))
    payment_method_types = serializers.ChoiceField(choices=('card',))

    def validate_payment_method_types(self, value):
        return [value]
