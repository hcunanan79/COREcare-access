

from django.db import models
from django.contrib.auth.models import User

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")

    phone = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=80, blank=True, null=True)          # e.g., Caregiver, RN, Admin
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="employee_photos/", blank=True, null=True)

    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    emergency_contact_name = models.CharField(max_length=120, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profile"# Create your models here.
