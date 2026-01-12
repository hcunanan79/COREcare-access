from django.db import models
from clients.models import Client


class CareAssessment(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="care_assessment",
    )

    care_needs = models.TextField(blank=True, null=True)
    demographics = models.TextField(blank=True, null=True)
    community_care = models.TextField(blank=True, null=True)
    adls = models.TextField(blank=True, null=True)
    iadls = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Care Assessment — {self.client}"

# Create your models here.
