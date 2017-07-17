from prettyconf import config
import spotipy
from spotipy import oauth2


CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
REDIRECT_URI = config('REDIRECT_URI')
CACHE_FILE = config('CACHE_FILE')


class SpotifyAuthService:
    def __init__(self, scope='playlist-modify-public'):
        self.sp_oauth = oauth2.SpotifyOAuth(
            CLIENT_ID,
            CLIENT_SECRET,
            REDIRECT_URI,
            scope=scope,
            cache_path=CACHE_FILE
        )

    def get_authorize_url(self):
        return self.sp_oauth.get_authorize_url()

    def get_access_token(self):
        token_info = self._get_token_info()
        if not token_info:
            return None
        return token_info['access_token']

    def parse_response_code(self, url):
        code = self.sp_oauth.parse_response_code(url)
        if code:
            self._cache_access_token(code)
        return code

    def _cache_access_token(self, code):
        self.sp_oauth.get_access_token(code)

    def _get_token_info(self):
        return self.sp_oauth.get_cached_token()


class SpotifyService(spotipy.Spotify):
    pass
