import logging

import pyramid.httpexceptions as exc
from pyramid.view import view_config

from spound.services import SpotifyAuthService, SpotifyService


logger = logging.getLogger(__name__)


@view_config(route_name='auth', renderer='auth.j2')
def auth(request):
    auth_service = SpotifyAuthService()
    code = auth_service.parse_response_code(request.url)
    if not code:
        return {'auth_url': auth_service.get_authorize_url()}
    return exc.HTTPFound(request.route_url('home'))


@view_config(route_name='home', renderer='home.j2')
def home(request):
    auth_service = SpotifyAuthService()
    access_token = auth_service.get_access_token()

    if not access_token:
        return exc.HTTPFound(request.route_url('auth'))

    spotify_service = SpotifyService(access_token)
    user = spotify_service.current_user()
    playlists = spotify_service.current_user_playlists()
    logger.debug(user)
    logger.debug(playlists)
    return {
        'user': user,
        'playlists': playlists['items'],
    }


@view_config(route_name='search', renderer='search.j2')
def search(request):
    auth_service = SpotifyAuthService()
    spotify_service = SpotifyService(auth_service.get_access_token())
    results = spotify_service.search(request.GET.get('q'), market='BR')
    logger.debug(results)
    return {'tracks': results['tracks']['items']}


@view_config(route_name='playlist.activate')
def playlist_activate(request):
    request.session['current_playlist_id'] = request.POST.get('playlist_id')
    return exc.HTTPFound(request.route_url('home'))


@view_config(route_name='playlist.add_track')
def add_track_to_playlist(request):
    auth_service = SpotifyAuthService()
    spotify_service = SpotifyService(auth_service.get_access_token())
    current_playlist_id = request.session['current_playlist_id']
    current_user_id = spotify_service.current_user()['id']
    track_id = request.POST.get('track_id')
    spotify_service.user_playlist_add_tracks(current_user_id, current_playlist_id, [track_id])
    return exc.HTTPFound(request.route_url('home'))
