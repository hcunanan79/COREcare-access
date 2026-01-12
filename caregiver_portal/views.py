import csv
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from clients.models import Client
from caregiver_portal.models import Visit

from django.shortcuts import get_object_or_404, render
from clients.models import Client

def client_profile(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, "caregiver_portal/client_profile.html", {"client": client})


def is_admin(user):
    return user.is_staff  # you can change to user.is_superuser if you want


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

        # If you already have a different flow for clocking out, you can change this redirect.
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

    if request.method == "POST":
        visit.clock_out = timezone.now()

        if visit.clock_in:
            duration = visit.clock_out - visit.clock_in
            hours = round(duration.total_seconds() / 3600, 2)
            visit.duration_hours = Decimal(str(hours))

        visit.save()
        return render(request, "caregiver/clock_out.html", {"visit": visit})

    # If they open the clock-out page, show the details and a button to clock out.
    return render(request, "caregiver/clock_out.html", {"visit": visit})


@login_required
def weekly_summary(request):
    today = timezone.localdate()

    # Monday -> Sunday
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)          # Sunday

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

    default_start = today - timedelta(days=today.weekday())  # Monday
    default_end = default_start + timedelta(days=6)          # Sunday

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

    # (keeping your current rule: staff users are caregivers)
    caregivers = User.objects.filter(is_active=True, groups__name="Caregiver"
).order_by("username")

    rows = []
    for cg in caregivers:
        total = (
            Visit.objects.filter(
                caregiver_name=cg.username,
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

    default_start = today - timedelta(days=today.weekday())  # Monday
    default_end = default_start + timedelta(days=6)          # Sunday

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
