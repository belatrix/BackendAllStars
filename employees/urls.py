from .views import employee_list, employee
from django.conf.urls import url


urlpatterns = [
    url(r'^list/$', employee_list, name='employee_list'),
    url(r'^(?P<employee_id>\d+)/$', employee, name='employee_detail'),
]
