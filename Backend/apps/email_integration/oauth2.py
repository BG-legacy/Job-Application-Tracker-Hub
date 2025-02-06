from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)

class GmailOAuth2:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "javascript_origins": ["http://localhost:8000"]
            }
        }
        logger.info(f"OAuth2 config initialized with redirect URI: {settings.GOOGLE_REDIRECT_URI}")

    def get_authorization_url(self):
        """Generate OAuth2 authorization URL"""
        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=self.SCOPES,
                redirect_uri=settings.GOOGLE_REDIRECT_URI
            )
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'  # Force consent screen
            )
            
            logger.info(f"Generated auth URL: {authorization_url}")
            logger.info(f"Generated state: {state}")
            
            return authorization_url, state
            
        except Exception as e:
            logger.error(f"Error generating auth URL: {str(e)}", exc_info=True)
            raise

    def get_credentials(self, auth_code):
        """Exchange authorization code for credentials"""
        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=self.SCOPES,
                redirect_uri=settings.GOOGLE_REDIRECT_URI
            )
            
            logger.info(f"Exchanging code for credentials with redirect URI: {settings.GOOGLE_REDIRECT_URI}")
            flow.fetch_token(code=auth_code)
            
            return flow.credentials
            
        except Exception as e:
            logger.error(f"Error getting credentials: {str(e)}", exc_info=True)
            raise

    def refresh_credentials(self, token_data):
        """Refresh expired credentials"""
        credentials = Credentials.from_authorized_user_info(
            json.loads(token_data),
            self.SCOPES
        )
        
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            
        return credentials