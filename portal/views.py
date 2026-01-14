import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

@login_required
def employee_dashboard(request):
    return render(request, "portal/employee_dashboard.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["invite_code"] != os.environ.get("EMPLOYEE_INVITE_CODE", ""):
                form.add_error("invite_code", "Invalid invite code.")
            else:
                User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                )
                messages.success(request, "Account created. Please log in.")
                return redirect("/admin/")
    else:
        form = SignUpForm()

    return render(request, "portal/signup.html", {"form": form})

def portal_home(request):
    return render(request, "portal/signup.html")
from django.contrib.auth.decorators import login_required

@login_required
def employee_dashboard(request):
    return render(request, "portal/employee_dashboard.html")
