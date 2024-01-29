
from django.urls import path, include
from . import views
urlpatterns = [
    path('create/', views.CreateFriendRequestView.as_view(), name='create-friend-request'),
    path('list-friend-request-me/', views.GetFriendRequestMeView.as_view(), name='create-friend-request'),
    path('accept/<int:pk>/', views.AcceptFriendRequestView.as_view(), name='accept-friend'),
    path('reject/<int:pk>/', views.RejectFriendRequestView.as_view(), name='reject-friend'),
    path('unfriend/<int:pk>/', views.UnFriendRequestView.as_view(), name='unfriend'),
    path('friends/', views.GetFriendsView.as_view(), name='get-friends'),
    # path('list/', views.GetAllLikeView.as_view(), name='list-like'),
    # path('delete/<int:pk>/', views.DeleteLikeView.as_view(), name='delete-like'),
]
