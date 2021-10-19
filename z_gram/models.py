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
    profile_picture = models.ImageField(upload_to='images/profile/', default='images/profile/user.png')
    location = models.CharField(max_length=70, blank=True, null=True)

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """
        receives signal once user model is saved, if user was created we create a UserProfile instance
        """
        if created:
            UserProfile.objects.create(user=instance)

    @staticmethod
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        # instance.save()
        pass

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


class UserPost(models.Model):
    """
    model for post by User
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='userposts')
    image = models.ImageField(upload_to='images/posts/')
    caption = models.CharField(max_length=250, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    name = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

    @property
    def get_all_comments(self):
        return self.comments.all()

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.username} Post'


class UserComment(models.Model):
    """
    model for the user comments in relation to User and Posts
    """
    comment = models.TextField()
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f'{self.user.username} Post'


class Follow(models.Model):
    """
    model for User followers and User following
    """
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'
