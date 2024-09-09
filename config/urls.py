from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include


from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("edu.urls", namespace="education")),
    path("users/", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
