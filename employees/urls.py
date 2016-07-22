from .views import employee, employee_block, employee_categories, employee_list, employee_bulk_creation
from .views import employee_creation, employee_activate, employee_deactivate, employee_update, employee_update_password
from .views import employee_deactivated_list, employee_location_list, employee_role_list, employee_image
from .views import employee_reset_password, employee_reset_password_confirmation, employee_register_device
from .views import CustomObtainAuthToken, top, employee_logout, employee_skills
from django.conf.urls import url


urlpatterns = [
    url(r'^authenticate/', CustomObtainAuthToken.as_view()),
    url(r'^create/$', employee_creation, name='employee_creation'),
    url(r'^create/bulk/$', employee_bulk_creation, name='employee_bulk_creation'),
    url(r'^list/$', employee_list, name='employee_list'),
    url(r'^list/deactivated/$', employee_deactivated_list, name='employee_deactivated_list'),
    url(r'^list/top/(?P<kind>\w+)/(?P<quantity>\d+)/$', top, name='employee_list_top'),
    url(r'^logout/$', employee_logout, name='employee_logout'),
    url(r'^location/list/$', employee_location_list, name='employee_location_list'),
    url(r'^role/list/$', employee_role_list, name='employee_role_list'),
    url(r'^reset/password/(?P<employee_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', employee_reset_password, name='employee_reset_password'),
    url(r'^reset/password/(?P<employee_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<employee_uuid>[0-9a-z-]+)$', employee_reset_password_confirmation, name='employee_reset_password_confirmation'),
    url(r'^(?P<employee_id>\d+)/$', employee, name='employee_detail'),
    url(r'^(?P<employee_id>\d+)/activate/$', employee_activate, name='employee_activate'),
    url(r'^(?P<employee_id>\d+)/avatar/$', employee_image, name='employee_image'),
    url(r'^(?P<employee_id>\d+)/block/(?P<action>\w+)/$', employee_block, name='employee_block'),
    url(r'^(?P<employee_id>\d+)/category/list/$', employee_categories, name='employee_category_list'),
    url(r'^(?P<employee_id>\d+)/skills/list/$', employee_skills, name='employee_skills'),
    url(r'^(?P<employee_id>\d+)/deactivate/$', employee_deactivate, name='employee_deactivate'),
    url(r'^(?P<employee_id>\d+)/register/device/$', employee_register_device, name='employee_register_device'),
    url(r'^(?P<employee_id>\d+)/update/$', employee_update, name='employee_update'),
    url(r'^(?P<employee_id>\d+)/update/password/$', employee_update_password, name='employee_update_password'),
]
