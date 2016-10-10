from django.conf.urls import url
from .views import CategoryDetail, CategoryList, KeywordDetail, KeywordList, SubcategoryDetail, SubcategoryList

urlpatterns = [
    url(r'^category/$', CategoryList.as_view()),
    url(r'^category/(?P<category_id>[0-9]+)/$', CategoryDetail.as_view()),
    url(r'^keyword/$', KeywordList.as_view()),
    url(r'^keyword/(?P<keyword_id>[0-9]+)/$', KeywordDetail.as_view()),
    url(r'^subcategory/$', SubcategoryList.as_view()),
    url(r'^subcategory/(?P<subcategory_id>[0-9]+)/$', SubcategoryDetail.as_view()),
]
