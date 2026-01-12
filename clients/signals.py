from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client, PatientProfile


@receiver(post_save, sender=Client)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        PatientProfile.objects.create(client=instance)
