from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account.views import ConfirmEmailView as _ConfirmEmailView
from allauth.utils import email_address_exists
from rest_framework import serializers


class ConfirmEmailView(_ConfirmEmailView):
    template_name = 'accounts/confirm_email.txt'


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                "A user is already registered with this e-mail address.")
        return email

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user