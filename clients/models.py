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
