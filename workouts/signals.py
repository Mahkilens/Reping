from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

print("✅ workouts.signals imported; User model =", User)

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    print("🔥 post_save hit:", instance.username, "created=", created)

    if created:
        Profile.objects.create(user=instance)
        print("✅ profile created for:", instance.username)
