from django.db import models
from django.conf import settings

class PrivateTodo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    todo_text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    pub_date = models.DateTimeField()

class PublicTodo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    todo_text = models.CharField(max_length=200)
    upvotes = models.IntegerField(default=0)
    pub_date = models.DateTimeField()