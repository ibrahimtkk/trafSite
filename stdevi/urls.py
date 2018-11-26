from django.conf.urls import url
from .views import *

app_name = 'stdevi'

urlpatterns = [

    url(r'^$', stdevi_home, name='stdevi_home'),

    url(r'^harita/', stdevi_harita, name='stdevi_harita'),

]