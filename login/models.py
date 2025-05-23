from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    ROLE_CHOICES = [
        ("patron", "Patron"),
        ("librarian", "Librarian"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)  # Allows user selection
    is_setup = models.BooleanField(default=False)  # Tracks if the user has chosen a role
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.role if self.role else 'No Role Selected'}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"
    
# Signal to automatically create Profile when a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role="patron", is_setup=True)
