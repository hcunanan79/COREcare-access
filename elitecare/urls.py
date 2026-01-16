from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView

admin.site.site_header = "CORECare Access"
admin.site.site_title = "CORECare Access"
admin.site.index_title = "Home : BayArea Elite Homecare"

urlpatterns = [
    path("", lambda request: redirect("/portal/")),  # 👈 MUST BE FIRST

    path("caregiver/", include("caregiver_portal.urls")),
    path("admin/", admin.site.urls),
    path("schedule/", include("clients.urls")),
    path("portal/", include("portal.urls")),
    
    # Issue #16: Service Worker for PWA (must be at root scope)
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw'),
]

from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
