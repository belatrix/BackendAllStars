from .views import send_message_all, send_message_to, send_message_location
from .views import get_activities, get_messages, get_messages_from, get_notifications
from django.conf.urls import url


urlpatterns = [
    url(r'^send/message/all/$', send_message_all, name='send_message_all'),
    url(r'^send/message/to/(?P<employee_username>\w+)/$', send_message_to, name='send_message_to'),
    url(r'^send/message/location/(?P<location_id>\d+)/$', send_message_location, name='send_message_location'),
    url(r'^get/activity/employee/(?P<employee_id>\d+)/all/$', get_activities, name='get_activities'),
    url(r'^get/message/employee/(?P<employee_id>\d+)/all/$', get_messages, name='get_messages'),
    url(r'^get/message/from/employee/(?P<employee_id>\d+)/all/$', get_messages_from, name='get_messages_from'),
    url(r'^get/notification/employee/(?P<employee_id>\d+)/all/$', get_notifications, name='get_notifications'),
]
