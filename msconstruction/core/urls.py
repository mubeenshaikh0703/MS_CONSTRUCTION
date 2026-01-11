from django.urls import path
from .views import home, admin_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]
