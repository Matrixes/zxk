from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),

    url(r'^register/$', views.register, name='register'),

    url(r'^github/$', views.github_login, name='github_login'),
    url(r'^github_auth/', views.github_auth, name='github_auth'),

]