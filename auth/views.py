from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.conf import settings


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = f'{settings.DOMAIN_NAME}api/auth/google/login/callback/'

    '''
        https://accounts.google.com/o/oauth2/v2/auth?
        redirect_uri=https://urgify.io/api/auth/google/login/callback/&prompt=consent&
        response_type=code&client_id=1088507466449-sm8rjgibbeusul17ht05n7tn422jbhbu.apps.googleusercontent.com&
        scope=openid%20email%20profile&access_type=offline
    '''
