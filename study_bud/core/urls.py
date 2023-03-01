from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.sign_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("register", views.sign_up, name="register"),
    path("user/<int:pk>", views.user_profile, name="user-profile"),
    path("room/<int:pk>", views.room, name="room"),
    path("room/new", views.create_room, name="create-room"),
    path("room/<int:pk>/", views.edit_room, name="edit-room"),
    path("room/<int:pk>/delete/", views.delete_room, name="delete-room"),
    path("message/<int:pk>/delete/", views.delete_message, name="delete-message"),
]
