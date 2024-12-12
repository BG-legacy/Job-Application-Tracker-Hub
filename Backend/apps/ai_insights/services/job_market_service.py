import requests
from django.conf import settings
from datetime import datetime, timedelta

class JobMarketService:
    @staticmethod
    def get_market_trends():
        """
        Fetch job market trends from external API
        (Using dummy data for demonstration - replace with actual API calls)
        """
        return {
            'hot_skills': ['Python', 'React', 'AWS', 'DevOps'],
            'growing_industries': ['AI/ML', 'Cloud Computing', 'Cybersecurity'],
            'avg_salaries': {
                'entry_level': 75000,
                'mid_level': 100000,
                'senior_level': 150000
            },
            'demand_score': {
                'software_engineer': 0.85,
                'data_scientist': 0.92,
                'product_manager': 0.78
            }
        }

    @staticmethod
    def analyze_job_fit(job_title, skills):
        """Analyze how well a job matches current market demands"""
        market_data = JobMarketService.get_market_trends()
        
        # Calculate job demand score
        base_score = market_data['demand_score'].get(job_title.lower(), 0.5)
        
        # Calculate skill match score
        skill_matches = sum(1 for skill in skills if skill in market_data['hot_skills'])
        skill_score = skill_matches / len(market_data['hot_skills'])
        
        return {
            'demand_score': base_score,
            'skill_match': skill_score,
            'market_alignment': (base_score + skill_score) / 2
        } 