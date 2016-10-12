from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>.*?)/$', views.user, name='user'),

    url(r'^edit/$', views.edit, name='edit'),
    url(r'^password-change/$', views.password_change, name='password_change'),

    url(r'^register/$', views.register, name='register'),

    url(r'^github/$', views.github_login, name='github_login'),
    url(r'^github-auth/', views.github_auth, name='github_auth'),

    #url(r'^ajax-login/$', views.ajax_login, name='ajax-login'),

    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),
]