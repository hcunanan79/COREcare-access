from django.db import models
from django.conf import settings
from clients.models import Client
from decimal import Decimal
from django.core.exceptions import ValidationError


class Shift(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="shifts",
    )

    caregiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_shifts",
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    pay_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    bill_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    duration_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    total_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    total_bill = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

        if self.pay_rate is not None and self.pay_rate < 0:
            raise ValidationError("Pay rate cannot be negative.")

        if self.bill_rate is not None and self.bill_rate < 0:
            raise ValidationError("Bill rate cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.start_time and self.end_time:
            seconds = (self.end_time - self.start_time).total_seconds()
            hours = Decimal(seconds) / Decimal("3600")
            self.duration_hours = hours.quantize(Decimal("0.01"))

            if self.pay_rate is not None:
                self.total_pay = (self.duration_hours * self.pay_rate).quantize(Decimal("0.01"))

            if self.bill_rate is not None:
                self.total_bill = (self.duration_hours * self.bill_rate).quantize(Decimal("0.01"))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Shift — {self.client} — {self.start_time}"
