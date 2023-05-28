from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:id>", views.view_listing, name="view_listing"),
    path("new", views.create_listing, name="create_listing"),
    path("categories", views.view_categories, name="view_categories"),
    path("categories/<str:name>", views.view_category, name="view_category"),
    path("<int:id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:id>/listings", views.my_listings, name="my_listings"),
    path("<int:id>/bids", views.my_bids, name="my_bids")
]
