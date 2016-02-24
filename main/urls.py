from django.conf.urls import url
from django.contrib.auth.views import logout
from main.views import *


urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^image/$', ImageProcessing.as_view(), name='image'),
    url(r'^effects/', Effects.as_view(), name='effects'),
    url(r'^accounts/logout/$', logout,
        {'next_page': '/accounts/login/'}, name="logout"),
    url(r'^image/(?P<id>[0-9]+)/delete/$',
        DeleteImage.as_view(), name='delete'),
    url(r'^save-effects/', SaveProcessedImage.as_view(), name='save_effects'),


]
