from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
from apps.applications.models import Application
from apps.ai_insights.services import AIAnalysisService

class AIAnalysisServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create applications with different statuses
        statuses = ['Pending', 'Interview', 'Offer', 'Rejected', 'Interview']
        for i, status in enumerate(statuses):
            Application.objects.create(
                user=self.user,
                company_name=f'Company {i}',
                job_title='Software Engineer',
                status=status,
                applied_date=timezone.now().date() - timedelta(days=i)
            )

    def test_analyze_application_trends(self):
        """Test application trend analysis"""
        analysis_service = AIAnalysisService()
        insights = analysis_service.analyze_application_trends(self.user)
        
        self.assertIn('trend_analysis', insights)
        self.assertIn('recommendations', insights)
        
        # Verify trend analysis content
        trend_analysis = insights['trend_analysis']
        self.assertIn('Total applications: 5', trend_analysis)
        self.assertIn('Interview rate:', trend_analysis)
        self.assertIn('Offer rate:', trend_analysis)
        
        # Verify recommendations
        recommendations = insights['recommendations']
        self.assertTrue(isinstance(recommendations, str))
        self.assertTrue(len(recommendations) > 0)

    def test_empty_analysis(self):
        """Test analysis with no applications"""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='pass123'
        )
        
        analysis_service = AIAnalysisService()
        insights = analysis_service.analyze_application_trends(new_user)
        
        self.assertIn('Total applications: 0', insights['trend_analysis']) 