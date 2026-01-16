from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from .models import Visit, WeeklySummary

def update_weekly_summary(caregiver, date):
    """
    Recalculates and saves the WeeklySummary for a given caregiver and date.
    Finds the Monday of the week for the given date and re-aggregates all visits.
    """
    if not caregiver or not date:
        return

    # Find start of week (Monday)
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Aggregate all visits for this week
    visits = Visit.objects.filter(
        caregiver=caregiver,
        clock_in__date__range=[start_of_week, end_of_week],
        duration_hours__isnull=False
    )
    
    agg = visits.aggregate(
        total_hours=Sum('duration_hours')
    )
    
    total_hours = agg['total_hours'] or 0
    total_visits = visits.count()
    
    # Update or create summary record
    WeeklySummary.objects.update_or_create(
        caregiver=caregiver,
        week_start=start_of_week,
        defaults={
            'total_hours': total_hours,
            'total_visits': total_visits,
        }
    )
