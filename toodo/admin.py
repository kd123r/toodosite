from django.contrib import admin
from .models import PrivateTodo, PublicTodo
# Register your models here.

admin.site.register(PrivateTodo)
admin.site.register(PublicTodo)
