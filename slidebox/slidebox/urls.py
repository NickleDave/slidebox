from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^slidebox/', include('slideAdmin.urls', namespace="slideAdmin")),
    url(r'^admin/', include(admin.site.urls)),
]
