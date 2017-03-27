from .views import category_detail, category_list
from .views import keyword_list, keyword_detail, keyword_create
from django.conf.urls import url


urlpatterns = [
    url(r'^list/$', category_list, name='category_list'),
    url(r'^(?P<category_id>\d+)/$', category_detail, name='category_detail'),
    url(r'^keyword/create/$', keyword_create, name='keyword_create'),
    url(r'^keyword/list/$', keyword_list, name='keyword_list'),
    url(r'^keyword/(?P<keyword_id>\d+)/$', keyword_detail, name='keyword_detail'),
]
