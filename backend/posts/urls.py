
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("create/", views.CreatePostView.as_view(), name='create-post'),
    path("list/", views.GetAllPostView.as_view(), name='list-post'),
    path("list-me/", views.GetAllPostMeView.as_view(), name='list-post-me'),


    path("update/<int:pk>/", views.UpdatePostView.as_view(), name='update-post'),
    path("delete/<int:pk>/", views.DeletePostView.as_view(), name='delete-post'),
    path("detail/<int:pk>/", views.GetDetailPostView.as_view(), name='detail-post')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
