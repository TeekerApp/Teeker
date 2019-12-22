
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("register/<slug:option>", views.register_validation, name="register_validation"),
    path("forgot_pwd", views.forgot_pwd, name="forgot_pwd"),
    path("forgot_pwd/<slug:option>", views.forgot_pwd_handler, name="forgot_pwd_handler"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout")
]