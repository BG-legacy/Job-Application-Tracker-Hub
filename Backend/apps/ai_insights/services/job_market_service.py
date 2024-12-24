import requests
from django.conf import settings
from datetime import datetime, timedelta

class JobMarketService:
    def __init__(self):
        # Initialize with common tech skills and their market demand
        self.market_data = {
            'hot_skills': [
                'Python',
                'JavaScript',
                'React',
                'AWS',
                'Docker',
                'Kubernetes',
                'Machine Learning',
                'DevOps',
                'SQL',
                'Node.js'
            ],
            'demand_scores': {
                'Python': 0.9,
                'JavaScript': 0.85,
                'React': 0.8,
                'AWS': 0.85,
                'Docker': 0.75,
                'Kubernetes': 0.7,
                'Machine Learning': 0.8,
                'DevOps': 0.85,
                'SQL': 0.75,
                'Node.js': 0.7
            }
        }

    def get_market_trends(self):
        """Return current market trends and in-demand skills"""
        return self.market_data

    @staticmethod
    def analyze_job_fit(job_title, skills):
        """Analyze how well a job matches with given skills"""
        # Simple scoring system
        base_score = 0.5  # Default market alignment
        skill_match = len(skills) / 10  # Normalize by expected number of skills
        
        return {
            'market_alignment': round((base_score + skill_match) / 2, 2),
            'skill_match': skill_match
        } 