from django.contrib import admin
from django.utils.html import format_html
from .models import Shift


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("caregiver", "client", "start_time", "end_time", "navigate")
    list_filter = ("caregiver", "client")

    def navigate(self, obj):
        if not obj.client:
            return "-"

        address = obj.client.full_address()
        if not address:
            return "-"

        apple = obj.client.apple_maps_directions_url()
        google = obj.client.google_maps_directions_url()

        return format_html(
            '<a href="{}" target="_blank">Apple Maps</a> | <a href="{}" target="_blank">Google Maps</a>',
            apple,
            google
        )

    navigate.short_description = "GPS"
