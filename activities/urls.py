from .views import send_message_all, send_message_location, get_messages, get_activities, get_notifications
from django.conf.urls import url


urlpatterns = [
    url(r'^send/message/all/$', send_message_all, name='send_message_all'),
    url(r'^send/message/location/(?P<location_id>\d+)/$', send_message_location, name='send_message_location'),
    url(r'^get/activity/employee/(?P<employee_id>\d+)/all/$', get_activities, name='get_activities'),
    url(r'^get/message/employee/(?P<employee_id>\d+)/all/$', get_messages, name='get_messages'),
    url(r'^get/notification/employee/(?P<employee_id>\d+)/all/$', get_notifications, name='get_notifications'),
]
