from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from apps.users.models import User
from apps.applications.models import Application
from apps.ai_insights.models import AIInsight

class AIInsightViewsTest(APITestCase):
    def setUp(self):
        # Create test user and token
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create test application
        self.application = Application.objects.create(
            user=self.user,
            company_name='Test Company',
            job_title='Software Engineer',
            status='Pending',
            applied_date=timezone.now().date()
        )

    def test_get_ai_insights(self):
        """Test getting AI insights"""
        url = reverse('ai-insights')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('trend_analysis', response.data)
        self.assertIn('recommendations', response.data)

    def test_get_application_insights(self):
        """Test getting insights for specific application"""
        # Create an insight for the application
        insight = AIInsight.objects.create(
            application=self.application,
            trend_analysis='Test analysis',
            recommendations='Test recommendations'
        )
        
        url = reverse('application-insights', kwargs={'application_id': self.application.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['trend_analysis'], 'Test analysis')

    def test_unauthorized_access(self):
        """Test unauthorized access is blocked"""
        self.client.credentials()  # Remove authentication
        url = reverse('ai-insights')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 