from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addInject$', views.addInject, name='addInject'),
    url(r'^addAnimal$', views.addAnimal, name='addAnimal'),
    url(r'^addResults$', views.addResults, name='addResults'),
    url(r'^searchAnimal$', views.searchAnimal, name='searchAnimal'),
#    url(r'^searchInject$', views.searchInject, name='searchInject'),
    url(r'^FindDistance$', views.find_distance,name='find_distance'),
]
