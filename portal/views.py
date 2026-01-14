from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def portal_home(request):
    # Simple landing page (adjust if you already have a template)
    return render(request, "portal/portal_home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/portal/dashboard/")
    else:
        form = UserCreationForm()

    return render(request, "portal/signup.html", {"form": form})


@login_required
def employee_dashboard(request):
    return render(request, "portal/employee_dashboard.html")
