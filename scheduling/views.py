from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def timeclock_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("timeclock_home")

        return render(request, "timeclock/login.html", {"error": "Invalid login"})

    return render(request, "timeclock/login.html")


@login_required(login_url="/timeclock/login/")
def timeclock_home(request):
    return render(request, "timeclock/home.html")