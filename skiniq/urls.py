from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('rest_framework.urls')),
    url(r'^api/v1/accounts/', include('apps.accounts.urls')),
    url(r'^api/v1/moles/', include('apps.moles.urls')),
]
