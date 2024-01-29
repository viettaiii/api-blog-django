
from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.CreateLikeCommentView.as_view(), name='create-like-comment'),
    path('list/', views.GetAllLikeCommentView.as_view(), name='list-like-comment'),
    path('delete/<int:pk>/', views.DeleteLikeCommentView.as_view(), name='delete-like-comment'),
]
