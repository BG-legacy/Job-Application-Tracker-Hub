from django.test import TestCase
from django.utils import timezone
from apps.users.models import User
from apps.applications.models import Application
from apps.ai_insights.models import AIInsight

class AIInsightModelTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test application
        self.application = Application.objects.create(
            user=self.user,
            company_name='Test Company',
            job_title='Software Engineer',
            status='Pending',
            applied_date=timezone.now().date()
        )
        
        # Create test AI insight
        self.ai_insight = AIInsight.objects.create(
            application=self.application,
            trend_analysis='Test trend analysis',
            recommendations='Test recommendations'
        )

    def test_ai_insight_creation(self):
        """Test AIInsight model creation"""
        self.assertTrue(isinstance(self.ai_insight, AIInsight))
        self.assertEqual(str(self.ai_insight.trend_analysis), 'Test trend analysis')
        
    def test_ai_insight_ordering(self):
        """Test AIInsight ordering by created_at"""
        second_insight = AIInsight.objects.create(
            application=self.application,
            trend_analysis='Second analysis',
            recommendations='More recommendations'
        )
        insights = AIInsight.objects.all()
        self.assertEqual(insights[0], second_insight)  # Newest first
        
    def test_cascade_deletion(self):
        """Test that AIInsights are deleted when Application is deleted"""
        initial_count = AIInsight.objects.count()
        self.application.delete()
        self.assertEqual(AIInsight.objects.count(), initial_count - 1) 