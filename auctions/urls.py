from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>/profile", views.profile, name="profile"),
    path("createList", views.create, name="create"),
    path("activeList",views.active, name="active"),
    path("allList/<str:category>", views.allList, name="allList"),
    path("fullList/<str:title>", views.fullList, name="fullList"),
    path("<str:username>/watchList", views.watchlist, name="watchlist"),
    path("<str:username>/viewList/<str:title>", views.viewlist, name="viewlist")
]
