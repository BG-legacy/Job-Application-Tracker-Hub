from celery import shared_task
from django.utils import timezone
from apps.users.models import User
from .models import AIInsight
from .services.analysis_service import AIAnalysisService

@shared_task
def generate_periodic_insights():
    """Generate insights for all active users daily"""
    today = timezone.now().date()
    
    for user in User.objects.filter(is_active=True):
        analysis_service = AIAnalysisService()
        insights = analysis_service.analyze_application_trends(user)
        
        # Store the latest insights
        recent_applications = user.application_set.order_by('-applied_date')[:1]
        if recent_applications:
            AIInsight.objects.create(
                application=recent_applications[0],
                trend_analysis=insights['trend_analysis'],
                recommendations=insights['recommendations']
            )

    return f"Generated insights for {User.objects.filter(is_active=True).count()} users" 