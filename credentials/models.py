from django.db import models
from django.conf import settings


class EmployeeCredential(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_credentials",
    )

    CREDENTIAL_TYPES = [
        ("CPR", "CPR Certification"),
        ("TB", "TB Test"),
        ("ID", "Government ID"),
        ("LICENSE", "Professional License"),
        ("BACKGROUND", "Background Check"),
        ("OTHER", "Other"),
    ]

    credential_type = models.CharField(max_length=20, choices=CREDENTIAL_TYPES)
    document = models.FileField(upload_to="employee_credentials/", blank=True, null=True)
    issued_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee} — {self.get_credential_type_display()}"
