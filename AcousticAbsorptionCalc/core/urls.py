from core.views import HomeView
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("users/", include("users.urls", namespace="users")),
    path("user_logs/", include("user_logs.urls", namespace="user-logs")),
    path("projects/", include("projects.urls")),
    path("rooms/", include("rooms.urls")),
    path("calculations/", include("calculations.urls")),
    path("plans/", include("plans.urls", namespace="plans")),
    path("project_logs/", include("project_logs.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
