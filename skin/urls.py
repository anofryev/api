from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.site.site_header = 'Skin Hadleylab administrative interface'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/web_ui/')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('rest_framework.urls')),
    url(r'^api/v1/', include('apps.accounts.urls')),
    url(r'^api/v1/', include('apps.moles.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
