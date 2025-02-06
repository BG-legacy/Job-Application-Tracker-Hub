from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.applications.models import Application
from apps.ai_insights.services.analysis_service import AIAnalysisService
from datetime import datetime
import time

User = get_user_model()

class TestLiveOpenAIIntegration(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test applications with different statuses
        self.applications = [
            Application.objects.create(
                user=self.user,
                company_name='Tech Corp',
                job_title='Senior Software Engineer',
                job_description='Python Django React Node.js AWS',
                date_applied=datetime.now(),
                status='Pending'
            ),
            Application.objects.create(
                user=self.user,
                company_name='AI Solutions',
                job_title='Full Stack Developer',
                job_description='JavaScript TypeScript React Python',
                date_applied=datetime.now(),
                status='Interview'
            ),
            Application.objects.create(
                user=self.user,
                company_name='Data Inc',
                job_title='Backend Developer',
                job_description='Python FastAPI PostgreSQL Docker',
                date_applied=datetime.now(),
                status='Rejected'
            )
        ]
        
        self.service = AIAnalysisService()

    def test_live_chatgpt_insights(self):
        """Test actual OpenAI API integration"""
        print("\nTesting live OpenAI API integration...")
        
        # Calculate test metrics
        metrics = {
            'total_apps': len(self.applications),
            'response_rate': 66.7,  # 2 out of 3 have responses
            'interview_rate': 33.3,  # 1 out of 3 reached interview
            'success_rate': 0.0,    # No offers yet
            'market_alignment': 0.8  # High alignment with tech stack
        }

        # Get actual insights from OpenAI
        insights = self.service._get_chatgpt_insights(
            metrics, 
            Application.objects.filter(user=self.user)
        )

        print(f"\nReceived insights: {insights}\n")

        # Basic validation of response
        self.assertIsNotNone(insights)
        self.assertNotEqual(insights, "Unable to generate AI insights at this time.")
        self.assertTrue(len(insights) > 50)  # Should get a substantial response

        # Verify response contains key terms
        key_terms = ['rate', 'interview', 'recommend', 'improve']
        for term in key_terms:
            self.assertIn(term.lower(), insights.lower())

        # Add delay to respect rate limits
        time.sleep(1)

    def test_live_analysis_trends(self):
        """Test the complete analysis pipeline"""
        print("\nTesting complete analysis pipeline...")
        
        # Get full analysis
        analysis = self.service.analyze_application_trends(self.user)

        print("\nAnalysis Results:")
        print(f"Total Applications: {analysis['metrics']['total_apps']}")
        print(f"Response Rate: {analysis['metrics']['response_rate']}%")
        print(f"Interview Rate: {analysis['metrics']['interview_rate']}%")
        print(f"ChatGPT Analysis: {analysis['metrics']['chatgpt_analysis']}\n")

        # Validate analysis structure
        self.assertIn('metrics', analysis)
        self.assertIn('recommendations', analysis)
        self.assertIn('chatgpt_analysis', analysis['metrics'])

        # Validate metrics
        self.assertEqual(analysis['metrics']['total_apps'], 3)
        self.assertGreaterEqual(analysis['metrics']['response_rate'], 0)
        self.assertLessEqual(analysis['metrics']['response_rate'], 100) 