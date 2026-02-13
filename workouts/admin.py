from django.contrib import admin
from .models import Exercise, WorkoutSession, SetEntry

# Register your models here.
admin.site.register(Exercise)
admin.site.register(WorkoutSession)
admin.site.register(SetEntry)