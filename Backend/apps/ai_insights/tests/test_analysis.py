from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.applications.models import Application
from apps.ai_insights.services.analysis_service import AIAnalysisService
from django.utils import timezone
from datetime import timedelta

class AIAnalysisServiceTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.service = AIAnalysisService()

    def test_new_user_no_applications(self):
        """Test analysis for user with no applications"""
        results = self.service.analyze_application_trends(self.user)
        self.assertEqual(results['metrics']['total_apps'], 0)
        self.assertEqual(
            results['recommendations'],
            "START: Begin your job search journey by submitting your first application"
        )

    def test_low_response_rate(self):
        """Test analysis for low response rate scenario"""
        # Create 10 applications with 8 pending
        for i in range(10):
            status = 'Pending' if i < 8 else 'Interview'
            self._create_application(status, days_ago=i)

        results = self.service.analyze_application_trends(self.user)
        self.assertIn('RESUME', results['recommendations'])
        self.assertEqual(results['metrics']['response_rate'], 20)

    def test_high_success_rate(self):
        """Test analysis for high success rate scenario"""
        statuses = ['Offer', 'Offer', 'Interview', 'Pending', 'Interview']
        for i, status in enumerate(statuses):
            self._create_application(
                status, 
                days_ago=i,
                job_description='Python Django React AWS Developer with 5 years experience'
            )

        results = self.service.analyze_application_trends(self.user)
        self.assertIn('PROGRESS', results['recommendations'])
        self.assertEqual(results['metrics']['success_rate'], 40)

    def test_skill_matching(self):
        """Test skill matching analysis"""
        # Create application with specific skills
        self._create_application(
            'Pending',
            days_ago=1,
            job_description='Looking for Python Django Developer with React and AWS experience'
        )
        
        results = self.service.analyze_application_trends(self.user)
        self.assertTrue(len(self.service._extract_skills(
            'Python Django Developer with React and AWS experience'
        )) >= 3)

    def _create_application(self, status, days_ago, job_description=None):
        """Helper method to create test applications"""
        if job_description is None:
            job_description = 'Generic Software Engineer Position'

        return Application.objects.create(
            user=self.user,
            company_name='Test Company',
            job_title='Software Engineer',
            status=status,
            date_applied=timezone.now() - timedelta(days=days_ago),
            job_description=job_description
        )

    def tearDown(self):
        """Clean up after each test"""
        Application.objects.all().delete() 