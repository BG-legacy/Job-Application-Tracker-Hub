from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ..models import Application
from datetime import date

User = get_user_model()

class ApplicationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.application_data = {
            'company_name': 'Test Company',
            'job_title': 'Software Engineer',
            'status': 'Pending',
            'applied_date': date.today()
        }
        
        self.application = Application.objects.create(
            user=self.user,
            **self.application_data
        )

    def test_create_application(self):
        """Test creating a new application"""
        url = reverse('application-list')
        response = self.client.post(url, self.application_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 2)

    def test_list_applications(self):
        """Test listing user's applications"""
        url = reverse('application-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_application(self):
        """Test updating an application"""
        url = reverse('application-detail', args=[self.application.id])
        updated_data = {
            'company_name': 'Updated Company',
            'job_title': 'Senior Engineer',
            'status': 'Interview',
            'applied_date': date.today()
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.company_name, 'Updated Company')

    def test_delete_application(self):
        """Test deleting an application"""
        url = reverse('application-detail', args=[self.application.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.count(), 0)

    def test_unauthorized_access(self):
        """Test unauthorized access to applications"""
        self.client.force_authenticate(user=None)
        url = reverse('application-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 