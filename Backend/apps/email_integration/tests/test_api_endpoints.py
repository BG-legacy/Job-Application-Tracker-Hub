from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class TestEmailIntegrationAPI(TestCase):
    def setUp(self):
        # Create test user with required username
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Setup API client
        self.client = APIClient()
        
        # Debug print statements
        print(f"Created user: {self.user.username}")
        print(f"User is authenticated: {self.user.is_authenticated}")
        
        # Try both authentication methods
        self.client.force_authenticate(user=self.user)
        
        # Also set up token authentication as backup
        refresh = RefreshToken.for_user(self.user)
        token = str(refresh.access_token)
        print(f"Generated token: {token[:10]}...")  # Print first 10 chars of token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_1_connect_email(self):
        """Test /connect-email/ endpoint"""
        url = '/api/email/connect-email/'  # Use direct URL path instead of reverse()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('auth_url', data)
        self.assertIn('state', data)
        self.assertIn('expires_in', data)
        
        # Store state only if test passed
        if response.status_code == 200:
            self.oauth_state = data['state']
        print('✓ Connect Email Test Passed')

    def test_2_scrape_emails(self):
        """Test /scrape-emails/ endpoint"""
        url = '/api/email/scrape-emails/'  # Use direct URL path
        response = self.client.post(url, {'days_back': 30}, format='json')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('emails', data)
        self.assertIsInstance(data['emails'], list)
        self.assertIn('cache_key', data)
        print('✓ Scrape Emails Test Passed')

    def test_3_confirm_applications(self):
        """Test /confirm-applications/ endpoint"""
        url = '/api/email/confirm-applications/'  # Use direct URL path
        response = self.client.post(url, {'email_ids': ['test_id_1', 'test_id_2']}, format='json')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('saved_count', data)
        print('✓ Confirm Applications Test Passed')

    def test_4_error_cases(self):
        """Test error cases"""
        # Test without authentication
        self.client.credentials()  # Remove auth
        response = self.client.post('/api/email/scrape-emails/',
                                  {'days_back': 30},
                                  format='json')
        self.assertEqual(response.status_code, 401)
        
        # Restore auth for remaining tests
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Test invalid days_back
        response = self.client.post('/api/email/scrape-emails/',
                                  {'days_back': 'invalid'},
                                  format='json')
        self.assertEqual(response.status_code, 500)
        
        # Test confirm without cache
        response = self.client.post('/api/email/confirm-applications/',
                                  {'email_ids': ['invalid_id']},
                                  format='json')
        self.assertEqual(response.status_code, 400)
        print('✓ Error Cases Test Passed') 

    def tearDown(self):
        # Clean up created user
        self.user.delete() 