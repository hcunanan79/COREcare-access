from django.db import models
from django.conf import settings


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

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.caregiver} -> {self.client}"

    # Billing is disabled for now (Invoice model not built yet)
    # invoice = models.ForeignKey(
    #     "clients.Invoice",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caregiver} -> {self.client} ({self.start_time} - {self.end_time})"
