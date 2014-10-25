#coding:utf-8
from django.conf.urls import patterns, include, url
from chat import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lvxing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^/register$', views.register, name='register'),
    url(r'^/loginValidate$', views.loginValidate, name='loginValidate'),
)
