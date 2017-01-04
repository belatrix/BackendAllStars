from django.conf.urls import url
from .views import CategoryDetail, CategoryList, ObjectsDelete
from .views import KeywordList, KeywordDetail
from .views import BadgeList, BagdeDetail
from employees.views import employee_admin, employee_set_list
from employees.views import employee_bulk_creation, employee_deactivated_list, employee_activate, employee_block
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^delete/(?P<kind>\w+)/(?P<id>[0-9]+)/$', ObjectsDelete.as_view()),
    url(r'^badge/$', BadgeList.as_view()),
    url(r'^badge/(?P<badge_id>[0-9]+)/$', BagdeDetail.as_view()),
    url(r'^category/$', CategoryList.as_view()),
    url(r'^category/(?P<category_id>[0-9]+)/$', CategoryDetail.as_view()),
    url(r'^keyword/$', KeywordList.as_view()),
    url(r'^keyword/(?P<keyword_id>[0-9]+)/$', KeywordDetail.as_view()),
    url(r'^employee/create/bulk/$', employee_bulk_creation, name='employee_bulk_creation'),
    url(r'^employee/deactivated/list/$', employee_deactivated_list, name='employee_deactivated_list'),
    url(r'^employee/(?P<employee_id>\d+)/activate/(?P<action>\w+)/$', employee_activate, name='employee_activate'),
    url(r'^employee/(?P<employee_id>\d+)/block/(?P<action>\w+)/$', employee_block, name='employee_block'),
    url(r'^employee/(?P<employee_id>\d+)/admin/(?P<action>\w+)/$', employee_admin, name='employee_admin'),
    url(r'^employee/(?P<employee_id>\d+)/set/list/$', employee_set_list, name='employee_set_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
