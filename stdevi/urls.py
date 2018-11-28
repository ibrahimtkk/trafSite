from django.conf.urls import url

from home.views import *
from .views import *

app_name = 'stdevi'

urlpatterns = [

    url(r'^$', stdevi_home, name='stdevi_home'),

    url(r'^harita/', home_to_stdevi, name='stdevi_harita'),

]