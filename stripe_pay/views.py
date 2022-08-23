from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import stripe

from stripe_pay.serializers import StripePaymentIntentSerializer


class StripePaymentIntentViewSet(viewsets.GenericViewSet):
    serializer_class = StripePaymentIntentSerializer

    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        payment_intent_data = StripePaymentIntentSerializer(data=request.data)
        payment_intent_data.is_valid(raise_exception=True)

        try:
            payment_intent = stripe.PaymentIntent.create(**payment_intent_data.validated_data)
        except stripe.error.StripeError as e:
            return Response({'error': e.user_message}, 400)
        return Response({'client_secret': payment_intent.client_secret}, 200)
