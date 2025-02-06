from django.urls import path, include
from .views import (
    login_view, register_view, verify_token, 
    profile_view, update_avatar, list_users
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('verify/', verify_token, name='verify-token'),
    path('profile/', profile_view, name='user-profile'),
    path('profile/avatar/', update_avatar, name='update-avatar'),
    path('list/', list_users, name='list-users'),
    path('api/email/', include(('apps.email_integration.urls', 'email'), namespace='email')),
] 