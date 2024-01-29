
from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.CreateLikeView.as_view(), name='create-like'),
    path('list/', views.GetAllLikeView.as_view(), name='list-like'),
    path('delete/<int:pk>/', views.DeleteLikeView.as_view(), name='delete-like'),
]
