from prettyconf import config as pconfig
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


session_factory = SignedCookieSessionFactory(pconfig('COOKIE_SECRET'))


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.j2')

    config.set_session_factory(session_factory)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('auth', '/auth/')
    config.add_route('playlist.activate', '/current-playlist/')
    config.add_route('playlist.add_track', '/playlist/tracks/')
    config.add_route('search', '/search/')
    config.add_route('home', '/')

    config.scan()

    return config.make_wsgi_app()
