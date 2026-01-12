from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import include

admin.site.site_header = "CORECare Access"
admin.site.site_title = "CORECare Access"
admin.site.index_title = "Easing the way to better care"

urlpatterns = [
    path("caregiver/", include("caregiver_portal.urls")),    
    path("admin/", admin.site.urls),
    path("schedule/", include("clients.urls")),
    path("portal/", include("portal.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
