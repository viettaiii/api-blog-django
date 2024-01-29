
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='1.0.0',
        description='API docs'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include([
        path('auth/', include('users.urls')),
        path('posts/', include('posts.urls')),
        path('comments/', include('comments.urls')),
        path('likes-post/', include('likes.urls')),
        path('likes-comment/', include('likesComment.urls')),
        path('friend-requests/', include('friendRequests.urls')),
        path('notifications/', include('notifications.urls')),
        path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema')
    ]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
