
from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.GetNotificationsView.as_view(), name='list-notification'),
]
