from allauth.account.views import ConfirmEmailView as _ConfirmEmailView


class ConfirmEmailView(_ConfirmEmailView):
    template_name = 'accounts/confirm_email.txt'