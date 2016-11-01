from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.image_create, name='create'),
    url(r'^detail/(?P<id>\d+)/$', views.image_detail, name='detail'),
    url(r'^like/$', views.image_like, name='like'),
]
