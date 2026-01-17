from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from credentials.models import EmployeeCredential
from clients.models import Client
from shifts.models import Shift
from caregiver_portal.models import Visit
from timeclock.models import TimeEntry

User = get_user_model()


class EmployeeCredentialInline(admin.TabularInline):
    model = EmployeeCredential
    extra = 0


class UserAdmin(DjangoUserAdmin):
    inlines = [EmployeeCredentialInline]


# ====== ADMIN DASHBOARD TILES ======
# Create custom AdminSite class to override index view
class COREcareAdminSite(admin.AdminSite):
    site_header = "CORECare Access"
    site_title = "CORECare Access"
    index_title = "Dashboard"
    index_template = 'admin/index.html'

    def index(self, request, extra_context=None):
        """
        Custom admin index view that provides model counts for dashboard tiles.
        """
        # Get counts for each tile
        context = {
            'clients_count': Client.objects.count(),
            'shifts_count': Shift.objects.count(),
            'visits_count': Visit.objects.count(),
            'timeentries_count': TimeEntry.objects.count(),
            'credentials_count': EmployeeCredential.objects.count(),
        }

        # Merge with any extra context
        if extra_context:
            context.update(extra_context)

        # Call parent index with our context
        return super().index(request, extra_context=context)


# Replace the default admin site with our custom one
admin.site = COREcareAdminSite()

# Now register User with the custom admin site
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
