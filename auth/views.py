from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000/api/auth/google/login/callback/'
    client_class = OAuth2Client

    '''
        https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://localhost:8000/api/auth/google/login/callback/&prompt=consent&
        response_type=code&client_id=94023399944-bvmck2cigngkukamfpl5il469e9aaogv.apps.googleusercontent.com&
        scope=openid%20email%20profile&access_type=offline
        
        4%2F0AX4XfW
        4/0AX4XfW
    '''
