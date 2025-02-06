from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet
import logging

logger = logging.getLogger(__name__)

router = DefaultRouter()
logger.debug("Registering TeamViewSet with router")
router.register('', TeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/members/<int:member_id>/', 
         TeamViewSet.as_view({
             'delete': 'remove_member',
             'patch': 'update_member_role',
         }), 
         name='team-member-detail'),
    path('<int:pk>/tips/<int:tip_id>/upvote/', 
         TeamViewSet.as_view({
             'post': 'upvote_tip',
         }), 
         name='team-tip-upvote'),
]

logger.debug(f"Generated URL patterns: {router.urls}")

