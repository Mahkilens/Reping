from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone

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

    xp_next_level = profile.level * 100
    xp_progress_percent = min(int((profile.xp / xp_next_level) * 100), 100) if xp_next_level else 0

    return render(
        request,
        "workouts/dashboard.html",
        {
            "profile": profile,
            "recent_sessions": recent_sessions,
            "today_checkins_count": today_checkins_count,
            "week_checkins_count": week_checkins_count,
            "xp_next_level": xp_next_level,
            "xp_progress_percent": xp_progress_percent,
        }
    )


def home(request):
    return redirect("dashboard")


@login_required
def logs(request):
    return render(request, "workouts/logs.html")


@login_required
def exercises(request):
    return render(request, "workouts/exercises.html")


@login_required
def progress(request):
    return render(request, "workouts/progress.html")


@login_required
def settings(request):
    return render(request, "workouts/settings.html")


@login_required
def nutrition(request):
    return render(request, "workouts/nutrition.html")


@login_required
def hydration(request):
    return render(request, "workouts/hydration.html")


@login_required
def streak(request):
    return render(request, "workouts/streak.html")


@login_required
def analytics(request):
    return render(request, "workouts/analytics.html")

@login_required
def leaderboard(request):
    return render(request, "workouts/leaderboard.html")

@login_required 
def checkin_create(request):
    if request.method != "POST":
        return redirect("dashboard")

    profile, _ = Profile.objects.get_or_create(user=request.user)
    gym = Gym.objects.first()

    if gym is None:
        return redirect("dashboard")

    # Check in once per day (guard)
    today = timezone.localdate()
    already_checked_in = CheckIn.objects.filter(
        profile=profile,
        timestamp__date=today
    ).exists()

    if already_checked_in:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "reason": "already_checked_in_today"})
        return redirect("dashboard")

    # Create check-in
    CheckIn.objects.create(profile=profile, gym=gym)

    # Calculation for clients xp gain/control (reset-style leveling)
    profile.xp += 20
    while profile.xp >= profile.level * 100:
        threshold = profile.level * 100
        profile.xp -= threshold
        profile.level += 1
    profile.save()

    # AJAX response
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        xp_next_level = profile.level * 100
        xp_progress_percent = min(
            int((profile.xp / xp_next_level) * 100), 100
        ) if xp_next_level else 0

        return JsonResponse({
            "ok": True,
            "level": profile.level,
            "xp": profile.xp,
            "xp_next_level": xp_next_level,
            "xp_progress_percent": xp_progress_percent,
        })

    return redirect("dashboard")