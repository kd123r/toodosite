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

class Upvote(models.Model):
    public_todo = models.ForeignKey(
        PublicTodo, 
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

class Follower(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )

class Notification(models.Model):
    class Action(models.IntegerChoices):
        UPVOTE = 1
        FOLLOW = 2
    action = models.IntegerField(choices=Action.choices)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    timestamp = models.DateTimeField()
