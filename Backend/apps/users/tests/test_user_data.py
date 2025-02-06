from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class UserDataTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.url = reverse('user-data')

    def test_get_user_data_authenticated(self):
        """Test retrieving user data with authentication"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('career_level', response.data['data'])
        self.assertIn('skills', response.data['data'])

    def test_update_career_data_success(self):
        """Test updating career-related data"""
        data = {
            'career_level': 'Senior',
            'career_field': 'Software Development',
            'years_experience': 5,
            'target_role': 'Tech Lead',
            'target_salary_range': '100k-150k',
            'skills': ['Python', 'Django', 'React']
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['career_level'], data['career_level'])
        self.assertEqual(response.data['data']['skills'], data['skills'])

    def test_invalid_salary_range(self):
        """Test validation of invalid salary range"""
        data = {'target_salary_range': 'invalid-range'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('target_salary_range', response.data['details'])

    def test_invalid_years_experience(self):
        """Test validation of negative years of experience"""
        data = {'years_experience': -1}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('years_experience', response.data['details'])

    def test_invalid_skills_format(self):
        """Test validation of skills format"""
        data = {'skills': 'Python, Django'}  # Should be a list
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('skills', response.data['details'])

    def test_partial_update(self):
        """Test partial update of user data"""
        initial_data = {
            'career_level': 'Senior',
            'skills': ['Python', 'Django']
        }
        self.client.post(self.url, initial_data, format='json')
        
        update_data = {'career_field': 'Web Development'}
        response = self.client.post(self.url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['career_field'], update_data['career_field'])
        self.assertEqual(response.data['data']['career_level'], initial_data['career_level'])

    def test_empty_update(self):
        """Test update with empty data"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        """Test accessing endpoint without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 