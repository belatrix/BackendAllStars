from .views import give_star_to, stars_employee_list
from .views import stars_employee_subcategory_list, stars_employee_subcategory_detail_list, stars_top_employee_lists
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<from_employee_id>\d+)/give/star/to/(?P<to_employee_id>\d+)/', give_star_to, name='give_star_to'),
    url(r'^(?P<employee_id>\d+)/list/$', stars_employee_list, name='stars_employee_list'),
    url(r'^(?P<employee_id>\d+)/subcategory/list/$', stars_employee_subcategory_list, name='stars_employee_subcategory_list'),
    url(r'^(?P<employee_id>\d+)/subcategory/(?P<subcategory_id>\d+)/list/$',
        stars_employee_subcategory_detail_list,
        name='employee_subcategory_detail_list'),
    url(r'^top/(?P<top_number>\d+)/(?P<kind>\w+)/(?P<id>\d+)/', stars_top_employee_lists, name='stars_top_employee_lists'),
]