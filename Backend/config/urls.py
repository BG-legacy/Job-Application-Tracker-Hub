from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.users.views import login_view, register_view
import os

# Debug prints
print("URL Patterns Debug:")
print(f"DEBUG mode: {settings.DEBUG}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"File path: {os.path.join(settings.MEDIA_ROOT, 'avatars', 'Screenshot_2024-12-18_at_8.10.30PM.png')}")
print(f"File exists: {os.path.exists(os.path.join(settings.MEDIA_ROOT, 'avatars', 'Screenshot_2024-12-18_at_8.10.30PM.png'))}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/login/', login_view, name='login'),
    path('api/users/register/', register_view, name='register'),
    path('api/', include([
        path('', include('apps.applications.urls')),
        path('ai-insights/', include('apps.ai_insights.urls')),
        path('users/', include('apps.users.urls')),
        path('teams/', include('apps.teams.urls')),
        path('email/', include('apps.email_integration.urls', namespace='email_integration')),
        path('data/', include('apps.data_exchange.urls')),
    ])),
    path('api/', include('apps.teams.urls')),
    path('api/ai/', include('apps.ai_insights.urls')),
    path('api/teams/', include('apps.teams.urls')),
]

# Make media serving explicit
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    print("✓ Media URLs added to urlpatterns")
