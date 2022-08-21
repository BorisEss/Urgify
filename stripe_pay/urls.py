from django.urls import path

from stripe_pay.views import StripePaymentIntentViewSet

urlpatterns = [
    path('create-payment-intent/', StripePaymentIntentViewSet.as_view({'post': 'create_payment_intent'}))
]
