from .views import give_star_to, stars_employee_subcategory_list
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<from_employee_id>\d+)/give/star/to/(?P<to_employee_id>\d+)/', give_star_to, name='give_star_to'),
    url(r'^(?P<employee_id>\d+)/subcategory/list/$', stars_employee_subcategory_list, name='stars_employee_subcategory_list'),
]