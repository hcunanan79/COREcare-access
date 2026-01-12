from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmployeeProfile
from clients.models import CareTeam   # import your proxy model

class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    can_delete = False
    extra = 0

@admin.register(CareTeam)
class CareTeamAdmin(UserAdmin):
    inlines = [EmployeeProfileInline]
