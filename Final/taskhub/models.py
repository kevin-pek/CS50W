from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    task_views = ["All", "Completed", "Incomplete"]
    current_view = "All"

class Board(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE, related_name="boards")

#text note that can be added to boards
class Note(models.Model):
    content = models.CharField(max_length=300, default="")
    x_coord = models.IntegerField(default=0)
    y_coord = models.IntegerField(default=0)
    height = models.IntegerField(default=200)
    width = models.IntegerField(default=200)
    board = models.ForeignKey(Board, blank=True, null=True, on_delete=models.CASCADE, related_name="notes")

    def serialise(self):
        return {
            "id": self.pk,
            "content": self.content,
            "x_coord": self.x_coord,
            "y_coord": self.y_coord,
            "width": self.width,
            "height": self.height,
        }

#text completable note with possible deadlines and subtasks
class Task(models.Model):
    content = models.CharField(max_length=300)
    start = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=False)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="tasks")
    parent_task = models.ForeignKey("Task", blank=True, null=True, on_delete=models.CASCADE, related_name="subtasks")

    def serialise(self):
        return {
            "id": self.id,
            "content": self.content,
            "start": self.start,
            "deadline": self.deadline,
            "is_completed": self.is_completed,
            "parent_task": self.parent_task_id
        }
