from .views import category_add, category_list
from .views import keyword_list, subcategory_detail, subcategory_list, subcategory_list_by_category, keyword_add
from django.conf.urls import url

urlpatterns = [
    url(r'^add/$', category_add, name='category_add'),
    url(r'^list/$', category_list, name='category_list'),
    url(r'^(?P<category_id>\d+)/subcategory/list/$', subcategory_list_by_category, name='subcategory_list_by_category'),
    url(r'^keyword/add/$', keyword_add, name='keyword_add'),
    url(r'^keyword/list/$', keyword_list, name='keyword_list'),
    url(r'^subcategory/list/$', subcategory_list, name='subcategory_list'),
    url(r'^subcategory/(?P<subcategory_id>\d+)/$', subcategory_detail, name='subcategory_detail'),
]
