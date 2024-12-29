import openai
from django.conf import settings
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ChatGPTService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4"

    async def generate_personalized_insight(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized insights using ChatGPT"""
        try:
            # Construct the prompt with user context
            prompt = self._construct_prompt(user_data)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a career advisor AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                'insight': response.choices[0].message.content,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"ChatGPT API error: {str(e)}")
            return {
                'insight': "Unable to generate insight at this time.",
                'success': False,
                'error': str(e)
            }

    def _construct_prompt(self, user_data: Dict[str, Any]) -> str:
        """Create a detailed prompt based on user data"""
        return f"""
        Analyze the following job application data and provide personalized insights:
        
        Total Applications: {user_data.get('total_apps', 0)}
        Response Rate: {user_data.get('response_rate', 0)}%
        Interview Rate: {user_data.get('interview_rate', 0)}%
        Success Rate: {user_data.get('success_rate', 0)}%
        
        Recent Job Titles: {', '.join(user_data.get('recent_titles', []))}
        Skills: {', '.join(user_data.get('skills', []))}
        
        Please provide:
        1. Analysis of application performance
        2. Specific areas for improvement
        3. Strategic recommendations for increasing success rate
        4. Industry-specific insights based on the job titles
        """ 