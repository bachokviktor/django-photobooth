from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user model.

    Adds new fields: profile_pic, bio, following.
    """
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.CharField(max_length=150, blank=True, null=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)

    def follow(self, user):
        if user not in self.following.all() and user != self:
            self.following.add(user)

    def unfollow(self, user):
        if user in self.following.all() and user != self:
            self.following.remove(user)

    def remove_follower(self, user):
        if user in self.followers.all() and user != self:
            self.followers.remove(user)

    def __str__(self):
        return self.username
