from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^password-change/$', views.password_change, name='password_change'),
    # 账户关联信息的url 。。。。。。
    url(r'^settings/$', views.user_settings, name='user_settings'),

    url(r'^register/$', views.register, name='register'),

    # 我的主页相关url
    #url(r'^$', views.index, name='index'),
    url(r'^myhome/$', views.myhome, name='myhome'),
    url(r'^myposts/$', views.myposts, name='myposts'),
    url(r'^mycomments/$', views.mycomments, name='mycomments'),
    # 我的分享还没添加
    


    # 从自己的角度看别人, 记得将user_follow放到user_detail前面哟
    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),


    # github login
    url(r'^github/$', views.github_login, name='github_login'),
    url(r'^github-auth/', views.github_auth, name='github_auth'),

    #url(r'^ajax-login/$', views.ajax_login, name='ajax-login'),
]