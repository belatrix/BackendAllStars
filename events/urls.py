from .views import my_upcoming_events, local_events, other_location_events
from .views import event_detail
from django.conf.urls import url


urlpatterns = [
    url(r'^employee/(?P<employee_id>\d+)/upcoming/$', my_upcoming_events, name='my_upcoming_events'),
    url(r'^employee/(?P<employee_id>\d+)/local/$', local_events, name='local_events'),
    url(r'^employee/(?P<employee_id>\d+)/others/$', other_location_events, name='other_location_events'),
    url(r'^employee/(?P<employee_id>\d+)/event/(?P<event_id>\d+)/$', event_detail, name='event_detail'),
]
