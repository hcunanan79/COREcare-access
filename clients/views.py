"""
Issue #40: Client Calendar Views
Provides calendar view and event management for family members.
"""
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

from .models import Client, ClientFamilyMember, ClientCalendarEvent, EventAttachment
from .services import CalendarService


def schedule(request):
    """Legacy schedule view - redirects to calendar if authenticated."""
    if request.user.is_authenticated:
        # Check if user has any linked clients
        links = ClientFamilyMember.objects.filter(user=request.user)
        if links.exists():
            return redirect('family_home')
    return render(request, "clients/schedule.html")


def _check_client_access(user, client_id, require_schedule_view=True):
    """
    Verify user has access to a client's calendar.
    Returns the ClientFamilyMember link if authorized, raises PermissionDenied otherwise.
    """
    try:
        link = ClientFamilyMember.objects.get(client_id=client_id, user=user)
        if require_schedule_view and not link.can_view_schedule:
            raise PermissionDenied("You do not have permission to view this schedule.")
        return link
    except ClientFamilyMember.DoesNotExist:
        # Also allow staff/admin access
        if user.is_staff or user.is_superuser:
            return None  # Staff can access without a link
        raise PermissionDenied("You do not have access to this client's calendar.")


@login_required
def client_calendar(request, client_id):
    """
    Issue #40: Unified client calendar view.
    Displays shifts and events in a combined calendar/list view.
    """
    link = _check_client_access(request.user, client_id)
    client = get_object_or_404(Client, id=client_id)
    
    # Parse date range from query params
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    try:
        start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    except ValueError:
        start_date = None
    
    try:
        end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    except ValueError:
        end_date = None
    
    # Get unified schedule
    schedule = CalendarService.get_client_schedule(client_id, start_date, end_date)
    
    # Group by date for list view
    schedule_by_date = {}
    for item in schedule:
        date_key = item['start_time'].date()
        if date_key not in schedule_by_date:
            schedule_by_date[date_key] = []
        schedule_by_date[date_key].append(item)
    
    # Sort dates
    sorted_dates = sorted(schedule_by_date.keys())
    
    context = {
        'client': client,
        'link': link,
        'schedule': schedule,
        'schedule_by_date': [(date, schedule_by_date[date]) for date in sorted_dates],
        'today': timezone.localdate(),
        'start_date': start_date or timezone.localdate(),
        'end_date': end_date or (timezone.localdate() + timedelta(days=30)),
        'can_add_events': link is not None or request.user.is_staff,
    }
    
    return render(request, 'clients/client_calendar.html', context)


@login_required
def create_event(request, client_id):
    """
    Issue #40: Create a new calendar event.
    SECURITY: Validates ClientFamilyMember link before allowing creation.
    """
    link = _check_client_access(request.user, client_id)
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        # Parse form data
        title = request.POST.get('title', '').strip()
        event_type = request.POST.get('event_type', 'other')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location', '').strip()
        description = request.POST.get('description', '').strip()
        
        # Validation
        errors = []
        if not title:
            errors.append("Title is required.")
        
        try:
            start_datetime = timezone.datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
            start_datetime = timezone.make_aware(start_datetime)
        except (ValueError, TypeError):
            errors.append("Invalid start date/time.")
            start_datetime = None
        
        try:
            end_datetime = timezone.datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
            end_datetime = timezone.make_aware(end_datetime)
        except (ValueError, TypeError):
            errors.append("Invalid end date/time.")
            end_datetime = None
        
        if start_datetime and end_datetime and end_datetime <= start_datetime:
            errors.append("End time must be after start time.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'clients/event_form.html', {
                'client': client,
                'link': link,
                'form_data': request.POST,
                'event_types': ClientCalendarEvent.EventType.choices,
                'is_edit': False,
            })
        
        # Create event
        event = ClientCalendarEvent.objects.create(
            client=client,
            title=title,
            event_type=event_type,
            start_time=start_datetime,
            end_time=end_datetime,
            location=location,
            description=description,
            created_by=request.user,
        )
        
        messages.success(request, f"Event '{title}' created successfully.")
        return redirect('client_calendar', client_id=client_id)
    
    # GET request - show form
    context = {
        'client': client,
        'link': link,
        'event_types': ClientCalendarEvent.EventType.choices,
        'is_edit': False,
        'default_date': timezone.localdate().isoformat(),
    }
    return render(request, 'clients/event_form.html', context)


@login_required
def edit_event(request, client_id, event_id):
    """
    Issue #40: Edit an existing calendar event.
    SECURITY: Validates ClientFamilyMember link before allowing edit.
    """
    link = _check_client_access(request.user, client_id)
    client = get_object_or_404(Client, id=client_id)
    event = get_object_or_404(ClientCalendarEvent.all_objects, id=event_id, client_id=client_id)
    
    if request.method == 'POST':
        # Parse form data
        title = request.POST.get('title', '').strip()
        event_type = request.POST.get('event_type', 'other')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location', '').strip()
        description = request.POST.get('description', '').strip()
        
        # Validation
        errors = []
        if not title:
            errors.append("Title is required.")
        
        try:
            start_datetime = timezone.datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
            start_datetime = timezone.make_aware(start_datetime)
        except (ValueError, TypeError):
            errors.append("Invalid start date/time.")
            start_datetime = None
        
        try:
            end_datetime = timezone.datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
            end_datetime = timezone.make_aware(end_datetime)
        except (ValueError, TypeError):
            errors.append("Invalid end date/time.")
            end_datetime = None
        
        if start_datetime and end_datetime and end_datetime <= start_datetime:
            errors.append("End time must be after start time.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'clients/event_form.html', {
                'client': client,
                'link': link,
                'event': event,
                'form_data': request.POST,
                'event_types': ClientCalendarEvent.EventType.choices,
                'is_edit': True,
            })
        
        # Update event
        event.title = title
        event.event_type = event_type
        event.start_time = start_datetime
        event.end_time = end_datetime
        event.location = location
        event.description = description
        event.save()
        
        messages.success(request, f"Event '{title}' updated successfully.")
        return redirect('client_calendar', client_id=client_id)
    
    # GET request - show form with existing data
    context = {
        'client': client,
        'link': link,
        'event': event,
        'event_types': ClientCalendarEvent.EventType.choices,
        'is_edit': True,
    }
    return render(request, 'clients/event_form.html', context)


@login_required
def delete_event(request, client_id, event_id):
    """
    Issue #40: Soft-delete a calendar event.
    SECURITY: Validates ClientFamilyMember link before allowing delete.
    Supports both regular POST and AJAX requests.
    """
    link = _check_client_access(request.user, client_id)
    event = get_object_or_404(ClientCalendarEvent, id=event_id, client_id=client_id)
    
    if request.method == 'POST':
        event_title = event.title
        event.soft_delete()
        
        # Check if AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Event '{event_title}' deleted.",
                'event_id': event_id,
                'undo_url': f'/clients/{client_id}/events/{event_id}/restore/',
            })
        
        messages.success(request, f"Event '{event_title}' deleted.")
        return redirect('client_calendar', client_id=client_id)
    
    # GET request - show confirmation
    client = get_object_or_404(Client, id=client_id)
    context = {
        'client': client,
        'link': link,
        'event': event,
    }
    return render(request, 'clients/event_delete_confirm.html', context)


@login_required
def restore_event(request, client_id, event_id):
    """
    Issue #40: Restore a soft-deleted event (Undo feature).
    SECURITY: Validates ClientFamilyMember link before allowing restore.
    """
    link = _check_client_access(request.user, client_id)
    
    # Use all_objects to find soft-deleted events
    event = get_object_or_404(ClientCalendarEvent.all_objects, id=event_id, client_id=client_id)
    
    if request.method == 'POST':
        event.restore()
        
        # Check if AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Event '{event.title}' restored.",
                'event_id': event_id,
            })
        
        messages.success(request, f"Event '{event.title}' restored.")
        return redirect('client_calendar', client_id=client_id)
    
    # GET request - not supported, redirect
    return redirect('client_calendar', client_id=client_id)


@login_required
def calendar_api(request, client_id):
    """
    Issue #40: JSON API for calendar data.
    Used by JavaScript calendar widgets.
    """
    try:
        _check_client_access(request.user, client_id)
    except PermissionDenied:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')
    
    try:
        start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    except ValueError:
        start_date = None
    
    try:
        end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    except ValueError:
        end_date = None
    
    schedule = CalendarService.get_client_schedule(client_id, start_date, end_date)
    
    # Convert to JSON-serializable format
    events = []
    for item in schedule:
        events.append({
            'id': f"{item['type']}_{item['id']}",
            'title': f"{item['icon']} {item['title']}",
            'start': item['start_time'].isoformat(),
            'end': item['end_time'].isoformat(),
            'className': item['color_class'],
            'type': item['type'],
            'editable': item['type'] == 'event',
        })
    
    return JsonResponse(events, safe=False)


@login_required
def upload_attachment(request, client_id, event_id):
    """
    Issue #40: Upload file attachment to an event.
    SECURITY: Validates ClientFamilyMember link before allowing upload.
    """
    link = _check_client_access(request.user, client_id)
    event = get_object_or_404(ClientCalendarEvent, id=event_id, client_id=client_id)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    files = request.FILES.getlist('files')
    if not files:
        return JsonResponse({'error': 'No files provided'}, status=400)
    
    # Allowed file types (security)
    ALLOWED_EXTENSIONS = {
        'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'jpg', 'jpeg', 'png', 'gif', 'webp',
        'mp3', 'wav', 'm4a',
        'mp4', 'mov', 'avi',
        'txt', 'csv', 'zip'
    }
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    uploaded = []
    errors = []
    
    for file in files:
        # Check file size
        if file.size > MAX_FILE_SIZE:
            errors.append(f"{file.name}: File too large (max 50MB)")
            continue
        
        # Check extension
        ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
        if ext not in ALLOWED_EXTENSIONS:
            errors.append(f"{file.name}: File type not allowed")
            continue
        
        # Create attachment
        attachment = EventAttachment(
            event=event,
            file=file,
            original_filename=file.name,
            file_size=file.size,
            content_type=file.content_type or '',
            uploaded_by=request.user
        )
        attachment.save()
        
        uploaded.append({
            'id': attachment.id,
            'name': attachment.original_filename,
            'size': attachment.human_file_size,
            'icon': attachment.file_icon,
            'url': attachment.file.url,
            'is_image': attachment.is_image,
            'delete_url': f'/clients/{client_id}/events/{event_id}/attachments/{attachment.id}/delete/',
        })
    
    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'errors': errors,
    })


@login_required
def delete_attachment(request, client_id, event_id, attachment_id):
    """
    Issue #40: Delete a file attachment.
    SECURITY: Validates ClientFamilyMember link before allowing delete.
    """
    link = _check_client_access(request.user, client_id)
    event = get_object_or_404(ClientCalendarEvent, id=event_id, client_id=client_id)
    attachment = get_object_or_404(EventAttachment, id=attachment_id, event=event)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    filename = attachment.original_filename
    
    # Delete the file from storage
    if attachment.file:
        attachment.file.delete(save=False)
    
    # Delete the database record
    attachment.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"'{filename}' deleted.",
        })
    
    messages.success(request, f"Attachment '{filename}' deleted.")
    return redirect('edit_event', client_id=client_id, event_id=event_id)


