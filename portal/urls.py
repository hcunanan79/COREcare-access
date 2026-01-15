from django.urls import path
from . import views

urlpatterns = [
    path("", views.portal_home, name="portal_home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.employee_dashboard, name="employee_dashboard"),
]
