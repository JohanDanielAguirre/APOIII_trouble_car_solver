from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.user_login, name="login"),
    path("register", views.register, name="register"),
    path("forget_password", views.password_reset_request, name="forget_password"),
    path("logout", views.log_out, name="logout"),
    path("chat_history", views.chat_history, name="chat_history"),
    path("delete_history", views.delete_history, name="delete_history"),

    
]
