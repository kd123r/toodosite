from django.urls import path

from . import views

app_name = 'toodo'
urlpatterns = [
    path("", views.index, name="index"),
    path("private/", views.private, name="private"),
    path("private/update/<int:todo_id>/", views.private_update, name="private_update"),
]