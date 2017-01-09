from .views import my_upcoming_events, local_events
from django.conf.urls import url


urlpatterns = [
    url(r'^employee/(?P<employee_id>\d+)/upcoming/', my_upcoming_events, name='my_upcoming_events'),
    url(r'^employee/(?P<employee_id>\d+)/local/', local_events, name='local_events'),
]
