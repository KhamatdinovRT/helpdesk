from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'requests/$', views.request_view, name='request'),
    url(r'temp_requests$', views.temp_requests_view, name='temp_requests'),
    url(r'request/(?P<request_id>\d+)/edit/$', views.request_edit, name='edit_request'),
    url(r'request/temp/(?P<request_id>\d+)/delete/$', views.delete_request_from_temp, name='delete_request'),
    url(r'^request/create/$', views.create_request, name='req_create'),
    url(r'request/temp/(?P<request_id>\d+)/edit/$', views.create_request_from_temp, name='create_request_from_temp'),
    url(r'^login/$', auth_views.login,  name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^admin/', admin.site.urls),   
    url(r'^$', views.index),
]