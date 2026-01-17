from django.db import models
from urllib.parse import quote_plus

class Client(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name  = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    diagnosis = models.TextField(blank=True)
    care_plan = models.TextField(blank=True)

    class CareAssessment(models.Model):
        client = models.OneToOneField(
            "clients.Client",
            on_delete=models.CASCADE,
            related_name="assessment",
    )

    care_needs = models.TextField(blank=True, null=True)
    demographics = models.TextField(blank=True, null=True)
    community_care = models.TextField(blank=True, null=True)

    adls = models.TextField("Activities of Daily Living (ADLs)", blank=True, null=True)
    iadls = models.TextField("Instrumental Activities of Daily Living (IADLs)", blank=True, null=True)

    def __str__(self):
        return f"Assessment for {self.client}"

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def full_address(self):
        parts = [
            getattr(self, "address_line1", None),
            getattr(self, "city", None),
            getattr(self, "state", None),
            getattr(self, "zip_code", None),
        ]
        return ", ".join([p for p in parts if p])

    def google_maps_directions_url(self):
        addr = quote_plus(self.full_address() or "")
        return f"https://www.google.com/maps/dir/?api=1&destination={addr}"

    def apple_maps_directions_url(self):
        addr = quote_plus(self.full_address() or "")
        return f"https://maps.apple.com/?daddr={addr}&dirflg=d"

from django.contrib.auth.models import User

class CareTeam(User):
    class Meta:
        proxy = True
        app_label = "auth"              # keeps it under Authentication and Authorization
        verbose_name = "Care Team"
        verbose_name_plural = "Care Team"


from django.conf import settings

class ClientFamilyMember(models.Model):
    """
    Issue #22: Links a User (Family) to a Client for schedule visibility.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='family_members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='linked_clients')
    relationship = models.CharField(max_length=50, blank=True, help_text="e.g. Son, Daughter, Spouse")
    
    # Permissions
    can_view_schedule = models.BooleanField(default=True)
    can_message_caregivers = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['client', 'user']
        verbose_name = "Family Member"
        verbose_name_plural = "Family Members"

    def __str__(self):
        return f"{self.user} ({self.relationship}) -> {self.client}"


class ClientMessage(models.Model):
    """
    Issue #22: Communication channel between Family and Caregivers (via Client context).
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: visibility flags (e.g. private to admin vs public to caregivers)
    is_internal_only = models.BooleanField(default=False, help_text="If true, only visible to admins/staff, not caregivers.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Msg from {self.author} re: {self.client} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ClientCalendarEvent(models.Model):
    """
    Issue #40: Family-managed calendar events for clients.
    Allows family members to add appointments, activities, and other events
    that caregivers should be aware of.
    """
    
    class EventType(models.TextChoices):
        MEDICAL = 'medical', 'Medical'
        SOCIAL = 'social', 'Social'
        FAMILY = 'family', 'Family'
        THERAPY = 'therapy', 'Therapy'
        TRANSPORTATION = 'transportation', 'Transportation'
        OTHER = 'other', 'Other'
    
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='calendar_events'
    )
    title = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=20, 
        choices=EventType.choices, 
        default=EventType.OTHER
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    # Audit fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_calendar_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft delete support
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Future: External calendar sync
    external_id = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="External calendar event ID (Google, Outlook, etc.)"
    )
    
    class Meta:
        ordering = ['start_time']
        indexes = [
            # Optimizes date-range queries for client calendar view
            models.Index(fields=['client', 'start_time'], name='idx_event_client_start'),
            # Optimizes "my recent events" queries
            models.Index(fields=['created_by', 'created_at'], name='idx_event_creator'),
        ]
        verbose_name = "Calendar Event"
        verbose_name_plural = "Calendar Events"
    
    def clean(self):
        """Validate that end_time is after start_time."""
        from django.core.exceptions import ValidationError
        
        if self.end_time and self.start_time:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': 'End time must be after start time.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def soft_delete(self):
        """Mark the event as deleted without removing from database."""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        """Restore a soft-deleted event."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None
    
    @property
    def event_type_icon(self):
        """Return an icon for the event type (for accessibility)."""
        icons = {
            'medical': '🩺',
            'social': '👥',
            'family': '👨‍👩‍👧',
            'therapy': '💆',
            'transportation': '🚗',
            'other': '📌',
        }
        return icons.get(self.event_type, '📌')
    
    def __str__(self):
        return f"{self.title} ({self.client}) - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class ClientCalendarEventManager(models.Manager):
    """Custom manager to filter out soft-deleted events by default."""
    
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    
    def with_deleted(self):
        """Include soft-deleted events."""
        return super().get_queryset()
    
    def deleted_only(self):
        """Only soft-deleted events."""
        return super().get_queryset().filter(deleted_at__isnull=False)


# Replace the default manager with the custom one
ClientCalendarEvent.objects = ClientCalendarEventManager()
ClientCalendarEvent.objects.model = ClientCalendarEvent

# Keep a reference to all objects (including deleted)
ClientCalendarEvent.all_objects = models.Manager()
ClientCalendarEvent.all_objects.model = ClientCalendarEvent
