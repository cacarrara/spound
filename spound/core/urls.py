from django.urls import path
from django.views.generic import TemplateView

from core import views


urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('signin/', views.signin_view, name='signin'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
