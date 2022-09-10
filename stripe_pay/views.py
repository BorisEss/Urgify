from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import stripe

from stripe_pay.serializers import StripePaymentIntentSerializer


class StripePaymentIntentViewSet(viewsets.GenericViewSet):
    serializer_class = StripePaymentIntentSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        payment_intent_data = StripePaymentIntentSerializer(data=request.data)
        payment_intent_data.is_valid(raise_exception=True)

        no_need_on_stripe_fields = ['email', 'hospital_name', 'months', 'invoices']
        stripe_data = payment_intent_data.validated_data.copy()
        [stripe_data.pop(field) for field in no_need_on_stripe_fields]

        try:
            payment_intent = stripe.PaymentIntent.create(**stripe_data)
            payment_intent_data.save(payment_intent_id=payment_intent['id'])
        except stripe.error.StripeError as e:
            return Response({'error': e.user_message}, 400)
        return Response({'client_secret': payment_intent.client_secret}, 200)
