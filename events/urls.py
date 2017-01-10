from .views import my_upcoming_events, local_events, other_location_events
from .views import event_detail, employee_event_registration
from django.conf.urls import url


urlpatterns = [
    url(r'^upcoming/employee/(?P<employee_id>\d+)/$', my_upcoming_events, name='my_upcoming_events'),
    url(r'^local/employee/(?P<employee_id>\d+)/$', local_events, name='local_events'),
    url(r'^others/employee/(?P<employee_id>\d+)/$', other_location_events, name='other_location_events'),
    url(r'^(?P<event_id>\d+)/employee/(?P<employee_id>\d+)/$', event_detail, name='event_detail'),
    url(r'^(?P<event_id>\d+)/employee/(?P<employee_id>\d+)/registration/(?P<action>\w+)/$',
        employee_event_registration,
        name='employee_event_registration'),
]
