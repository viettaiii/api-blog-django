
from django.urls import path,include
from . import views
urlpatterns = [
    path('create/' , views.CreateCommentView.as_view(), name='create-comment'),
    path('reply/' , views.ReplyCommentView.as_view(), name='reply-comment'),
    path('update/<int:pk>/' , views.UpdateCommentView.as_view(), name='update-comment'),
    path('delete/<int:pk>/' , views.DeleteCommentView.as_view(), name='delete-comment'),
    path('list/' , views.GetAllCommentView.as_view(), name='list-comment')
]
