from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    """
    This model represents a post.
    """
    description = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, related_name="posts")
    likes = models.ManyToManyField(get_user_model(), related_name="liked_posts", blank=True)
    saves = models.ManyToManyField(get_user_model(), related_name="saved_posts", blank=True)
    mentions = models.ManyToManyField(get_user_model(), related_name="mentioned", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.modified_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.username} post ({self.id})"


class PostPhoto(models.Model):
    """
    This model represents a post photo.
    Having it as a separate model allows
    one post to have more than one photo.
    """
    photo = models.ImageField(upload_to="post_pics/")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="photos")


class Comment(models.Model):
    """
    This model represents a comment.
    """
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    reply_to = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="replies")
    likes = models.ManyToManyField(get_user_model(), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.modified_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.username}: {self.text[:10]}..."
