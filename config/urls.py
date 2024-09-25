from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="EduSphere API",
        default_version="v1",
        description="LMS-system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("edu.urls", namespace="education")),
    path("users/", include("users.urls", namespace="users")),
    
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
