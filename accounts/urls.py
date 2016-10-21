from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    # 从自己的角度看自己
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^password-change/$', views.password_change, name='password_change'),

    url(r'^register/$', views.register, name='register'),

    # 从自己的角度看别人
    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),

    # github login
    url(r'^github/$', views.github_login, name='github_login'),
    url(r'^github-auth/', views.github_auth, name='github_auth'),

    #url(r'^ajax-login/$', views.ajax_login, name='ajax-login'),
]