from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from portal.views import root_redirect

admin.site.site_header = "CORECare Access"
admin.site.site_title = "CORECare Access"
admin.site.index_title = "Home : BayArea Elite Homecare"

urlpatterns = [
    path("", root_redirect, name="root"),  # Issue #29: Smart redirect

    path("caregiver/", include("caregiver_portal.urls")),
    path("admin/", admin.site.urls),
    path("schedule/", include("clients.urls")),
    path("clients/", include("clients.urls")),  # Issue #40: Client calendar routes
    path("portal/", include("portal.urls")),
    
    # Issue #16: Service Worker for PWA (must be at root scope)
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production media serving (for Render persistent disk)
    # In a proper production setup (AWS S3), this wouldn't be needed.
    # But for Render Disk, we must serve the files via Django.
    from django.urls import re_path
    from django.views.static import serve
    
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

