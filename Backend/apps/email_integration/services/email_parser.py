import logging
from datetime import datetime
import re
from openai import OpenAI
from typing import Dict, Optional
import json  # Add this import at the top

logger = logging.getLogger(__name__)

class JobEmailParser:
    client = OpenAI()  # Initialize OpenAI client

    @classmethod
    def _format_date(cls, date_str: Optional[str]) -> Optional[str]:
        """Convert various date formats to YYYY-MM-DD or return None if invalid"""
        if not date_str:
            return None
            
        try:
            # Try parsing common date formats
            for fmt in [
                "%Y-%m-%d",           # 2024-03-14
                "%Y/%m/%d",           # 2024/03/14
                "%d-%m-%Y",           # 14-03-2024
                "%d/%m/%Y",           # 14/03/2024
                "%B %d, %Y",          # March 14, 2024
                "%b %d, %Y",          # Mar 14, 2024
                "%Y-%m-%dT%H:%M:%S",  # 2024-03-14T12:00:00
                "%Y-%m-%dT%H:%M:%S.%f%z",  # ISO format with timezone
            ]:
                try:
                    return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
                    
            return None
        except Exception:
            return None

    @classmethod
    def parse_email(cls, email_data: Dict) -> Dict:
        try:
            subject = email_data.get('subject', '') or ''
            body = email_data.get('body', '') or ''
            received_date = cls._format_date(email_data.get('received_date'))
            
            # Clean and combine text
            clean_text = cls._clean_html(f"{subject}\n{body}")
            
            # Use OpenAI to extract information
            response = cls.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract job-related information from the following email. Return a JSON with job_title, company_name, status (interview/offer/rejected/applied/unknown), and application_date (in YYYY-MM-DD format if found, otherwise null)."},
                    {"role": "user", "content": clean_text}
                ],
                response_format={ "type": "json_object" }
            )
            
            # Parse OpenAI response
            parsed_data = json.loads(response.choices[0].message.content)
            
            # Format and validate dates
            parsed_date = cls._format_date(parsed_data.get('application_date'))
            application_date = parsed_date or received_date
            
            return {
                'job_title': parsed_data.get('job_title'),
                'company_name': parsed_data.get('company_name'),
                'status': parsed_data.get('status', 'unknown'),
                'application_date': application_date,
                'confidence_score': 0.8 if parsed_data.get('job_title') else 0.0,
                'parsed_date': datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error parsing email: {str(e)}")
            return cls._get_default_error_response(str(e))

    @classmethod
    def _clean_html(cls, text: str) -> str:
        """Remove HTML content and CSS styles from text"""
        # Remove style tags and their contents
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Remove CSS classes and IDs
        text = re.sub(r'&#\d+;', ' ', text)
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @classmethod
    def _get_default_error_response(cls, error_message: str) -> Dict:
        """Return default error response"""
        return {
            'error': error_message,
            'parsed_date': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'status': 'unknown',
            'job_title': None,
            'company_name': None,
            'application_date': None
        } 
