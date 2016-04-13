from.views import subcategories_list
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<category_id>\d+)/subcategory/list/$', subcategories_list, name='subcategories_list')
]