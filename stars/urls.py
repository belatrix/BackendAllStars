from .views import give_star_to
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<from_employee_id>\d+)/give/star/to/(?P<to_employee_id>\d+)/', give_star_to, name='give_star_to'),
]