from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.analysis_service import AIAnalysisService
from .models import AIInsight
from .serializers import AIInsightSerializer
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from apps.applications.models import Application
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class AIInsightView(APIView):
    # Ensure only authenticated users can access
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Create analysis service instance
        analysis_service = AIAnalysisService()
        # Generate insights for the current user
        insights = analysis_service.analyze_application_trends(request.user)
        
        # Return formatted response
        return Response({
            'trend_analysis': insights['trend_analysis'],
            'recommendations': insights['recommendations']
        })

    def post(self, request):
        """Generate new insights for the user"""
        try:
            analysis_service = AIAnalysisService()
            insights = analysis_service.analyze_application_trends(request.user)
            
            # Get most recent application
            recent_application = Application.objects.filter(user=request.user).order_by('-date_applied').first()
            
            if recent_application:
                # Create new insight
                insight = AIInsight.objects.create(
                    application=recent_application,
                    trend_analysis=str(insights['metrics']),
                    recommendations=insights['recommendations']
                )
                
                serializer = AIInsightSerializer(insight)
                return Response(serializer.data, status=201)
            
            return Response({
                'error': 'No applications found to generate insights'
            }, status=400)
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return Response({
                'error': 'Failed to generate insights'
            }, status=500)

class ApplicationInsightView(APIView):
    # Ensure only authenticated users can access
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        try:
            # Get insights for specific application (only if user owns it)
            insight = AIInsight.objects.get(
                application_id=application_id,
                application__user=request.user
            )
            # Serialize the insight data
            serializer = AIInsightSerializer(insight)
            return Response(serializer.data)
        except AIInsight.DoesNotExist:
            # Return 404 if no insights found
            return Response({'error': 'No insights found'}, status=404)

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            logger.debug(f"Processing dashboard summary request for user {request.user.id}")
            
            # Get user's applications
            user_applications = Application.objects.filter(user=request.user)
            
            # Get date range for recent applications
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            
            # Calculate summary statistics
            summary_data = {
                'total_applications': user_applications.count(),
                'status_breakdown': dict(
                    user_applications.values('status')
                    .annotate(count=Count('id'))
                    .values_list('status', 'count')
                ),
                'recent_applications': user_applications.filter(
                    date_applied__gte=start_date
                ).count(),
                'response_rate': self._calculate_response_rate(user_applications),
                'monthly_applications': self._get_monthly_trend(user_applications),
                'top_positions': self._get_top_positions(user_applications)
            }
            
            logger.debug("Successfully generated dashboard summary")
            return Response(summary_data)
            
        except Exception as e:
            logger.error(f"Error generating dashboard summary: {str(e)}")
            return Response(
                {'error': 'Failed to generate dashboard summary'},
                status=500
            )

    def _calculate_response_rate(self, applications):
        total = applications.count()
        if total == 0:
            return 0
        responses = applications.exclude(status='Pending').count()
        return round((responses / total) * 100, 2)

    def _get_monthly_trend(self, applications):
        last_6_months = timezone.now() - timedelta(days=180)
        monthly_data = (
            applications.filter(date_applied__gte=last_6_months)
            .values('date_applied__month')
            .annotate(count=Count('id'))
            .order_by('date_applied__month')
        )
        return {item['date_applied__month']: item['count'] for item in monthly_data}

    def _get_top_positions(self, applications):
        return dict(
            applications.values('position')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
            .values_list('position', 'count')
        )

class AIRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Create cache key based on user ID and timestamp (daily)
            cache_key = f'ai_recommendations_{request.user.id}_{timezone.now().date()}'
            
            # Try to get cached insights first
            cached_insights = cache.get(cache_key)
            if cached_insights:
                return Response(cached_insights)

            # If no cache, generate new insights
            analysis_service = AIAnalysisService()
            insights = analysis_service.analyze_application_trends(request.user)
            
            # Get the ChatGPT analysis
            chatgpt_analysis = insights.get('metrics', {}).get('chatgpt_analysis')
            if not chatgpt_analysis:
                metrics = insights.get('metrics', {})
                chatgpt_analysis = analysis_service._get_chatgpt_insights(metrics, request.user.application_set.all())
            
            response_data = {
                'chatgpt_analysis': chatgpt_analysis or 'Analysis will be available once you submit applications',
                'metrics': {
                    'response_rate': insights.get('metrics', {}).get('response_rate', 0),
                    'interview_rate': insights.get('metrics', {}).get('interview_rate', 0),
                    'success_rate': insights.get('metrics', {}).get('success_rate', 0),
                    'market_alignment': insights.get('metrics', {}).get('market_alignment', 0)
                }
            }

            # Cache the response for 24 hours
            cache.set(cache_key, response_data, 60 * 60 * 24)
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return Response(
                {'error': 'Failed to generate recommendations'},
                status=500
            )