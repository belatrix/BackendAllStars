from .views import my_upcoming_events
from django.conf.urls import url


urlpatterns = [
    url(r'^employee/(?P<employee_id>\d+)/upcoming/', my_upcoming_events, name='my_upcoming_events'),
]
