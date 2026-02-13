from django.db import models 

# Create your models here.
# Excercise = 
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

# WorkoutSession = 
class WorkoutSession(models.Model):
    date = models.DateField()
    notes = models.TextField(blank=True)

    # Returning a string: __str__, special python operation: When this object is converted to text, what should it look like?
    def __str__(self):
        return f"workout on {self.date}"

# SetEntry = 
class SetEntry(models.Model):
    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name="sets"
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="sets"
    )
    set_number = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        set_part = f"Set {self.set_number} " if self.set_number is not None else ""
        return f"{set_part}{self.exercise.name}: {self.weight} x {self.reps}"

