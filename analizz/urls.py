from django.conf.urls import url
from .views import *

app_name = 'analizz'

urlpatterns = [

    url(r'^$', analiz_home, name='analiz_home'),

    url(r'^grafikler/', analiz_grafikler, name='analiz_grafikler'),

]