from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("checkin/", views.checkin_create, name="checkin_create"),
    path("logs/", views.logs, name="logs"),
    path("exercises/", views.exercises, name="exercises"),
    path("progress/", views.progress, name="progress"),
    path("settings/", views.settings, name="settings"),
    path("nutrition/", views.nutrition, name="nutrition"),
    path("hydration/", views.hydration, name="hydration"),
    path("streak/", views.streak, name="streak"),
    path("analytics/", views.analytics, name="analytics"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("accounts/", include("allauth.urls")),
]
