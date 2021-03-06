from django.conf.urls import url
from .feeds import LatestPostsFeed
from . import views


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.index_1, name='index'),

    # url(r'^$', views.PostListView.as_view(), name='index'),

    url(r'^(?P<id>\d*)/$', views.post, name='post'),

    # url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'), 
    
    url(r'^tag/(?P<tag>[-\w]+)', views.tag, name='tag'),

    #url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post, name='post'),
    
    url(r'^post-like/', views.post_like, name='post_like'),
    url(r'(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),

    url(r'^publish/$', views.publish, name='publish'),
    # url融合了
    #url(r'^publish/md$', views.publish_md, name='publish_md'),
    
    # 修改博客
    url(r'^(?P<id>\d*)/edit/$', views.edit, name='edit'),
]