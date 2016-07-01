from .views import event, event_list, participant, participant_list, participant_create
from .views import event_register_collaborator, event_unregister_collaborator
from .views import event_register_participant, event_unregister_participant
from django.conf.urls import url


urlpatterns = [
    url(r'^list/$', event_list, name='event_list'),
    url(r'^(?P<event_id>\d+)/$', event, name='event_detail'),
    url(r'^(?P<event_id>\d+)/register/collaborator/(?P<employee_id>\d+)/$', event_register_collaborator, name='event_register_collaborator'),
    url(r'^(?P<event_id>\d+)/register/participant/(?P<participant_id>\d+)/$', event_register_participant, name='event_register_participant'),
    url(r'^(?P<event_id>\d+)/unregister/collaborator/(?P<employee_id>\d+)/$', event_unregister_collaborator, name='event_unregister_collaborator'),
    url(r'^(?P<event_id>\d+)/unregister/participant/(?P<participant_id>\d+)/$', event_unregister_participant, name='event_unregister_participant'),
    url(r'^participant/(?P<participant_id>\d+)/$', participant, name='participant_detail'),
    url(r'^participant/$', participant_create, name='participant_create'),
    url(r'^participant/list/$', participant_list, name='participant_list'),
]
