from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    model for the user including related methods
    """
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    username = models.TextField(max_length=150)
    bio = models.CharField(max_length=400, blank=True, null=True, default="simple bio")
    profile_picture = models.ImageField(upload_to='images/profile', default='user.png')
    location = models.CharField(max_length=70, blank=True, null=True)

    @classmethod
    @receiver(post_save, sender=User)
    def create_user_profile(cls, sender, instance, created, **kwargs):
        """
        receives signal once user model is saved, if user was created we create a UserProfile instance
        """
        if created:
            cls.objects.create(user=instance)

    @staticmethod
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return f'{self.user.username}: profile'

    @classmethod
    def search_profile(cls, search_term):
        """
        method to search for users
        """
        return cls.objects.filter(user__username__icontains=search_term).all()


