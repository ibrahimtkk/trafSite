from django.conf.urls import url
from .views import *

app_name = 'tahmin'

urlpatterns = [

    url(r'^$', tahmin_home, name='tahmin_home'),

]