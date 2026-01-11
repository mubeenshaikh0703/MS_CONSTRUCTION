from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    login_view,
    signup_view,
    reset_password_view,
    profile_view,
    delete_account,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('reset-password/', reset_password_view, name='reset_password'),
    path('profile/', profile_view, name='profile'),
    path('delete-account/', delete_account, name='delete_account'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
