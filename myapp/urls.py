from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get", views.get, name="get"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("delete", views.delete, name="delete"),
    path("changepassword", views.changepassword, name="changepassword")
]