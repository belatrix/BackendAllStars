from .views import employee, employee_categories, employee_list, employee_avatar
from .views import employee_creation, employee_activate, employee_deactivate, employee_update, employee_update_password
from .views import employee_deactivated_list, employee_location_list, employee_role_list
from .views import CustomObtainAuthToken, search, top
from django.conf.urls import url


urlpatterns = [
    url(r'^authenticate/', CustomObtainAuthToken.as_view()),
    url(r'^create/$', employee_creation, name='employee_creation'),
    url(r'^list/$', employee_list, name='employee_list'),
    url(r'^list/deactivated/$', employee_deactivated_list, name='employee_deactivated_list'),
    url(r'^list/top/(?P<kind>\w+)/(?P<quantity>\d+)/$', top, name='employee_list_top'),
    url(r'^location/list/$', employee_location_list, name='employee_location_list'),
    url(r'^role/list/$', employee_role_list, name='employee_role_list'),
    url(r'^(?P<employee_id>\d+)/$', employee, name='employee_detail'),
    url(r'^(?P<employee_id>\d+)/activate/$', employee_activate, name='employee_activate'),
    url(r'^(?P<employee_id>\d+)/avatar/$', employee_avatar, name='employee_avatar'),
    url(r'^(?P<employee_id>\d+)/category/list/$', employee_categories, name='employee_category_list'),
    url(r'^(?P<employee_id>\d+)/deactivate/$', employee_deactivate, name='employee_deactivate'),
    url(r'^(?P<employee_id>\d+)/update/$', employee_update, name='employee_update'),
    url(r'^(?P<employee_id>\d+)/update/password/$', employee_update_password, name='employee_update_password'),
    url(r'^search/(?P<search_term>\w+)/', search, name='employee_search'),
]
