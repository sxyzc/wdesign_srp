from django.conf.urls import url

from . import views

app_name = 'srp'
urlpatterns = [
    #url(r'^test', views.test, name='test'),
    url(r'^index', views.index, name='index'),
    url(r'^detail', views.detail, name='detail'),
    url(r'^introduce', views.introduce, name='introduce'),
    url(r'^process_get', views.process_get, name='process'),
    url(r'^search', views.process_search, name='search'),
    url(r'^update_data', views.update_data, name='update_data'),
    url(r'^viewer', views.viewer, name='viewer'),
    
    # url(r'^mainPage', views.mainPage),
    # url(r'^login', views.login, name='login'),
    # url(r'^register', views.register, name='register'),

]
