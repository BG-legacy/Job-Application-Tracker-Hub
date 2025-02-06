from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.applications.models import Application
from apps.ai_insights.services.analysis_service import AIAnalysisService
from unittest.mock import patch, MagicMock
from datetime import datetime

User = get_user_model()

class TestAIAnalysisService(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test applications
        self.application = Application.objects.create(
            user=self.user,
            company_name='Test Company',
            job_title='Software Engineer',
            job_description='Python Django React JavaScript',
            date_applied=datetime.now(),
            status='Pending'
        )
        
        self.service = AIAnalysisService()

    @patch('openai.chat.completions.create')
    def test_get_chatgpt_insights_success(self, mock_openai):
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Test AI insight response"))
        ]
        mock_openai.return_value = mock_response

        # Test metrics
        metrics = {
            'response_rate': 50.0,
            'interview_rate': 25.0,
            'success_rate': 10.0,
            'market_alignment': 0.7
        }

        # Get insights
        insights = self.service._get_chatgpt_insights(
            metrics, 
            Application.objects.filter(user=self.user)
        )

        # Assertions
        self.assertEqual(insights, "Test AI insight response")
        mock_openai.assert_called_once()
        
        # Verify the prompt structure
        call_args = mock_openai.call_args[1]
        self.assertEqual(call_args['model'], 'gpt-4')
        self.assertEqual(len(call_args['messages']), 2)
        self.assertEqual(call_args['temperature'], 0.7)

    @patch('openai.chat.completions.create')
    def test_get_chatgpt_insights_error(self, mock_openai):
        # Mock OpenAI error
        mock_openai.side_effect = Exception("API Error")

        # Test metrics
        metrics = {
            'response_rate': 50.0,
            'interview_rate': 25.0,
            'success_rate': 10.0,
            'market_alignment': 0.7
        }

        # Get insights
        insights = self.service._get_chatgpt_insights(
            metrics, 
            Application.objects.filter(user=self.user)
        )

        # Assert error handling
        self.assertEqual(insights, "Unable to generate AI insights at this time.")

    def test_construct_insight_prompt(self):
        # Test metrics
        metrics = {
            'response_rate': 50.0,
            'interview_rate': 25.0,
            'success_rate': 10.0,
            'market_alignment': 0.7
        }

        # Get prompt
        prompt = self.service._construct_insight_prompt(
            metrics,
            Application.objects.filter(user=self.user)
        )

        # Assert prompt structure
        self.assertIn('Response Rate: 50.0%', prompt)
        self.assertIn('Interview Rate: 25.0%', prompt)
        self.assertIn('Success Rate: 10.0%', prompt)
        self.assertIn('Market Alignment: 0.7', prompt)
        self.assertIn('Software Engineer', prompt)  # Job title from test application 