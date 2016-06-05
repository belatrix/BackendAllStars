from .views import event, event_list
from django.conf.urls import url


urlpatterns = [
    url(r'^list/$', event_list, name='event_list'),
]
