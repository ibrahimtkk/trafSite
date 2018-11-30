from django.conf.urls import url
from .views import *

app_name = 'home'

urlpatterns = [

    url(r'^', home_view, name='home_view'),

    url(r'^stdevi/harita', home_to_stdevi, name='home_to_stdevi'),

]