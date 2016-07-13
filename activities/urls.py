from .views import send_message_all, send_message_location
from django.conf.urls import url


urlpatterns = [
    url(r'^send/message/all/$', send_message_all, name='send_message_all'),
    url(r'^send/message/location/(?P<location_id>\d+)/$', send_message_location, name='send_message_location'),
]
