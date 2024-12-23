from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone
from .job_market_service import JobMarketService

class AIAnalysisService:
    def __init__(self):
        self.job_market_service = JobMarketService()

    def analyze_application_trends(self, user):
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=90)
        
        applications = user.application_set.filter(
            date_applied__gte=start_date
        )

        # Calculate base metrics
        total_apps = applications.count()
        response_rate = self._calculate_response_rate(applications)
        interview_rate = self._calculate_interview_conversion(applications)
        success_rate = self._calculate_success_rate(applications)

        # Generate recommendations based on metrics
        recommendations = self._generate_recommendations({
            'total_apps': total_apps,
            'response_rate': response_rate,
            'interview_rate': interview_rate,
            'success_rate': success_rate
        })

        return {
            'metrics': {
                'total_apps': total_apps,
                'response_rate': response_rate,
                'interview_rate': interview_rate,
                'success_rate': success_rate
            },
            'recommendations': recommendations
        }

    def _calculate_response_rate(self, applications):
        if not applications.exists():
            return 0
        responses = applications.exclude(status='Pending').count()
        return responses / applications.count()

    def _calculate_interview_conversion(self, applications):
        if not applications.exists():
            return 0
        interviews = applications.filter(status='Interview').count()
        return interviews / applications.count()

    def _calculate_success_rate(self, applications):
        if not applications.exists():
            return 0
        offers = applications.filter(status='Offer').count()
        return offers / applications.count()

    def _generate_recommendations(self, metrics):
        recommendations = []
        
        if metrics['total_apps'] == 0:
            return "START: Begin your job search journey by submitting your first application"
            
        if metrics['response_rate'] < 0.15:
            recommendations.append(
                "RESUME: Consider professional resume review - current response rate is below average"
            )
        
        if metrics['interview_rate'] < 0.25 and metrics['total_apps'] > 3:
            recommendations.append(
                "SKILLS: Focus on interview preparation - conversion rate suggests room for improvement"
            )
        
        if metrics['success_rate'] < 0.05 and metrics['total_apps'] > 10:
            recommendations.append(
                "STRATEGY: Review job search strategy - consider targeting positions better aligned with your skills"
            )
            
        # Add default recommendation if none generated
        if not recommendations:
            recommendations.append(
                "PROGRESS: Keep maintaining your current approach - your metrics are looking good"
            )
            
        return "\n\n".join(recommendations)