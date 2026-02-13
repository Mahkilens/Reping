from django.db import models 

# Create your models here.
class Exercise(models.Model):
    # Name of the exercise (e.g., Bench Press)
    name = models.CharField(max_length=100)

    # Optional muscle group classification
    muscle_group = models.CharField(max_length=100, blank=True)

    # String representation shown in admin
    def __str__(self):
        return self.name

# WorkoutSession = 
class WorkoutSession(models.Model):
    # Date of the workout session
    date = models.DateField()

    # Optional notes for that workout
    notes = models.TextField(blank=True)

    # Display format in admin panel
    def __str__(self):
        return f"Workout on {self.date}"


class SetEntry(models.Model):
    # Each set belongs to ONE workout session.
    # If the session is deleted, all its sets are deleted too (CASCADE).
    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name="sets"  # allows: workout_session.sets.all()
    )

    # Each set is for ONE specific exercise.
    # Example: Bench Press, Squat, Deadlift.
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="sets"  # allows: exercise.sets.all()
    )

    # Optional set number (Set 1, Set 2, etc.)
    # blank=True = optional in forms
    # null=True = database can store NULL
    set_number = models.IntegerField(blank=True, null=True)

    # Required number of repetitions performed in this set.
    reps = models.IntegerField()

    # Weight used for this set.
    # max_digits = total digits allowed
    # decimal_places = digits after decimal
    # Example: 135.00
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    # Controls how this object appears in Django admin and when printed.
    def __str__(self):
        set_part = f"Set {self.set_number} " if self.set_number is not None else ""
        return f"{set_part}{self.exercise.name}: {self.weight} x {self.reps}"


