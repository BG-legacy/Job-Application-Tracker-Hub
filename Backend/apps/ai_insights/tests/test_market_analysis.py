from django.test import TestCase
from django.utils import timezone
from apps.users.models import User
from apps.applications.models import Application
from apps.ai_insights.services.job_market_service import JobMarketService
from apps.ai_insights.services.analysis_service import AIAnalysisService

class JobMarketAnalysisTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.application = Application.objects.create(
            user=self.user,
            company_name='Tech Corp',
            job_title='Software Engineer',
            status='Pending',
            applied_date=timezone.now().date()
        )
        
        self.market_service = JobMarketService()
        self.analysis_service = AIAnalysisService()

    def test_market_trends_data(self):
        """Test market trends data structure"""
        trends = self.market_service.get_market_trends()
        
        self.assertIn('hot_skills', trends)
        self.assertIn('growing_industries', trends)
        self.assertIn('avg_salaries', trends)
        self.assertIn('demand_score', trends)

    def test_job_fit_analysis(self):
        """Test job fit analysis"""
        analysis = self.market_service.analyze_job_fit(
            'Software Engineer',
            ['Python', 'React']
        )
        
        self.assertIn('demand_score', analysis)
        self.assertIn('skill_match', analysis)
        self.assertIn('market_alignment', analysis)
        self.assertTrue(0 <= analysis['market_alignment'] <= 1)

    def test_enhanced_insights(self):
        """Test enhanced insights with market data"""
        insights = self.analysis_service.analyze_application_trends(self.user)
        
        self.assertIn('metrics', insights)
        self.assertIn('market_alignment', insights['metrics'])
        self.assertIn('skill_gaps', insights['metrics']) 