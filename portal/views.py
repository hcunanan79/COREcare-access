from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


def logout_view(request):
    logout(request)
    return redirect("/portal/login/")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            
            # Smart Redirect Logic
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            
            # Check if user is a Family Member
            from clients.models import ClientFamilyMember
            if ClientFamilyMember.objects.filter(user=user).exists():
                return redirect("family_home")
                
            # Default to Employee/Caregiver Dashboard
            return redirect("employee_dashboard")

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
    from django.utils import timezone

    shifts = Shift.objects.filter(caregiver=request.user).order_by('start_time')
    today = timezone.now().date()
    return render(request, "portal/employee_dashboard.html", {"shifts": shifts, "today": today})


def offline_view(request):
    """Fallback page for offline PWA requests"""
    return render(request, "offline.html")


@login_required
def family_home(request):
    """
    Issue #22: Family Portal Home.
    Lists all clients linked to the logged-in user.
    """
    from clients.models import ClientFamilyMember
    
    links = ClientFamilyMember.objects.filter(user=request.user).select_related('client')
    
    context = {
        'links': links,
    }
    return render(request, 'portal/family_home.html', context)


@login_required
def family_client_detail(request, client_id):
    """
    Issue #22: View client schedule and messages.
    """
    from django.shortcuts import get_object_or_404
    from clients.models import ClientFamilyMember, ClientMessage
    from shifts.models import Shift
    from django.utils import timezone
    from django.core.exceptions import PermissionDenied
    
    # Verify access
    link = get_object_or_404(ClientFamilyMember, client_id=client_id, user=request.user)
    
    if request.method == "POST":
        if not link.can_message_caregivers:
            raise PermissionDenied("You do not have permission to post messages.")
            
        content = request.POST.get('content')
        if content:
            ClientMessage.objects.create(
                client_id=client_id,
                author=request.user,
                content=content
            )
        return redirect('family_client_detail', client_id=client_id)

    # Fetch simple schedule (next 14 days)
    today = timezone.now().date()
    upcoming_shifts = []
    if link.can_view_schedule:
        upcoming_shifts = Shift.objects.filter(
            client_id=client_id,
            start_time__date__gte=today
        ).order_by('start_time')[:10]
        
    messages = ClientMessage.objects.filter(client_id=client_id).select_related('author')[:50]
    
    context = {
        'link': link,
        'client': link.client,
        'upcoming_shifts': upcoming_shifts,
        'messages': messages,
    }
    return render(request, 'portal/family_client_detail.html', context)
