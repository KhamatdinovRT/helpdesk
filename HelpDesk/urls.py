from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'request/$', views.request_view, name='request'),
    url(r'request/(?P<request_id>\d+)/edit/$', views.request_edit, name='edit_request'),
]