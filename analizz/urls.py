"""from django.conf.urls import url
from .views import *
from home.views import *
import home

app_name = 'analizz'

urlpatterns = [

    url(r'^', home.views.home_to_aylikHiz, name='analiz_home'),

    #url(r'^grafikler/', analiz_grafikler, name='analiz_grafikler'),


    # urlsi analiz/grafikler olan sayfa icin home_to_tumGun fonku calistir.
    url(r'^grafikler/', home.views.home_to_tumGun, name='analiz_grafikler'),

    url(r'^renkliHarita/', home.views.home_to_renkliHarita, name='analiz_renkliHarita'),

    url(r'^aylikGrafik/', home.views.home_to_aylikHiz, name='analiz_aylikHiz'),

    url(r'^havaDurumuEtkisi/', home.views.home_to_havaDurumu, name='analiz_havaDurumu'),

]
"""

from django.conf.urls import url
from .views import *
from home.views import *

app_name = 'analizz'

urlpatterns = [

    url(r'^$', analiz_home, name='analiz_home'),

    #url(r'^grafikler/', analiz_grafikler, name='analiz_grafikler'),


    # urlsi analiz/grafikler olan sayfa icin home_to_tumGun fonku calistir.
    url(r'^grafikler/', home_to_tumGun, name='analiz_grafikler'),

    url(r'^renkliHarita/', home_to_renkliHarita, name='analiz_renkliHarita'),

    url(r'^aylikGrafik/', home_to_aylikHiz, name='analiz_aylikHiz'),

    url(r'^havaDurumuEtkisi/', home_to_havaDurumu, name='analiz_havaDurumu'),

    url(r'^djangoyaGonder/', djangoyaGonder, name='analiz_djangoyaGonder'),

    url(r'^djangodanAl/', djangodanAl, name='analiz_djangodanAl'),


]