from .views import category_list, subcategory_detail, subcategories_list
from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', category_list, name='category_list'),
    url(r'^(?P<category_id>\d+)/subcategory/list/$', subcategories_list, name='subcategories_list'),
    url(r'^subcategory/(?P<subcategory_id>\d+)/$', subcategory_detail, name='subcategory_detail'),
]
