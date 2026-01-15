import csv
from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django_ratelimit.decorators import ratelimit

from clients.models import Client
from caregiver_portal.models import Visit, VisitComment
from shifts.models import Shift


@login_required
def employee_dashboard(request):
    """Unified dashboard showing shifts, clock-in/out actions, and weekly summary."""
    today = timezone.localdate()
    caregiver = request.user
    
    # Today's shifts
    todays_shifts = Shift.objects.filter(
        caregiver=caregiver,
        start_time__date=today
    ).select_related('client').order_by('start_time')
    
    # Active visit (currently clocked in)
    active_visit = Visit.objects.filter(
        caregiver=caregiver,
        clock_out__isnull=True
    ).select_related('client', 'shift').first()
    
    # Upcoming shifts (next 7 days)
    upcoming_shifts = Shift.objects.filter(
        caregiver=caregiver,
        start_time__date__gt=today,
        start_time__date__lte=today + timedelta(days=7)
    ).select_related('client').order_by('start_time')[:10]
    
    # Weekly hours summary
    start_of_week = today - timedelta(days=today.weekday())
    weekly_hours = Visit.objects.filter(
        caregiver=caregiver,
        clock_in__date__gte=start_of_week,
        duration_hours__isnull=False
    ).aggregate(total=Sum('duration_hours'))['total'] or 0
    
    context = {
        'todays_shifts': todays_shifts,
        'active_visit': active_visit,
        'upcoming_shifts': upcoming_shifts,
        'weekly_hours': round(float(weekly_hours), 2),
    }
    
    return render(request, 'caregiver_portal/employee_dashboard.html', context)


@login_required
@ratelimit(key='user', rate='10/h', method='POST', block=True)
def clock_in_shift(request, shift_id):
    """Clock in to a scheduled shift."""
    shift = get_object_or_404(Shift, id=shift_id)
    
    # SECURITY: Verify logged-in user is assigned to this shift
    if shift.caregiver != request.user:
        raise PermissionDenied("You cannot clock into a shift assigned to another caregiver.")
    
    # Check if already clocked in somewhere
    active_visit = Visit.objects.filter(caregiver=request.user, clock_out__isnull=True).first()
    if active_visit:
        messages.warning(request, "You are already clocked into another visit. Please clock out first.")
        return redirect('clock_out', visit_id=active_visit.id)
    
    # Create visit linked to shift
    visit = Visit.objects.create(
        shift=shift,
        caregiver=request.user,
        client=shift.client,
        clock_in=timezone.now(),
    )
    
    messages.success(request, f"Clocked in to {shift.client} at {visit.clock_in.strftime('%I:%M %p')}")
    return redirect('clock_out', visit_id=visit.id)


def client_profile(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, "caregiver_portal/client_profile.html", {"client": client})


def is_admin(user):
    return user.is_staff


def parse_date(value):
    """
    Expects value like '2026-01-08' from <input type="date">.
    Returns a python date object or None.
    """
    if not value:
        return None
    try:
        return timezone.datetime.fromisoformat(value).date()
    except Exception:
        return None


@login_required
def clock_page(request):
    clients = Client.objects.all()

    if request.method == "POST":
        client_id = request.POST.get("client")
        notes = request.POST.get("notes", "")

        client = get_object_or_404(Client, id=client_id)

        visit = Visit.objects.create(
            client=client,
            caregiver=request.user,
            clock_in=timezone.now(),
            notes=notes,
        )

        return redirect("clock_out", visit_id=visit.id)

    return render(
        request,
        "caregiver/clock_in.html",
        {
            "clients": clients,
            "caregiver_name": request.user.get_username(),
        },
    )


@login_required
def clock_out(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id, caregiver=request.user)
    comments = visit.comments.all()

    if request.method == "POST":
        # Handle mileage
        mileage = request.POST.get("mileage")
        if mileage:
            try:
                visit.mileage = Decimal(mileage)
            except Exception:
                pass

        # Clock out
        visit.clock_out = timezone.now()

        if visit.clock_in:
            duration = visit.clock_out - visit.clock_in
            hours = round(duration.total_seconds() / 3600, 2)
            visit.duration_hours = Decimal(str(hours))

        visit.save()
        return redirect("weekly_summary")

    return render(
        request,
        "caregiver/clock_out.html",
        {
            "visit": visit,
            "comments": comments,
        },
    )


@login_required
def add_comment(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id, caregiver=request.user)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            VisitComment.objects.create(
                visit=visit,
                author=request.user,
                text=text,
            )

    return redirect("clock_out", visit_id=visit.id)


@login_required
def add_mileage(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id, caregiver=request.user)

    if request.method == "POST":
        mileage = request.POST.get("mileage", "").strip()
        if mileage:
            try:
                visit.mileage = Decimal(mileage)
                visit.save()
            except Exception:
                pass

    return redirect("clock_out", visit_id=visit.id)


@login_required
def weekly_summary(request):
    today = timezone.localdate()

    # Monday -> Sunday
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    visits = Visit.objects.filter(
        caregiver=request.user,
        clock_in__date__range=[start_of_week, end_of_week],
        duration_hours__isnull=False,
    ).order_by("clock_in")

    total_hours = visits.aggregate(total=Sum("duration_hours"))["total"] or 0

    return render(
        request,
        "caregiver/weekly_summary.html",
        {
            "start": start_of_week,
            "end": end_of_week,
            "total_hours": round(float(total_hours), 2),
            "visits": visits,
        },
    )


@user_passes_test(is_admin)
def admin_payroll(request):
    today = timezone.localdate()

    default_start = today - timedelta(days=today.weekday())
    default_end = default_start + timedelta(days=6)

    start_param = request.GET.get("start")
    end_param = request.GET.get("end")

    start_date = parse_date(start_param) or default_start
    end_date = parse_date(end_param) or default_end

    shift = request.GET.get("shift")
    if shift == "prev":
        start_date = start_date - timedelta(days=7)
        end_date = end_date - timedelta(days=7)
    elif shift == "next":
        start_date = start_date + timedelta(days=7)
        end_date = end_date + timedelta(days=7)

    User = get_user_model()

    caregivers = User.objects.filter(
        is_active=True,
        groups__name="Caregiver"
    ).order_by("username")

    rows = []
    for cg in caregivers:
        total = (
            Visit.objects.filter(
                caregiver=cg,
                clock_in__date__range=[start_date, end_date],
                duration_hours__isnull=False,
            )
            .aggregate(total=Sum("duration_hours"))["total"]
            or 0
        )

        rows.append(
            {
                "caregiver": cg,
                "total_hours": round(float(total), 2),
            }
        )

    return render(
        request,
        "caregiver/admin_payroll.html",
        {
            "start": start_date,
            "end": end_date,
            "rows": rows,
        },
    )


@user_passes_test(is_admin)
def admin_payroll_csv(request):
    today = timezone.localdate()

    default_start = today - timedelta(days=today.weekday())
    default_end = default_start + timedelta(days=6)

    start_param = request.GET.get("start")
    end_param = request.GET.get("end")

    start_date = parse_date(start_param) or default_start
    end_date = parse_date(end_param) or default_end

    User = get_user_model()
    caregivers = User.objects.filter(is_active=True, is_staff=True).order_by("username")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="payroll_{start_date}_to_{end_date}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Caregiver", "Total Hours", "Start Date", "End Date"])

    for cg in caregivers:
        total = (
            Visit.objects.filter(
                caregiver=cg,
                clock_in__date__range=[start_date, end_date],
                duration_hours__isnull=False,
            )
            .aggregate(total=Sum("duration_hours"))["total"]
            or 0
        )

        writer.writerow([cg.username, round(float(total), 2), start_date, end_date])

    return response
