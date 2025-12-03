from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("chat.chatapp.urls")),  # ✅ use app's URLs
    path("admin/", admin.site.urls),
]
