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

]