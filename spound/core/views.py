from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.services import SpotifyAuthService, SpotifyService


class SignInView(TemplateView):
    template_name = 'signin.html'

    def get(self, request, *args, **kwargs):
        self.auth_service = SpotifyAuthService()
        self.code = self.auth_service.parse_response_code(request.get_full_path())
        if self.code:
            return redirect(reverse('core:home'))

        return super().get(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        if not self.code:
            context['auth_url'] = self.auth_service.get_authorize_url()
        return context


signin_view = SignInView.as_view()


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        auth_service = SpotifyAuthService()
        access_token = auth_service.get_access_token()

        if not access_token:
            return redirect(reverse('core:signin'))

        spotify_service = SpotifyService(access_token)
        self.user = spotify_service.current_user()
        self.playlists = spotify_service.current_user_playlists()

        return super().get(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['user'] = self.user,
        context['playlists'] = self.playlists['items'],

        return context


home_view = HomeView.as_view()
