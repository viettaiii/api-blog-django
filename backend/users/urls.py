
from django.urls import path
from . import views
urlpatterns = [
    path("register/",  views.RegisterView.as_view(), name='register'),
    path("login/",  views.LoginView.as_view(), name='login'),
    path("me/",  views.GetMeView.as_view(), name='get-me'),
    path("logout/",  views.LogoutView.as_view(), name='logout'),
    path("users/",  views.GetAllUserView.as_view(), name='list-user')
]
