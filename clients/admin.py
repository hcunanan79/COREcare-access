from django.contrib import admin
from .models import Client, ClientFamilyMember, ClientMessage, ClientCalendarEvent, EventAttachment

class ClientFamilyMemberInline(admin.TabularInline):
    model = ClientFamilyMember
    extra = 1

class ClientMessageInline(admin.TabularInline):
    model = ClientMessage
    extra = 0
    readonly_fields = ['created_at']

class ClientCalendarEventInline(admin.TabularInline):
    model = ClientCalendarEvent
    extra = 0
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    fields = ['title', 'event_type', 'start_time', 'end_time', 'location', 'created_by', 'created_at']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientFamilyMemberInline, ClientCalendarEventInline, ClientMessageInline]

@admin.register(ClientFamilyMember)
class ClientFamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'client', 'relationship', 'can_view_schedule']
    list_filter = ['client']

@admin.register(ClientMessage)
class ClientMessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'client', 'content', 'created_at']
    list_filter = ['client', 'created_at']


class EventAttachmentInline(admin.TabularInline):
    model = EventAttachment
    extra = 0
    readonly_fields = ['uploaded_at', 'uploaded_by', 'file_size']
    fields = ['file', 'original_filename', 'file_size', 'uploaded_by', 'uploaded_at']


@admin.register(ClientCalendarEvent)
class ClientCalendarEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'event_type', 'start_time', 'end_time', 'created_by', 'attachment_count', 'is_active']
    list_filter = ['client', 'event_type', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    date_hierarchy = 'start_time'
    inlines = [EventAttachmentInline]
    
    def is_active(self, obj):
        return not obj.is_deleted
    is_active.boolean = True
    is_active.short_description = 'Active'
    
    def attachment_count(self, obj):
        return obj.attachments.count()
    attachment_count.short_description = 'Files'
    
    def get_queryset(self, request):
        """Include soft-deleted events for admin view."""
        return ClientCalendarEvent.all_objects.all()
    
    actions = ['soft_delete_selected', 'restore_selected']
    
    def soft_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.soft_delete()
        self.message_user(request, f"{queryset.count()} event(s) soft-deleted.")
    soft_delete_selected.short_description = "Soft delete selected events"
    
    def restore_selected(self, request, queryset):
        for obj in queryset:
            obj.restore()
        self.message_user(request, f"{queryset.count()} event(s) restored.")
    restore_selected.short_description = "Restore selected events"


@admin.register(EventAttachment)
class EventAttachmentAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'event', 'human_file_size', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_at', 'content_type']
    search_fields = ['original_filename', 'event__title']
    readonly_fields = ['uploaded_at']
    
    def human_file_size(self, obj):
        return obj.human_file_size
    human_file_size.short_description = 'Size'


