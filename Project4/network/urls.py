
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/profile", views.user, name="user"),
    path("<int:id>/follow", views.follow, name="follow"),
    path("posts", views.posts, name="posts"),
    path("following", views.following, name="following"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("<int:id>/like", views.like, name="like"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
