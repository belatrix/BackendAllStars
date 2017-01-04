from .views import give_star_to, star, give_star_to_many, stars_employee_list
from .views import stars_top_employee_lists, stars_employee_list_group_by_category
from .views import stars_employee_list_group_by_category_detail, stars_employee_list_group_by_keyword_detail
from .views import stars_employee_list_group_by_keyword
from .views import stars_keyword_list, stars_keyword_list_detail
from .views import badges_employee_list, employee_list_group_by_badges, employee_list_group_by_badges_detail
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<from_employee_id>\d+)/give/star/to/(?P<to_employee_id>\d+)/', give_star_to, name='give_star_to'),
    url(r'^(?P<from_employee_id>\d+)/give/star/to/many/$', give_star_to_many, name='give_star_to_many'),
    url(r'^(?P<star_id>\d+)/$', star, name='star_detail'),
    url(r'^(?P<employee_id>\d+)/list/$', stars_employee_list, name='stars_employee_list'),
    url(r'^(?P<employee_id>\d+)/badge/list/$', badges_employee_list, name='badges_employee_list'),
    url(r'^(?P<employee_id>\d+)/list/group/category/$', stars_employee_list_group_by_category, name='stars_employee_list_group_by_category'),
    url(r'^(?P<employee_id>\d+)/list/group/keyword/$', stars_employee_list_group_by_keyword, name='stars_employee_list_group_by_keyword'),
    url(r'^(?P<employee_id>\d+)/list/group/category/(?P<category_id>\d+)/$',
        stars_employee_list_group_by_category_detail,
        name='stars_employee_list_group_by_category_detail'),
    url(r'^(?P<employee_id>\d+)/list/group/keyword/(?P<keyword_id>\d+)/$',
        stars_employee_list_group_by_keyword_detail,
        name='stars_employee_list_group_by_keyword_detail'),
    url(r'^badge/employee/list/$', employee_list_group_by_badges, name='employee_list_group_by_badges'),
    url(r'^badge/(?P<badge_id>\d+)/employee/list/$', employee_list_group_by_badges_detail, name='employee_list_group_by_badges_detail'),
    url(r'^keyword/list/$', stars_keyword_list, name='stars_keyword_list'),
    url(r'^keyword/(?P<keyword_id>\d+)/list/$', stars_keyword_list_detail, name='stars_keyword_list_detail'),
    url(r'^top/(?P<top_number>\d+)/(?P<kind>\w+)/(?P<id>\d+)/', stars_top_employee_lists, name='stars_top_employee_lists'),
]
