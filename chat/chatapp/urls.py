from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, chat_view, signup

urlpatterns = [
    path("", home, name="home"),
    path("chat/<int:conversation_id>/", chat_view, name="chat_view"),
    path("login/", auth_views.LoginView.as_view(template_name="chatapp/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
]
