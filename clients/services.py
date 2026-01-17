"""
Issue #40: Calendar Service Layer
Provides a unified interface for fetching client schedules (shifts + events).
"""
from datetime import timedelta
from django.utils import timezone


class CalendarService:
    """
    Service layer for client calendar operations.
    Returns merged, sorted lists of Shifts and ClientCalendarEvents.
    """
    
    @staticmethod
    def get_client_schedule(client_id, start_date=None, end_date=None, include_shifts=True, include_events=True):
        """
        Fetch a unified schedule for a client within a date range.
        
        Args:
            client_id: The client's ID
            start_date: Start of date range (default: today)
            end_date: End of date range (default: today + 30 days)
            include_shifts: Include caregiver shifts (default: True)
            include_events: Include calendar events (default: True)
        
        Returns:
            List of dicts with unified schema:
            [
                {
                    'type': 'shift' | 'event',
                    'id': int,
                    'title': str,
                    'start_time': datetime,
                    'end_time': datetime,
                    'location': str (optional),
                    'icon': str (emoji),
                    'color_class': str (CSS class),
                    'details': dict (type-specific extra data),
                }
            ]
        """
        from shifts.models import Shift
        from clients.models import ClientCalendarEvent
        
        # Default date range: today to 30 days from now
        if start_date is None:
            start_date = timezone.now().date()
        if end_date is None:
            end_date = start_date + timedelta(days=30)
        
        schedule = []
        
        # Fetch shifts
        if include_shifts:
            shifts = Shift.objects.filter(
                client_id=client_id,
                start_time__date__gte=start_date,
                start_time__date__lte=end_date
            ).select_related('caregiver').order_by('start_time')
            
            for shift in shifts:
                schedule.append({
                    'type': 'shift',
                    'id': shift.id,
                    'title': f"Caregiver: {shift.caregiver.first_name} {shift.caregiver.last_name[:1] if shift.caregiver.last_name else ''}.",
                    'start_time': shift.start_time,
                    'end_time': shift.end_time,
                    'location': '',
                    'icon': '👤',
                    'color_class': 'schedule-item-shift',
                    'details': {
                        'caregiver_id': shift.caregiver.id,
                        'caregiver_name': f"{shift.caregiver.first_name} {shift.caregiver.last_name}",
                    }
                })
        
        # Fetch events (soft-deleted events are automatically filtered)
        if include_events:
            events = ClientCalendarEvent.objects.filter(
                client_id=client_id,
                start_time__date__gte=start_date,
                start_time__date__lte=end_date
            ).select_related('created_by').prefetch_related('attachments').order_by('start_time')
            
            for event in events:
                creator_name = ''
                if event.created_by:
                    creator_name = f"{event.created_by.first_name} {event.created_by.last_name}".strip()
                    if not creator_name:
                        creator_name = event.created_by.username
                
                schedule.append({
                    'type': 'event',
                    'id': event.id,
                    'title': event.title,
                    'start_time': event.start_time,
                    'end_time': event.end_time,
                    'location': event.location,
                    'icon': event.event_type_icon,
                    'color_class': f'schedule-item-event schedule-item-{event.event_type}',
                    'details': {
                        'event_type': event.event_type,
                        'event_type_display': event.get_event_type_display(),
                        'description': event.description,
                        'created_by': creator_name,
                        'created_at': event.created_at,
                        'attachment_count': event.attachments.count(),
                        'attachments': [{
                            'id': a.id,
                            'name': a.original_filename,
                            'url': a.file.url,
                            'icon': a.file_icon,
                            'size': a.human_file_size
                        } for a in event.attachments.all()]
                    }
                })
        
        # Sort by start_time
        schedule.sort(key=lambda x: x['start_time'])
        
        return schedule
    
    @staticmethod
    def get_events_for_client(client_id, start_date=None, end_date=None):
        """
        Fetch only calendar events (not shifts) for a client.
        Used when family members want to manage their own events.
        """
        return CalendarService.get_client_schedule(
            client_id, 
            start_date, 
            end_date, 
            include_shifts=False, 
            include_events=True
        )
    
    @staticmethod
    def check_conflicts(client_id, start_time, end_time, exclude_event_id=None):
        """
        Check if a proposed event conflicts with existing shifts or events.
        
        Returns:
            List of conflicting items (empty if no conflicts)
        """
        from shifts.models import Shift
        from clients.models import ClientCalendarEvent
        
        conflicts = []
        
        # Check shift conflicts
        conflicting_shifts = Shift.objects.filter(
            client_id=client_id,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        for shift in conflicting_shifts:
            conflicts.append({
                'type': 'shift',
                'title': f"Caregiver shift",
                'start_time': shift.start_time,
                'end_time': shift.end_time,
            })
        
        # Check event conflicts
        conflicting_events = ClientCalendarEvent.objects.filter(
            client_id=client_id,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if exclude_event_id:
            conflicting_events = conflicting_events.exclude(id=exclude_event_id)
        
        for event in conflicting_events:
            conflicts.append({
                'type': 'event',
                'title': event.title,
                'start_time': event.start_time,
                'end_time': event.end_time,
            })
        
        return conflicts
