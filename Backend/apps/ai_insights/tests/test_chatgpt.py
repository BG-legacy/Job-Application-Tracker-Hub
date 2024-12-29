import asyncio
from django.test import TestCase
from ..services.chatgpt_service import ChatGPTService

class ChatGPTServiceTest(TestCase):
    def test_api_connection(self):
        # Sample user data
        test_data = {
            'total_apps': 10,
            'response_rate': 50,
            'interview_rate': 30,
            'success_rate': 20,
            'recent_titles': ['Software Engineer', 'Full Stack Developer'],
            'skills': ['Python', 'Django', 'JavaScript']
        }
        
        # Create service instance
        service = ChatGPTService()
        
        # Run async test
        async def run_test():
            result = await service.generate_personalized_insight(test_data)
            print("\nAPI Response:", result)
            return result
            
        # Execute test
        result = asyncio.run(run_test())
        
        # Verify response
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['insight'])