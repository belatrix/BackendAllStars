from .views import event, event_list, participant, participant_list
from django.conf.urls import url


urlpatterns = [
    url(r'^list/$', event_list, name='event_list'),
    url(r'^(?P<event_id>\d+)/$', event, name='event_detail'),
    url(r'^participant/(?P<participant_id>\d+)/$', participant, name='participant_detail'),
    url(r'^participant/list/$', participant_list, name='participant_list'),
]
