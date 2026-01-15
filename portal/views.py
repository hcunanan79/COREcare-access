from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect to 'next' if it exists, otherwise dashboard
            next_url = request.GET.get("next") or "/portal/dashboard/"
            return redirect(next_url)

        return render(
            request,
            "portal/login.html",
            {"error": "Invalid login"}
        )

    return render(request, "portal/login.html")


def portal_home(request):
    # Simple landing page (adjust if you already have a template)
    return render(request, "portal/portal_home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/portal/dashboard/")
    else:
        form = SignUpForm()

    return render(request, "portal/signup.html", {"form": form})


@login_required
def employee_dashboard(request):
    from shifts.models import Shift
    shifts = Shift.objects.filter(caregiver=request.user).order_by('start_time')
    return render(request, "portal/employee_dashboard.html", {"shifts": shifts})
