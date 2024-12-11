from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/reminders/', include('apps.reminders.urls')),
] 