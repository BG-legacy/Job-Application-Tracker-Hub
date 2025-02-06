from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.email_integration.models import EmailToken, JobEmail
from apps.email_integration.services.email_service import GmailService
from unittest.mock import patch, MagicMock
from datetime import datetime
import base64
import json

User = get_user_model()

class TestGmailService(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create token with proper OAuth2 data structure
        token_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": ["https://www.googleapis.com/auth/gmail.readonly"],
            "client_id": "test_client_id",
            "client_secret": "test_client_secret"
        }
        
        self.token = EmailToken.objects.create(
            user=self.user,
            token_data=json.dumps(token_data)
        )
        
        self.service = GmailService(self.user)

    @patch('apps.email_integration.oauth2.GmailOAuth2')
    @patch('apps.email_integration.services.email_service.build')
    def test_fetch_job_related_emails(self, mock_build, mock_oauth):
        # Mock OAuth2 credentials
        mock_credentials = MagicMock()
        mock_oauth.return_value.refresh_credentials.return_value = mock_credentials
        
        # Mock Gmail API response
        mock_messages = MagicMock()
        mock_messages.list().execute.return_value = {'messages': [{'id': 'msg1'}]}
        mock_messages.get().execute.return_value = {
            'id': 'msg1',
            'threadId': 'thread1',
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': 'Job Application: Software Engineer'},
                    {'name': 'From', 'value': 'hr@company.com'},
                    {'name': 'Date', 'value': '2024-01-15T10:00:00Z'}
                ],
                'body': {'data': base64.b64encode(b'Position: Software Engineer').decode()}
            },
            'labelIds': ['INBOX']
        }
        
        # Setup mock Gmail service
        mock_users = MagicMock()
        mock_users.messages.return_value = mock_messages
        
        mock_service = MagicMock()
        mock_service.users.return_value = mock_users
        
        mock_build.return_value = mock_service

        # Test email fetching
        emails = self.service.fetch_job_related_emails(days_back=7)
        
        # Verify results
        self.assertEqual(len(emails), 1)
        self.assertIn('job_title', emails[0])
        self.assertIn('company_name', emails[0])
        self.assertIn('application_status', emails[0])
        self.assertIn('parsing_confidence', emails[0])

    def test_email_storage(self):
        email_data = {
            'message_id': 'test_msg_1',
            'thread_id': 'test_thread_1',
            'subject': 'Software Engineer Position',
            'from_email': 'hr@company.com',
            'received_date': datetime.now(),
            'body': 'Thank you for your application',
            'job_title': 'Software Engineer',
            'company_name': 'Tech Company',
            'application_status': 'applied',
            'parsing_confidence': 0.9
        }

        # Create job email
        job_email = JobEmail.objects.create(
            user=self.user,
            **email_data
        )

        # Verify storage
        stored_email = JobEmail.objects.get(message_id='test_msg_1')
        self.assertEqual(stored_email.job_title, 'Software Engineer')
        self.assertEqual(stored_email.application_status, 'applied')
        self.assertEqual(stored_email.parsing_confidence, 0.9)

    def test_fetch_emails_no_token(self):
        """Test fetching emails without valid token"""
        # Remove token
        self.token.delete()
        
        with self.assertRaises(Exception) as context:
            service = GmailService(self.user)
            service.get_service()  # Call get_service directly
        
        self.assertIn('Email not connected', str(context.exception))

    def test_parse_email_with_parts(self):
        """Test parsing email with multipart structure"""
        email_data = {
            'id': 'msg1',
            'threadId': 'thread1',
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': 'Job Application'},
                    {'name': 'From', 'value': 'hr@company.com'},
                    {'name': 'Date', 'value': '2024-01-15T10:00:00Z'}
                ],
                'parts': [
                    {
                        'mimeType': 'text/plain',
                        'body': {'data': base64.b64encode(b'Position: Software Engineer').decode()}
                    }
                ]
            },
            'labelIds': ['INBOX']
        }
        
        result = self.service._parse_email(email_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['message_id'], 'msg1')
        self.assertIn('Software Engineer', result['body'])

    @patch('apps.email_integration.services.email_service.build')
    def test_fetch_emails_api_error(self, mock_build):
        """Test handling Gmail API errors"""
        mock_service = MagicMock()
        mock_service.users().messages().list.side_effect = Exception('API Error')
        mock_build.return_value = mock_service
        
        emails = self.service.fetch_job_related_emails()
        
        self.assertEqual(len(emails), 0)

    def test_email_storage_invalid_data(self):
        """Test storing email with invalid data"""
        email_data = {
            'message_id': 'test_msg_2',
            'thread_id': 'test_thread_2',
            'subject': 'A' * 300,  # Exceeds max_length
            'from': 'hr@company.com',
            'date': 'invalid_date',
            'body': 'Test body',
            'job_title': None,
            'company_name': None,
            'application_status': 'invalid_status',
            'parsing_confidence': -1
        }
        
        with self.assertRaises(Exception):
            JobEmail.objects.create(
                user=self.user,
                **email_data
            )