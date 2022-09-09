from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import stripe

from stripe_pay.serializers import StripePaymentIntentSerializer
from stripe_pay import models


class StripePaymentIntentViewSet(viewsets.GenericViewSet):
    serializer_class = StripePaymentIntentSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        payment_intent = StripePaymentIntentSerializer(data=request.data)
        payment_intent.is_valid(raise_exception=True)

        hospital_name = payment_intent.validated_data.pop('hospital_name')
        email = payment_intent.validated_data.pop('email')

        try:
            payment_intent = stripe.PaymentIntent.create(**payment_intent.validated_data)
            models.PreOrderPayment.objects.create(
                payment_intent_id=payment_intent['id'],
                hospital_name=hospital_name,
                email=email,
            )
        except stripe.error.StripeError as e:
            return Response({'error': e.user_message}, 400)
        return Response({'client_secret': payment_intent}, 200)
