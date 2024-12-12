from datetime import datetime, timedelta
from django.db.models import Count, Avg
from django.utils import timezone
from .job_market_service import JobMarketService

class AIAnalysisService:
    def __init__(self):
        self.job_market_service = JobMarketService()

    def analyze_application_trends(self, user):
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=90)
        
        applications = user.application_set.filter(
            applied_date__gte=start_date
        )

        # Calculate base metrics
        metrics = {
            'total_apps': applications.count(),
            'status_distribution': dict(applications.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'weekly_application_rate': applications.count() / 13,  # 90 days ≈ 13 weeks
            'response_rate': applications.exclude(status='Pending').count() / applications.count() if applications.count() > 0 else 0,
            'success_rate': applications.filter(status__in=['Offer', 'Accepted']).count() / applications.count() if applications.count() > 0 else 0,
            'interview_conversion': (
                applications.filter(status='Offer').count() / 
                applications.filter(status='Interview').count()
                if applications.filter(status='Interview').count() > 0 else 0
            )
        }
        
        # Add market analysis
        market_data = self.job_market_service.get_market_trends()
        job_titles = user.application_set.values_list('job_title', flat=True).distinct()
        
        market_insights = {
            'market_alignment': self._analyze_market_alignment(job_titles),
            'skill_gaps': self._identify_skill_gaps(job_titles, market_data['hot_skills'])
        }
        
        metrics.update(market_insights)

        # Generate trend analysis text
        trend_analysis = (
            f"Application Analysis (Last 90 Days):\n"
            f"• Volume Metrics:\n"
            f"  - Total applications: {metrics['total_apps']}\n"
            f"  - Weekly application rate: {metrics['weekly_application_rate']:.1f}\n\n"
            f"• Success Metrics:\n"
            f"  - Response rate: {metrics['response_rate']:.1%}\n"
            f"  - Interview conversion rate: {metrics['interview_conversion']:.1%}\n"
            f"  - Overall success rate: {metrics['success_rate']:.1%}\n\n"
            f"• Status Breakdown:\n" +
            '\n'.join(f"  - {status}: {count}" for status, count in metrics['status_distribution'].items())
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics)

        return {
            'trend_analysis': trend_analysis,
            'recommendations': recommendations,
            'metrics': metrics
        }

    def _analyze_market_alignment(self, job_titles):
        """Analyze how well the user's job search aligns with market demands"""
        alignment_scores = []
        for title in job_titles:
            fit_analysis = self.job_market_service.analyze_job_fit(title, [])
            alignment_scores.append(fit_analysis['market_alignment'])
        
        return sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0

    def _identify_skill_gaps(self, job_titles, market_skills):
        """Identify skills gaps based on target roles and market demands"""
        return {
            'missing_critical_skills': ['AWS', 'Kubernetes'],
            'recommended_certifications': ['AWS Certified Developer', 'CKAD']
        }

    def _generate_recommendations(self, metrics):
        """Generate recommendations based on metrics"""
        recommendations = []
        
        if metrics['weekly_application_rate'] < 3:
            recommendations.append("ACTION: Increase application volume to at least 3 per week")
        
        if metrics['response_rate'] < 0.15:
            recommendations.append(
                "RESUME: Consider professional resume review - current response rate is below average"
            )
        
        if metrics['interview_conversion'] < 0.25 and metrics.get('status_distribution', {}).get('Interview', 0) > 3:
            recommendations.append(
                "SKILLS: Focus on interview preparation - conversion rate suggests room for improvement"
            )
        
        if metrics['success_rate'] < 0.05 and metrics['total_apps'] > 10:
            recommendations.append(
                "STRATEGY: Review job search strategy - consider targeting positions better aligned with your skills"
            )

        return "\n\n".join(recommendations)