from .views import category_list, subcategories_list
from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', category_list, name='category_list'),
    url(r'^(?P<category_id>\d+)/subcategory/list/$', subcategories_list, name='subcategories_list')
]
