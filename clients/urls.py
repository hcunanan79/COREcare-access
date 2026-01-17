"""
Issue #40: Client Calendar URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    # Legacy schedule view
    path("schedule/", views.schedule, name="clients_schedule"),
    
    # Issue #40: Client Calendar
    path("<int:client_id>/calendar/", views.client_calendar, name="client_calendar"),
    path("<int:client_id>/calendar/api/", views.calendar_api, name="calendar_api"),
    
    # Issue #40: Event Management
    path("<int:client_id>/events/create/", views.create_event, name="create_event"),
    path("<int:client_id>/events/<int:event_id>/edit/", views.edit_event, name="edit_event"),
    path("<int:client_id>/events/<int:event_id>/delete/", views.delete_event, name="delete_event"),
    path("<int:client_id>/events/<int:event_id>/restore/", views.restore_event, name="restore_event"),
    
    # Issue #40: Attachments
    path("<int:client_id>/events/<int:event_id>/attachments/upload/", views.upload_attachment, name="upload_attachment"),
    path("<int:client_id>/events/<int:event_id>/attachments/<int:attachment_id>/delete/", views.delete_attachment, name="delete_attachment"),
]

