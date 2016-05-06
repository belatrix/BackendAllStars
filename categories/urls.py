from .views import category_list, keyword_list, subcategory_detail, subcategory_list, subcategory_list_by_category
from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', category_list, name='category_list'),
    url(r'^(?P<category_id>\d+)/subcategory/list/$', subcategory_list_by_category, name='subcategory_list_by_category'),
    url(r'^keyword/list/$', keyword_list, name='keyword_list'),
    url(r'^subcategory/list/$', subcategory_list, name='subcategory_list'),
    url(r'^subcategory/(?P<subcategory_id>\d+)/$', subcategory_detail, name='subcategory_detail'),
]
