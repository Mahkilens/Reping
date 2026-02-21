from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Profile, Gym, CheckIn


@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    recent_sessions = profile.sessions.order_by("-date")[:5]

    # today logic
    today = date.today()
    today_checkins_count = CheckIn.objects.filter(
        profile=profile,
        timestamp__date=today
    ).count()

    # week logic (Monday -> today)
    start_of_week = today - timedelta(days=today.weekday())
    week_checkins_count = CheckIn.objects.filter(
        profile=profile,
        timestamp__date__gte=start_of_week,
        timestamp__date__lte=today
    ).count()

    return render(
        request,
        "workouts/dashboard.html",
        {
            "profile": profile,
            "recent_sessions": recent_sessions,
            "today_checkins_count": today_checkins_count,
            "week_checkins_count": week_checkins_count,
        }
    )


def home(request):
    return redirect("dashboard")


@login_required
def checkin_create(request):
    if request.method != "POST":
        return redirect("dashboard")

    profile, _ = Profile.objects.get_or_create(user=request.user)
    gym = Gym.objects.first()

    if gym is None:
        return redirect("dashboard")

    CheckIn.objects.create(profile=profile, gym=gym)
    return redirect("dashboard")