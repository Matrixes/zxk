from django.conf.urls import url
from django.contrib.auth import views as v
from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^login/$', v.login, name='login'),
    url(r'^logout/$', v.logout, name='logout'),
    url(r'^logout-then-login/$', v.logout_then_login, name='lougout_then_login'),

    url(r'^password-change/$', v.password_change, name='password_change'),
    url(r'^password-change/done/$', v.password_change_done, name='password_change_done'),

    url(r'^password-reset/$', v.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', v.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
    	   v.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', v.password_reset_complete, name='password_reset_complete'),
    
    url(r'^register/$', views.register, name='register'),
    
    url(r'^edit/$', views.edit, name='edit'),
]


'''
Django includes several forms and views in the authentication framework that
you can use straightaway. 

Create a new directory inside the templates directory of your account application
and name it registration. This is the default path where the Django authentication
views expect your authentication templates to be. 

If you are seeing the log out page of the Django administration site instead of your
own log out page, check the INSTALLED_APPS setting of your project and make sure
that django.contrib.admin comes after the account application. Both templates
are located in the same relative path and the Django template loader will use the
first one it finds.
'''