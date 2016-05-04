from .views import employee, employee_categories, employee_list, employee_avatar, employee_creation
from .views import employee_location_list, employee_role_list
from .views import CustomObtainAuthToken, search, top
from django.conf.urls import url


urlpatterns = [
    url(r'^authenticate/', CustomObtainAuthToken.as_view()),
    url(r'^create/$', employee_creation, name='employee_creation'),
    url(r'^list/$', employee_list, name='employee_list'),
    url(r'^list/top/(?P<kind>\w+)/(?P<quantity>\d+)/$', top, name='employee_list_top'),
    url(r'^location/list/$', employee_location_list, name='employee_location_list'),
    url(r'^role/list/$', employee_role_list, name='employee_role_list'),
    url(r'^(?P<employee_id>\d+)/$', employee, name='employee_detail'),
    url(r'^(?P<employee_id>\d+)/avatar/$', employee_avatar, name='employee_avatar'),
    url(r'^(?P<employee_id>\d+)/category/list/$', employee_categories, name='employee_category_list'),
    url(r'^search/(?P<search_term>\w+)/', search, name='employee_search'),
]
