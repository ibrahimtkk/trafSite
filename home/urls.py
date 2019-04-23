"""from django.conf.urls import url
from .views import *
import home

app_name = 'home'

urlpatterns = [

    url(r'^$', home_view, name='home_view'),

    #url(r'^', home_to_aylikHiz, name='home_to_aylikHiz'),

    #url(r'/analizz/renkliHarita/', home.views.home_to_aylikHiz, name='home_to_aylikHiz'),
#
    #url(r'^grafikler/', home.views.home_to_tumGun, name='analiz_grafikler'),
#
    #url(r'^renkliHarita/', home.views.home_to_renkliHarita, name='analiz_renkliHarita'),
#
    #url(r'^aylikGrafik/', home.views.home_to_aylikHiz, name='analiz_aylikHiz'),
#
    #url(r'^havaDurumuEtkisi/', home.views.home_to_havaDurumu, name='analiz_havaDurumu'),
#
    #url(r'^stdevi/harita', home.views.home_to_stdevi, name='home_to_stdevi'),

]
"""

from django.conf.urls import url
from .views import *

app_name = 'home'

urlpatterns = [

    url(r'^$', home_view, name='home_view'),

    url(r'^stdevi/harita', home_to_stdevi, name='home_to_stdevi'),

]