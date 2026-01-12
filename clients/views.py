from django.shortcuts import render

def schedule(request):
    return render(request, "clients/schedule.html")
