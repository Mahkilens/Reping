"""
Reping - Admin Configuration
----------------------------

Phase: Backend Foundation (State 1)

Purpose:
- Register core workout models with Django Admin.
- Enable CRUD operations (Create, Read, Update, Delete) 
  for Exercise, WorkoutSession, and SetEntry.

Why this matters:
- Allows manual creation and inspection of database records.
- Speeds up backend testing before building user-facing UI.
- Confirms that model relationships work correctly.

Models Registered:
- Exercise
- WorkoutSession
- SetEntry
"""

from django.contrib import admin
from .models import Exercise, WorkoutSession, SetEntry, Profile


# Register your models here.
admin.site.register(Exercise)
admin.site.register(WorkoutSession)
admin.site.register(SetEntry)
admin.site.register(Profile)