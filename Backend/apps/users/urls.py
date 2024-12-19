from django.urls import path
from .views import login_view, register_view, verify_token, profile_view, update_avatar

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('verify/', verify_token, name='verify-token'),
    path('profile/', profile_view, name='user-profile'),
    path('profile/avatar/', update_avatar, name='update-avatar'),
] 