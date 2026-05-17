from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'iSpeye Distribution Admin'
admin.site.site_title = 'iSpeye Admin'
admin.site.index_title = 'Access Control Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('distribution.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
