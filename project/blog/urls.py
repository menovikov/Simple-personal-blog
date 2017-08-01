from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from posts.views import profile_view, redirect_view
from . import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include("posts.urls")),
    url(r'^profile/$', profile_view),
    url(r'^$', redirect_view),
]

handler404 = 'posts.views.handler404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
