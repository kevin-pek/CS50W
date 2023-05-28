from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>/', views.entry_page, name="entry"),
    path("new/", views.new_page, name="new_page"),
    path("edit/<str:name>/", views.edit_page, name="edit_page"),
    path("wiki/", views.random_page, name="random"),
]
