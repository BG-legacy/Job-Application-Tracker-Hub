from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('teams/<int:pk>/members/<int:member_id>/', 
         TeamViewSet.as_view({
             'delete': 'remove_member',
             'patch': 'update_member_role'
         }), 
         name='team-member-detail'),
]

