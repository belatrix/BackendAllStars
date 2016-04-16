from .views import employee, employee_categories, employee_list
from .views import CustomObtainAuthToken, search, top
from django.conf.urls import url


urlpatterns = [
    url(r'^authenticate/', CustomObtainAuthToken.as_view()),
    url(r'^list/$', employee_list, name='employee_list'),
    url(r'^list/top/(?P<kind>\w+)/(?P<quantity>\d+)/$', top, name='employee_list_top'),
    url(r'^(?P<employee_id>\d+)/$', employee, name='employee_detail'),
    url(r'^(?P<employee_id>\d+)/category/list/$', employee_categories, name='employee_category_list'),
    url(r'^search/(?P<search_term>\w+)/', search, name='employee_search'),
]
