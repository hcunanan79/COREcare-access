from django.urls import path
from . import views

urlpatterns = [
    path("", views.portal_home, name="portal_home"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("debug/", views.debug_request),
]
