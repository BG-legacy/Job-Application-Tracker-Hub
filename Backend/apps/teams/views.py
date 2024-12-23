from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Team, TeamMember, TeamTip
from .serializers import TeamSerializer, TeamMemberSerializer, TeamTipSerializer
from .permissions import IsTeamAdminOrReadOnly, IsTeamMemberOrAdmin
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from apps.applications.models import Application
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.ai_insights.services.analysis_service import AIAnalysisService
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsTeamAdminOrReadOnly]
    queryset = Team.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        logger.debug("Getting queryset for user: %s", self.request.user)
        return Team.objects.filter(members__user=self.request.user)

    def perform_create(self, serializer):
        try:
            team = serializer.save(created_by=self.request.user)
            TeamMember.objects.create(
                team=team,
                user=self.request.user,
                role='Admin'
            )
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        except IntegrityError:
            raise serializers.ValidationError('Team creation failed')

    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        # Check if user is team admin
        if not team.team_members.filter(user=request.user, role='Admin').exists():
            return Response(
                {'error': 'Only team admins can delete teams'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        team = self.get_object()
        members = TeamMember.objects.filter(team=team)
        serializer = TeamMemberSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        team = self.get_object()
        if not TeamMember.objects.filter(
            team=team,
            user=request.user,
            role='Admin'
        ).exists():
            return Response(
                {"error": "Only team admins can add members"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = TeamMemberSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(team=team)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "User is already a team member"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove_member(self, request, pk=None, member_id=None):
        team = self.get_object()
        if not TeamMember.objects.filter(
            team=team,
            user=request.user,
            role='Admin'
        ).exists():
            return Response(
                {"error": "Only team admins can remove members"},
                status=status.HTTP_403_FORBIDDEN
            )

        member = get_object_or_404(TeamMember, id=member_id, team=team)
        
        # Prevent removing the last admin
        if member.role == 'Admin' and team.members.filter(role='Admin').count() <= 1:
            return Response(
                {"error": "Cannot remove the last admin"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post'])
    def tips(self, request, pk=None):
        team = self.get_object()
        
        if request.method == 'GET':
            tips = team.tips.all()
            serializer = TeamTipSerializer(tips, many=True, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = TeamTipSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                tip = serializer.save(team=team, author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='tips/(?P<tip_id>[^/.]+)/rate')
    def rate_tip(self, request, pk=None, tip_id=None):
        team = self.get_object()
        tip = get_object_or_404(TeamTip, id=tip_id, team=team)
        
        if tip.upvotes.filter(id=request.user.id).exists():
            tip.upvotes.remove(request.user)
            action = 'removed'
        else:
            tip.upvotes.add(request.user)
            action = 'added'
        
        serializer = TeamTipSerializer(tip, context={'request': request})
        return Response({
            'message': f'Upvote {action}',
            'tip': serializer.data
        }) 

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Fetch collective team progress data"""
        team = self.get_object()
        team_members = team.members.values_list('user_id', flat=True)
        
        # Get date range (last 30 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Get applications from team members
        applications = Application.objects.filter(
            user_id__in=team_members,
            date_applied__gte=start_date
        )
        
        # Calculate metrics
        metrics = {
            'total_applications': applications.count(),
            'status_breakdown': applications.values('status').annotate(
                count=Count('id')
            ),
            'active_members': applications.values('user').distinct().count(),
            'interview_rate': applications.filter(
                status='Interview'
            ).count() / max(applications.count(), 1) * 100,
            'offer_rate': applications.filter(
                status='Offer'
            ).count() / max(applications.count(), 1) * 100
        }
        
        return Response(metrics)

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        """Generate AI recommendations for team performance"""
        team = self.get_object()
        analysis_service = AIAnalysisService()
        
        try:
            # Get all team members' applications
            team_members = team.team_members.values_list('user_id', flat=True)
            
            # Analyze each member's trends
            insights = []
            for user_id in team_members:
                member_insights = analysis_service.analyze_application_trends(
                    User.objects.get(id=user_id)
                )
                insights.append(member_insights)
            
            # Aggregate team metrics
            team_metrics = {
                'total_applications': sum(i['metrics']['total_applications'] for i in insights),
                'response_rate': sum(i['metrics']['response_rate'] for i in insights) / len(insights),
                'interview_conversion': sum(i['metrics']['interview_conversion'] for i in insights) / len(insights),
                'success_rate': sum(i['metrics']['success_rate'] for i in insights) / len(insights)
            }
            
            return Response({
                'team_metrics': team_metrics,
                'member_insights': insights
            })
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return Response(
                {'error': 'Failed to generate recommendations'},
                status=500
            )

    def check_team_permission(self, team, required_role='Member'):
        member = team.team_members.filter(user=self.request.user).first()
        if not member:
            raise PermissionDenied('You are not a member of this team')
        if required_role == 'Admin' and member.role != 'Admin':
            raise PermissionDenied('Admin privileges required')

    @action(detail=True, methods=['patch'])
    def update_member_role(self, request, pk=None, member_id=None):
        team = self.get_object()
        member = get_object_or_404(TeamMember, id=member_id, team=team)
        
        new_role = request.data.get('role')
        if new_role not in ['Admin', 'Member']:
            return Response(
                {"error": "Invalid role. Must be 'Admin' or 'Member'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevent demoting the last admin
        if member.role == 'Admin' and new_role == 'Member':
            admin_count = team.members.filter(role='Admin').count()
            if admin_count <= 1:
                return Response(
                    {"error": "Cannot demote the last admin"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        member.role = new_role
        member.save()
        
        serializer = TeamMemberSerializer(member)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='members/(?P<member_id>[^/.]+)/update')
    def update_member(self, request, pk=None, member_id=None):
        team = self.get_object()
        member = get_object_or_404(TeamMember, id=member_id, team=team)
        
        # Prevent removing the last admin
        if member.role == 'Admin' and request.data.get('role') != 'Admin':
            admin_count = team.members.filter(role='Admin').count()
            if admin_count <= 1:
                return Response(
                    {"error": "Cannot remove the last admin"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = TeamMemberSerializer(
            member, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        logger.debug("Create method called with data: %s", request.data)
        logger.debug("Request method: %s", request.method)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                team = serializer.save(created_by=request.user)
                logger.debug("Team created: %s", team)
                
                TeamMember.objects.create(
                    team=team,
                    user=request.user,
                    role='Admin'
                )
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error("Error creating team: %s", str(e))
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        logger.error("Serializer errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        logger.debug(f"Checking permissions for {self.action} action")
        return super().get_permissions()

    def initial(self, request, *args, **kwargs):
        logger.debug(f"Initial method called for {request.method} request")
        super().initial(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='tips/(?P<tip_id>[^/.]+)/upvote')
    def upvote_tip(self, request, pk=None, tip_id=None):
        """Handle upvoting/un-upvoting a team tip"""
        team = self.get_object()
        tip = get_object_or_404(TeamTip, id=tip_id, team=team)
        
        if tip.upvotes.filter(id=request.user.id).exists():
            tip.upvotes.remove(request.user)
            action = 'removed'
        else:
            tip.upvotes.add(request.user)
            action = 'added'
        
        serializer = TeamTipSerializer(tip, context={'request': request})
        return Response({
            'message': f'Upvote {action}',
            'tip': serializer.data
        })