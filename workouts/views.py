from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Profile

@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    recent_sessions = profile.sessions.order_by("-date")[:5]
    return render(request, "workouts/dashboard.html", {"profile": profile, "recent_sessions": recent_sessions})

def home(request):
    return redirect("dashboard")
