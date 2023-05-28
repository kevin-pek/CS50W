from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/create", views.create_task, name="create_task"),
    path("tasks/toggle", views.toggle_task, name="toggle_task"),
    path("tasks/delete", views.delete_task, name="delete_task"),
    path("tasks/<str:viewname>", views.changeview, name="changeview"),

    path("boards", views.noticeboard, name="noticeboard"),
    path("boards/<str:boardname>", views.load_board, name="loadboard"),
    path("boards/<str:boardname>/add", views.add_note, name="addnote"),
    path("boards/<int:note_id>/save", views.update_note, name="updatenote"),
    path("boards/delete/<int:note_id>", views.delete_note, name="deletenote"),

    path("calendar", views.calendar, name="calendar"),
    path("calendar/get_tasks", views.get_tasks, name="get_tasks"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
