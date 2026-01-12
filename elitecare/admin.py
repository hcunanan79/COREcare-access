from django.contrib import admin

admin.site.site_header = "CORECare Access"
admin.site.site_title = "CORECare Access"
admin.site.index_title = "Dashboard"

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from credentials.models import EmployeeCredential

User = get_user_model()


class EmployeeCredentialInline(admin.TabularInline):
    model = EmployeeCredential
    extra = 0


class UserAdmin(DjangoUserAdmin):
    inlines = [EmployeeCredentialInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
