from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Visit
from .utils import update_weekly_summary

@receiver(post_save, sender=Visit)
def update_summary_on_save(sender, instance, created, **kwargs):
    """
    Update weekly summary when a visit is created or updated.
    """
    if instance.clock_in:
        update_weekly_summary(instance.caregiver, instance.clock_in.date())
    
    # If the date changed, we might need to update the old week too, 
    # but for now we assume visits don't move across weeks often.

@receiver(post_delete, sender=Visit)
def update_summary_on_delete(sender, instance, **kwargs):
    """
    Update weekly summary when a visit is deleted.
    """
    if instance.clock_in:
        update_weekly_summary(instance.caregiver, instance.clock_in.date())
