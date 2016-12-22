from .views import give_star_to, star, give_star_to_many, stars_employee_list
from .views import stars_top_employee_lists
from .views import stars_keyword_list, stars_keyword_list_detail
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<from_employee_id>\d+)/give/star/to/(?P<to_employee_id>\d+)/', give_star_to, name='give_star_to'),
    url(r'^(?P<from_employee_id>\d+)/give/star/to/many/$', give_star_to_many, name='give_star_to_many'),
    url(r'^(?P<star_id>\d+)/$', star, name='star_detail'),
    url(r'^(?P<employee_id>\d+)/list/$', stars_employee_list, name='stars_employee_list'),
    url(r'^keyword/list/$', stars_keyword_list, name='stars_keyword_list'),
    url(r'^keyword/(?P<keyword_id>\d+)/list/$', stars_keyword_list_detail, name='stars_keyword_list_detail'),
    url(r'^top/(?P<top_number>\d+)/(?P<kind>\w+)/(?P<id>\d+)/', stars_top_employee_lists, name='stars_top_employee_lists'),
]
