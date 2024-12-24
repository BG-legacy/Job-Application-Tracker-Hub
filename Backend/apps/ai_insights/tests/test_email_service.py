from django.test import TestCase
from django.core import mail
from apps.users.models import User
from ..services.email_service import AIInsightEmailService

class EmailServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.test_insights = {
            'metrics': {
                'response_rate': 0.5,
                'interview_rate': 0.3,
                'success_rate': 0.1
            },
            'recommendations': 'Test recommendation: Keep up the good work!'
        }

    def test_send_insight_email(self):
        """Test sending insight email"""
        email_service = AIInsightEmailService()
        email_service.send_insight_email(self.user, self.test_insights)
        
        # Test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify the email content
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Your Job Application Insights')
        self.assertEqual(email.to, [self.user.email])
        self.assertIn('Test recommendation', email.body)
        self.assertIn(self.user.username, email.body) 