from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<int:pk>", views.room, name="room"),
    path("room/new", views.create_room, name="create-room"),
    path("room/<int:pk>/", views.edit_room, name="edit-room"),
    path("room/<int:pk>/delete/", views.delete_room, name="delete-room"),
]
