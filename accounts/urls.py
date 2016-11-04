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
    url(r'^myshare/$', views.myshare, name='myshare'),
    url(r'^mydrafts/$', views.mydrafts, name='mydrafts'),
    url(r'^mycollects/$', views.mycollects, name='mycollects'),
    url(r'^myfollowing/$', views.myfollowing, name='myfollowing'),
    url(r'^myfollowers/$', views.myfollowers, name='myfollowers'),
    
    # 添加到收藏
    url(r'^collecting/$', views.collecting, name='collecting'),
    # 收藏夹

    # 从自己的角度看别人, 记得将user_follow放到user_detail前面哟
    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),

    # 其它用户的主页及相关信息等
    url(r'^users/(?P<username>[-\w]+)/$', views.user_home, name='user_home'),
    url(r'^users/(?P<username>[-\w]+)/posts/$', views.user_posts, name='user_posts'),
    url(r'^users/(?P<username>[-\w]+)/comments/$', views.user_comments, name='user_comments'),
    url(r'^users/(?P<username>[-\w]+)/share/$', views.user_share, name='user_share'),
    url(r'^users/(?P<username>[-\w]+)/following/$', views.user_following, name='user_following'),
    url(r'^users/(?P<username>[-\w]+)/followers/$', views.user_followers, name='user_followers'),


    # github login
    url(r'^github/$', views.github_login, name='github_login'),
    url(r'^github-auth/', views.github_auth, name='github_auth'),

    #url(r'^ajax-login/$', views.ajax_login, name='ajax-login'),
]