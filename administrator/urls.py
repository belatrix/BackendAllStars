from django.conf.urls import url
from .views import CategoryDetail, CategoryList, KeywordDetail, KeywordList
from .views import CategoriesModelsDelete
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^delete/categories/(?P<kind>\w+)/(?P<id>[0-9]+)/$', CategoriesModelsDelete.as_view()),
    url(r'^category/$', CategoryList.as_view()),
    url(r'^category/(?P<category_id>[0-9]+)/$', CategoryDetail.as_view()),
    url(r'^keyword/$', KeywordList.as_view()),
    url(r'^keyword/(?P<keyword_id>[0-9]+)/$', KeywordDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
