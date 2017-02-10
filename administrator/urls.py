from django.conf.urls import url
from .views import MessageList, MessageDetail, MessageListFromEmployee, SiteInfoDetail
from .views import CategoryDetail, CategoryList, ObjectsDelete
from .views import EmployeeList, EmployeeTopList
from .views import EventList, EventDetail, EventActivityList, EventActivityDetail
from .views import KeywordList, KeywordDetail
from .views import BadgeList, BagdeDetail
from .views import LocationList, LocationDetail
from .views import PositionList, PositionDetail
from .views import RoleList, RoleDetail
from employees.views import employee_admin, employee_set_list
from employees.views import employee_bulk_creation, employee_deactivated_list, employee_activate, employee_block
from stars.views import give_badge_to
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^delete/(?P<kind>\w+)/(?P<id>[0-9]+)/$', ObjectsDelete.as_view()),
    url(r'^badge/$', BadgeList.as_view()),
    url(r'^badge/(?P<badge_id>[0-9]+)/$', BagdeDetail.as_view()),
    url(r'^badge/(?P<badge_id>[0-9]+)/to/(?P<to_employee_id>[0-9]+)/from/(?P<from_employee_id>[0-9]+)/$',
        give_badge_to,
        name='give_badge_to'),
    url(r'^category/$', CategoryList.as_view()),
    url(r'^category/(?P<category_id>[0-9]+)/$', CategoryDetail.as_view()),
    url(r'^employee/$', EmployeeList.as_view()),
    url(r'^employee/top/(?P<kind>\w+)/$', EmployeeTopList.as_view()),
    url(r'^event/$', EventList.as_view()),
    url(r'^event/(?P<event_id>[0-9]+)/$', EventDetail.as_view()),
    url(r'^event/(?P<event_id>[0-9]+)/news/$', EventActivityList.as_view()),
    url(r'^event/(?P<event_id>[0-9]+)/news/(?P<news_id>[0-9]+)/$', EventActivityDetail.as_view()),
    url(r'^message/$', MessageList.as_view()),
    url(r'^message/from/employee/(?P<employee_id>[0-9]+)/$', MessageListFromEmployee.as_view()),
    url(r'^message/(?P<message_id>[0-9]+)/$', MessageDetail.as_view()),
    url(r'^keyword/$', KeywordList.as_view()),
    url(r'^keyword/(?P<keyword_id>[0-9]+)/$', KeywordDetail.as_view()),
    url(r'^location/$', LocationList.as_view()),
    url(r'^location/(?P<location_id>[0-9]+)/$', LocationDetail.as_view()),
    url(r'^position/$', PositionList.as_view()),
    url(r'^position/(?P<position_id>[0-9]+)/$', PositionDetail.as_view()),
    url(r'^role/$', RoleList.as_view()),
    url(r'^role/(?P<role_id>[0-9]+)/$', RoleDetail.as_view()),
    url(r'^employee/create/bulk/$', employee_bulk_creation, name='employee_bulk_creation'),
    url(r'^employee/deactivated/list/$', employee_deactivated_list, name='employee_deactivated_list'),
    url(r'^employee/(?P<employee_id>\d+)/activate/(?P<action>\w+)/$', employee_activate, name='employee_activate'),
    url(r'^employee/(?P<employee_id>\d+)/block/(?P<action>\w+)/$', employee_block, name='employee_block'),
    url(r'^employee/(?P<employee_id>\d+)/admin/(?P<action>\w+)/$', employee_admin, name='employee_admin'),
    url(r'^employee/(?P<employee_id>\d+)/set/list/$', employee_set_list, name='employee_set_list'),
    url(r'^site/info/$', SiteInfoDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
