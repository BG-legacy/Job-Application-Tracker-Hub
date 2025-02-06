from django.test import TestCase
from apps.email_integration.services.email_parser import JobEmailParser

class TestJobEmailParser(TestCase):
    def setUp(self):
        self.parser = JobEmailParser

    def test_parse_application_email(self):
        email_data = {
            'subject': 'Application Received: Software Engineer Position',
            'body': '''
            Thank you for applying to the Software Engineer position at TechCorp.
            
            Position: Senior Software Engineer
            Company: TechCorp Inc.
            
            We have received your application and will review it shortly.
            ''',
            'from': 'recruiting@techcorp.com'
        }
        
        result = self.parser.parse_email(email_data)
        
        self.assertEqual(result['job_title'], 'Senior Software Engineer')
        self.assertEqual(result['company_name'], 'TechCorp Inc')
        self.assertEqual(result['status'], 'applied')
        self.assertGreater(result['confidence_score'], 0.8)
        self.assertIn('parsed_date', result)

    def test_parse_interview_email(self):
        email_data = {
            'subject': 'Interview Invitation',
            'body': '''
            Dear Candidate,
            
            We would like to schedule an interview for the position of:
            Job Title: Full Stack Developer
            Company: StartupCo
            
            Please let us know your availability.
            ''',
            'from': 'hr@startupco.com'
        }
        
        result = self.parser.parse_email(email_data)
        
        self.assertEqual(result['job_title'], 'Full Stack Developer')
        self.assertEqual(result['company_name'], 'StartupCo')
        self.assertEqual(result['status'], 'interview')
        self.assertGreater(result['confidence_score'], 0.8)

    def test_parse_rejection_email(self):
        email_data = {
            'subject': 'Update on your application',
            'body': '''
            Unfortunately, we have decided not to move forward with your application for:
            Position: Data Scientist
            Organization: DataCo Ltd.
            
            We wish you the best in your job search.
            ''',
            'from': 'careers@dataco.com'
        }
        
        result = self.parser.parse_email(email_data)
        
        self.assertEqual(result['job_title'], 'Data Scientist')
        self.assertEqual(result['company_name'], 'DataCo Ltd')
        self.assertEqual(result['status'], 'rejected')
        self.assertGreater(result['confidence_score'], 0.8)

    def test_parse_empty_email(self):
        """Test parsing an empty email"""
        email_data = {
            'subject': '',
            'body': '',
            'from': ''
        }
        
        result = self.parser.parse_email(email_data)
        
        self.assertIsNone(result['job_title'])
        self.assertIsNone(result['company_name'])
        self.assertEqual(result['status'], 'unknown')
        self.assertEqual(result['confidence_score'], 0.0)

    def test_parse_malformed_email(self):
        """Test parsing email with malformed data"""
        email_data = {
            'subject': None,
            'body': {'invalid': 'structure'},
            'from': 123  # Wrong type
        }
        
        result = self.parser.parse_email(email_data)
        
        self.assertIn('error', result)
        self.assertEqual(result['confidence_score'], 0.0)

    def test_parse_offer_email(self):
        """Test parsing job offer email"""
        email_data = {
            'subject': 'Job Offer Letter',
            'body': '''
            Dear Candidate,
            
            We are pleased to offer you the position of:
            Job Title: Senior Data Engineer
            Company: DataTech Solutions
            
            Your starting salary will be...
            ''',
            'from': 'hr@datatech.com'
        }
        
        result = self.parser.parse_email(email_data)
        
        self.assertEqual(result['job_title'], 'Senior Data Engineer')
        self.assertEqual(result['company_name'], 'DataTech Solutions')
        self.assertEqual(result['status'], 'offer')
        self.assertGreater(result['confidence_score'], 0.8)