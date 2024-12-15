from django.contrib import admin
from django.urls import path, include
from apps.users.views import login_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/login/', login_view, name='login'),
    path('api/users/register/', register_view, name='register'),
    path('api/applications/', include('apps.applications.urls')),
] 