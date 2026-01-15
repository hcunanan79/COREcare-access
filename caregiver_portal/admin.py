from django.contrib import admin
from .models import Visit, VisitComment


class VisitCommentInline(admin.TabularInline):
    model = VisitComment
    extra = 0
    readonly_fields = ("author", "created_at")


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("caregiver", "client", "clock_in", "clock_out", "duration_hours", "mileage")
    list_filter = ("caregiver", "client")
    search_fields = ("caregiver__username", "client__first_name", "client__last_name")
    inlines = [VisitCommentInline]


@admin.register(VisitComment)
class VisitCommentAdmin(admin.ModelAdmin):
    list_display = ("visit", "author", "created_at", "text_preview")
    list_filter = ("author",)
    search_fields = ("text", "author__username")

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Comment"
