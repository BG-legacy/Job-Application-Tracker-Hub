from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings
from ..models import EmailToken
from ..oauth2 import GmailOAuth2
import base64
import email
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .email_parser import JobEmailParser

logger = logging.getLogger(__name__)

class GmailService:
    def __init__(self, user):
        self.user = user
        self.oauth2 = GmailOAuth2()
        
    def get_service(self):
        """Get authenticated Gmail service"""
        try:
            # Get stored token
            token = EmailToken.objects.get(user=self.user)
            credentials = self.oauth2.refresh_credentials(token.token_data)
            
            # Build Gmail service
            return build('gmail', 'v1', credentials=credentials)
            
        except EmailToken.DoesNotExist:
            logger.error(f"No email token found for user {self.user.id}")
            raise Exception("Email not connected")
        except Exception as e:
            logger.error(f"Error getting Gmail service: {str(e)}")
            raise

    def fetch_job_related_emails(self, days_back: int = 30, page_token: str = None) -> dict:
        """Fetch job-related emails from the past X days with pagination support"""
        try:
            service = self.get_service()
            
            # Calculate date range
            date_after = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
            
            # Enhanced search query with job-related keywords
            query = f'''
                after:{date_after} AND (
                    subject:("job application" OR "interview" OR "position" OR
                            "opportunity" OR "career" OR "hiring" OR "recruitment" OR
                            "application status" OR "thank you for applying" OR
                            "application received" OR "job offer" OR "next steps" OR
                            "phone screen" OR "coding test" OR "technical assessment" OR
                            "application confirmation" OR "talent acquisition")
                    OR from:(@linkedin.com OR @greenhouse.io OR @lever.co OR 
                            @workday.com OR @jobvite.com OR @indeed.com OR
                            @smartrecruiters.com OR @recruitee.com OR @hire.com OR
                            @careers OR @talent OR @recruiting OR @hr)
                )
            '''
            
            # Get matching messages with pagination
            results = service.users().messages().list(
                userId='me',
                q=query,
                pageToken=page_token,
                maxResults=50  # Limit results per page
            ).execute()
            
            messages = results.get('messages', [])
            next_page_token = results.get('nextPageToken')
            
            # Fetch full message details
            emails = []
            for msg in messages:
                email_data = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()
                
                parsed_email = self._parse_email(email_data)
                if parsed_email:
                    emails.append(parsed_email)
                    
            return {
                'emails': emails,
                'next_page_token': next_page_token
            }
            
        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            raise

    def _parse_email(self, email_data: Dict) -> Dict[str, Any]:
        """Parse relevant information from email data"""
        try:
            headers = email_data['payload']['headers']
            
            # Extract basic email info
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            from_email = next(h['value'] for h in headers if h['name'] == 'From')
            date = next(h['value'] for h in headers if h['name'] == 'Date')
            
            # Get email body
            body = self._get_email_body(email_data['payload'])
            
            # Ensure date is in ISO format
            received_date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
            formatted_date = received_date.isoformat()
            
            # Basic email data
            parsed_data = {
                'message_id': email_data['id'],
                'thread_id': email_data['threadId'],
                'subject': subject,
                'from': from_email,
                'received_date': formatted_date,  # Use ISO formatted date
                'body': body,
                'labels': email_data['labelIds']
            }

            # Parse job-related information
            job_data = JobEmailParser.parse_email({
                'subject': subject,
                'body': body,
                'from': from_email
            })
            
            # Merge the parsed job data
            parsed_data.update({
                'job_title': job_data.get('job_title'),
                'company_name': job_data.get('company_name'),
                'application_status': job_data.get('status'),
                'parsing_confidence': job_data.get('confidence_score')
            })
            
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing email: {str(e)}")
            return None

    def _get_email_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        if 'body' in payload and payload['body'].get('data'):
            return base64.urlsafe_b64decode(
                payload['body']['data'].encode('ASCII')
            ).decode('utf-8')
            
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(
                        part['body']['data'].encode('ASCII')
                    ).decode('utf-8')
                    
        return ""
