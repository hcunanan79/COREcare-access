from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Visit(models.Model):

    caregiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visits",
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="visits",
    )

    shift = models.ForeignKey(
        'shifts.Shift',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='visits',
        help_text='Linked shift if this is a scheduled visit, null for unscheduled visits',
    )

    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    duration_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    mileage = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="Mileage cannot be negative."),
            MaxValueValidator(500, message="Mileage cannot exceed 500 miles per visit."),
        ],
        help_text="Total miles driven for this visit (max 500)",
    )

    notes = models.TextField(blank=True, null=True)

    # Issue #15: Geolocation tracking for fraud prevention
    clock_in_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude where caregiver clocked in"
    )
    clock_in_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude where caregiver clocked in"
    )
    clock_in_accuracy = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GPS accuracy in meters at clock-in"
    )
    
    clock_out_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude where caregiver clocked out"
    )
    clock_out_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude where caregiver clocked out"
    )
    clock_out_accuracy = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GPS accuracy in meters at clock-out"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            # Optimizes weekly summary aggregations: filter by caregiver + date range
            models.Index(fields=['caregiver', 'clock_in'], name='idx_visit_cg_clockin'),
            # Fast lookup of active visits: WHERE clock_out IS NULL
            models.Index(fields=['clock_out'], name='idx_visit_clockout'),
        ]

    def clean(self):
        """Validate visit data integrity."""
        super().clean()
        
        # SECURITY: Ensure caregiver cannot clock into another caregiver's shift (issue #6)
        if self.shift and self.caregiver and self.shift.caregiver != self.caregiver:
            raise ValidationError({
                'shift': 'Visit caregiver must match the shift\'s assigned caregiver.'
            })
        
        # DATA QUALITY: Validate mileage (issue #5)
        if self.mileage is not None:
            if self.mileage < 0:
                raise ValidationError({
                    'mileage': 'Mileage cannot be negative.'
                })
            if self.mileage > 500:
                raise ValidationError({
                    'mileage': 'Mileage cannot exceed 500 miles per visit. Please verify your entry.'
                })

    def __str__(self):
        return f"{self.caregiver} -> {self.client} ({self.clock_in})"


class VisitComment(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment on {self.visit} by {self.author}"


class AuditLog(models.Model):
    """Issue #9: Comprehensive audit logging for security and compliance."""
    ACTION_CHOICES = [
        ('clock_in', 'Clock In'),
        ('clock_out', 'Clock Out'),
        ('visit_create', 'Visit Created'),
        ('visit_update', 'Visit Updated'),
        ('visit_delete', 'Visit Deleted'),
        ('mileage_update', 'Mileage Updated'),
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('permission_denied', 'Permission Denied'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    visit = models.ForeignKey(
        Visit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
    )
    shift = models.ForeignKey(
        'shifts.Shift',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['visit']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"
