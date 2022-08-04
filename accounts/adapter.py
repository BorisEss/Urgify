import random

from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class MyAccountAdapter(DefaultAccountAdapter):

    def generate_emailconfirmation_key(self, email):
        key = random.randint(100000, 199999)
        return key

    def get_email_object(self, template_prefix, email, context):
        to = [email] if isinstance(email, str) else email
        from_email = self.get_from_email()
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)
        msg = EmailMessage(subject, str(context['key']), from_email, to)
        return msg

    def send_mail(self, template_prefix, email, context):
        if 'key' not in context:
            return super().send_mail(template_prefix, email, context)
        msg = self.get_email_object(template_prefix, email, context)
        msg.send()
