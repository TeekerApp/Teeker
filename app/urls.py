
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("results=<slug:search>", views.index, name="index_search"),
    path("account", views.account, name="account"),
    path("register", views.register, name="register"),
    path("register/<slug:option>", views.register_validation, name="register_validation"),
    path("forgot_pwd", views.forgot_pwd, name="forgot_pwd"),
    path("forgot_pwd/<slug:option>", views.forgot_pwd_handler, name="forgot_pwd_handler"),
    path("forgot_pwd/<slug:option>/c", views.forgot_pwd_change, name="forgot_pwd_change"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("search_bar", views.search_bar, name="search_bar"),
    path("settings", views.settings_page, name="settings"),
    path("feedback", views.feedback, name="feedback"),
    path("inbox", views.inbox, name="inbox"),
    path("subscriptions", views.subscriptions, name="subscriptions"),
    path("upload_post", views.upload_post, name="upload_post"),
    path("visitor_account_view/<slug:option>", views.visitor_account_view, name="visitor_account_view"),
    path(r'^.well-known/acme-challenge/.*$', views.acme_challenge, name='acme-challenge')
]