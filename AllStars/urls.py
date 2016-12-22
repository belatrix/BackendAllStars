"""AllStars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^api/auth/', include('djoser.urls.authtoken')),
    url(r'^api/activity/', include('activities.urls', namespace='activities')),
    url(r'^api/admin/', include('administrator.urls', namespace='administrator')),
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^api/employee/', include('employees.urls', namespace='employees')),
    url(r'^api/category/', include('categories.urls', namespace='categories')),
    url(r'^api/star/', include('stars.urls', namespace='stars')),
    # url(r'^api/event/', include('events.urls', namespace='events')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
