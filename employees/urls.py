from .views import employee, employee_list
from .views import employee_creation, employee_update, employee_update_password
from .views import employee_location_list, employee_role_list, employee_image, employee_position_list
from .views import employee_reset_password, employee_reset_password_confirmation, employee_register_device
from .views import CustomObtainAuthToken, top, employee_logout
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^authenticate/', CustomObtainAuthToken.as_view()),
    url(r'^create/$', employee_creation, name='employee_creation'),
    url(r'^list/$', employee_list, name='employee_list'),
    url(r'^list/top/(?P<quantity>\d+)/(?P<kind>\w+)/$', top, name='employee_list_top'),
    url(r'^logout/$', employee_logout, name='employee_logout'),
    url(r'^location/list/$', employee_location_list, name='employee_location_list'),
    url(r'^position/list/$', employee_position_list, name='employee_position_list'),
    url(r'^role/list/$', employee_role_list, name='employee_role_list'),
    url(r'^reset/password/(?P<employee_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', employee_reset_password, name='employee_reset_password'),
    url(r'^reset/password/(?P<employee_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<employee_uuid>[0-9a-z-]+)$',
        employee_reset_password_confirmation,
        name='employee_reset_password_confirmation'),
    url(r'^(?P<employee_id>\d+)/$', employee, name='employee_detail'),
    url(r'^(?P<employee_id>\d+)/avatar/$', employee_image, name='employee_image'),
    url(r'^(?P<employee_id>\d+)/register/device/$', employee_register_device, name='employee_register_device'),
    url(r'^(?P<employee_id>\d+)/update/$', employee_update, name='employee_update'),
    url(r'^(?P<employee_id>\d+)/update/password/$', employee_update_password, name='employee_update_password'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
