from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.timeclock_login, name="timeclock_login"),
    path("", views.timeclock_home, name="timeclock_home"),
]
