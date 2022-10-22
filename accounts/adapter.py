import random

from allauth.account.adapter import DefaultAccountAdapter
from customerio import SendEmailRequest, CustomerIOException
from src.settings import emails_api
from src.email import CustomerIOEmail


class MyAccountAdapter(DefaultAccountAdapter):

    def generate_emailconfirmation_key(self, email):
        key = random.randint(100000, 199999)
        return key

    def send_mail(self, template_prefix, email, context):
        if 'key' not in context:
            return super().send_mail(template_prefix, email, context)

        request = SendEmailRequest(
            to=email,
            transactional_message_id=CustomerIOEmail.ConfirmAccountEmail,
            message_data={
                'confirmationKey': context['key']
            },
            identifiers={
                'email': email,
            },
        )

        try:
            emails_api.send_email(request)
        except CustomerIOException as e:
            print('Send email error: ', e)
