from django.db import models
from django.conf import settings
from shifts.models import Shift


class TimeEntry(models.Model):
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name="clock_entries"
    )
    caregiver = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="timeclock_entries"
)

    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    in_lat = models.FloatField(null=True, blank=True)
    in_lng = models.FloatField(null=True, blank=True)
    out_lat = models.FloatField(null=True, blank=True)
    out_lng = models.FloatField(null=True, blank=True)

    accuracy_m = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caregiver} – {self.shift}"
