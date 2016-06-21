from .views import event, event_list, participant
from django.conf.urls import url


urlpatterns = [
    url(r'^list/$', event_list, name='event_list'),
    url(r'^(?P<event_id>\d+)/$', event, name='event_detail'),
    url(r'^participant/(?P<participant_id>\d+)/$', participant, name='participant_detail'),
]
