from django.contrib import admin
from .models import Client, ClientFamilyMember, ClientMessage

class ClientFamilyMemberInline(admin.TabularInline):
    model = ClientFamilyMember
    extra = 1

class ClientMessageInline(admin.TabularInline):
    model = ClientMessage
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientFamilyMemberInline, ClientMessageInline]

@admin.register(ClientFamilyMember)
class ClientFamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'client', 'relationship', 'can_view_schedule']
    list_filter = ['client']

@admin.register(ClientMessage)
class ClientMessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'client', 'content', 'created_at']
    list_filter = ['client', 'created_at']
