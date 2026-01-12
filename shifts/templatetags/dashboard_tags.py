from datetime import timedelta
from django import template
from django.utils import timezone

from shifts.models import Shift  # <-- your Shift model

register = template.Library()

@register.simple_tag
def upcoming_shifts(days=7):
    now = timezone.now()
    end = now + timedelta(days=days)

    # IMPORTANT: change start_time/end_time to your real field names if different
    return Shift.objects.filter(
        start_time__gte=now,
        start_time__lte=end,
    ).order_by("start_time")
