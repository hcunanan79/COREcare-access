from django.urls import path
from . import views

urlpatterns = [
    path("", views.portal_home, name="portal_home"),
    path("signup/", views.signup, name="signup"),   # 👈 THIS LINE IS REQUIREDi
]
