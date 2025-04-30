from core.views import HomeView
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("projects_history/", include("projects_history.urls")),
    path("projects/", include("projects.urls")),
    path("rooms/", include("rooms.urls")),
    path("calculations/", include("calculations.urls")),
    path("plans/", include("plans.urls")),
    path("", HomeView.as_view(), name="home"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
