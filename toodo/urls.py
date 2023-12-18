from django.urls import path

from . import views

app_name = 'toodo'
urlpatterns = [
    path("", views.index, name="index"),
    path("private/", views.private, name="private"),
    path("private/create/", views.private_create, name="private_create"),
    path("private/update/<int:todo_id>/", views.private_update, name="private_update"),
    path("private/delete/<int:todo_id>/", views.private_delete, name="private_delete"),
    path("private/completed/<int:todo_id>/", views.private_completed, name="private_completed"),
    path("private/share/<int:todo_id>/", views.private_share, name="private_share")
]