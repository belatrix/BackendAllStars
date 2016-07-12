from .views import send_message_all
from django.conf.urls import url


urlpatterns = [
    url(r'^send/message/all/$', send_message_all, name='send_message_all'),
]
