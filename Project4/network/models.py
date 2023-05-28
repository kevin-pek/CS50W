from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class UserFollowing(models.Model):
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE, related_name="followers")
    follower_user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE, related_name="following")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower_user')

class Like(models.Model):
    post = models.ForeignKey("Post", blank=True, null=True, on_delete=models.CASCADE, related_name="likes")
    like_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="liked_posts")

    class Meta:
        unique_together = ('post', 'like_user')



class Post(models.Model):
    content = models.TextField(max_length=500)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    def get_likes(self):
        return self.likes.all()
        
    def __str__(self):
        return "Post created by " + str(self.user.username)

    def serialise(self):
        return {
            "id": self.id,
            "user": self.user,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
            "content": self.content
        }
