from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path("jwt/", include("authentication.urls")),
    path("document/", include("hub.urls")),
]

urlpatterns += static(
    settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, "static")
)
