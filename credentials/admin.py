from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import EmployeeCredential

User = get_user_model()


@admin.register(EmployeeCredential)
class EmployeeCredentialAdmin(admin.ModelAdmin):
    list_display = ("employee", "credential_type", "expiration_date")
    list_filter = ("credential_type",)
    search_fields = ("employee__username", "employee__first_name", "employee__last_name")


class EmployeeCredentialInline(admin.TabularInline):
    model = EmployeeCredential
    extra = 0


class UserAdmin(DjangoUserAdmin):
    inlines = [EmployeeCredentialInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
