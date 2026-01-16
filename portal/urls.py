from django.urls import path
from . import views

urlpatterns = [
    path("", views.portal_home, name="portal_home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("offline/", views.offline_view, name="offline"),
    
    # Issue #22: Family Portal
    path("family/", views.family_home, name="family_home"),
    path("family/client/<int:client_id>/", views.family_client_detail, name="family_client_detail"),
]
