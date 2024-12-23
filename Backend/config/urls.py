from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.users.views import login_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/login/', login_view, name='login'),
    path('api/users/register/', register_view, name='register'),
    path('api/', include([
        path('', include('apps.applications.urls')),
        path('ai-insights/', include('apps.ai_insights.urls')),
        path('users/', include('apps.users.urls')),
        path('teams/', include('apps.teams.urls')),
    ])),
    path('api/', include('apps.teams.urls')),
    path('api/ai/', include('apps.ai_insights.urls')),
    path('api/teams/', include('apps.teams.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
