from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
urlpatterns = [
    # Examples:
    # url(r'^$', 'chatPro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chat',include('chat.urls')),
]
