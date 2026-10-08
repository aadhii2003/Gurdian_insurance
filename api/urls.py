from django.urls import path
from . import views

urlpatterns = [
    path('auth/csrf/', views.get_csrf, name='api-csrf'),
    path('auth/login', views.login_view, name='api-login'),
    path('auth/logout', views.logout_view, name='api-logout'),
    path('auth/me', views.get_me, name='api-me'),
    path('dashboard/stats', views.get_dashboard_stats, name='api-stats'),
]
