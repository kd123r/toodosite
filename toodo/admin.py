from django.contrib import admin
from .models import PrivateTodo, PublicTodo, Upvote, Follower, Notification
# Register your models here.

admin.site.register(PrivateTodo)
admin.site.register(PublicTodo)
admin.site.register(Upvote)
admin.site.register(Follower)
admin.site.register(Notification)
