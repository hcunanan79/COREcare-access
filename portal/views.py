from django.shortcuts import render

def portal_home(request):
    return render(request, "portal/home.html")
