from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import redirect
from .oauth2 import GmailOAuth2
from .models import EmailToken, JobEmail
from .services.email_service import GmailService
import json
import logging
from urllib.parse import urlencode
from django.conf import settings
from django.contrib.auth.models import User
from apps.users.models import User  # Import your custom User model
from django.core.cache import cache
from datetime import timedelta
from rest_framework import status
from datetime import datetime
from rest_framework.decorators import api_view
from django.utils import timezone
from apps.applications.models import Application

logger = logging.getLogger(__name__)

class EmailAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Start OAuth2 flow"""
        try:
            oauth2 = GmailOAuth2()
            auth_url, state = oauth2.get_authorization_url()
            
            # Store state in session
            request.session['oauth_state'] = state
            request.session.modified = True
            
            logger.info(f"Starting OAuth flow with state: {state}")
            logger.info(f"Redirect URI: {settings.GOOGLE_REDIRECT_URI}")
            
            # Instead of returning JSON, redirect directly to Google
            return redirect(auth_url)
            
        except Exception as e:
            logger.error(f"Error in auth flow: {str(e)}", exc_info=True)
            return Response({
                'error': str(e),
                'debug': {
                    'session_data': dict(request.session),
                }
            }, status=500)

class OAuth2CallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Handle OAuth2 callback"""
        try:
            logger.info(f"Callback received with params: {dict(request.GET)}")
            
            code = request.GET.get('code')
            state = request.GET.get('state')

            if not code or not state:
                return self._redirect_to_frontend(error='Missing code or state parameter')

            # Get user_id from cache using state
            cache_key = f"oauth_state_{state}"
            cache_data = cache.get(cache_key)
            
            if not cache_data:
                return self._redirect_to_frontend(error='Invalid or expired state')
            
            user_id = cache_data['user_id']
            user = User.objects.get(id=user_id)
            
            # Exchange code for credentials
            oauth2 = GmailOAuth2()
            credentials = oauth2.get_credentials(code)
            
            # Store the token
            token_data = credentials.to_json()
            EmailToken.objects.update_or_create(
                user=user,
                defaults={'token_data': token_data}
            )
            
            # Clear the cache
            cache.delete(cache_key)
            
            # Redirect to frontend with success status
            return self._redirect_to_frontend(success=True)
            
        except User.DoesNotExist:
            logger.error(f"User not found for ID: {user_id}")
            return self._redirect_to_frontend(error='User not found')
        except Exception as e:
            logger.error(f"Callback error: {str(e)}", exc_info=True)
            return self._redirect_to_frontend(error=str(e))

    def _redirect_to_frontend(self, success=False, error=None):
        """Helper method to redirect to frontend with appropriate parameters"""
        # Get the frontend URL from settings
        frontend_url = settings.FRONTEND_URL  # Add this to your settings.py
        
        # Build the redirect URL with parameters
        params = {
            'status': 'success' if success else 'error'
        }
        
        if error:
            params['error'] = error
            
        redirect_url = f"{frontend_url}/email-integration?{urlencode(params)}"
        return redirect(redirect_url)

class EmailSyncView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Sync job-related emails"""
        try:
            service = GmailService(request.user)
            emails = service.fetch_job_related_emails()
            
            # Save emails to database
            saved_count = 0
            for email_data in emails:
                job_email, created = JobEmail.objects.update_or_create(
                    message_id=email_data['message_id'],
                    defaults={
                        'user': request.user,
                        'thread_id': email_data['thread_id'],
                        'subject': email_data['subject'],
                        'from_email': email_data['from'],
                        'received_date': email_data['date'],
                        'body': email_data['body'],
                        'job_title': email_data.get('job_title'),
                        'company_name': email_data.get('company_name'),
                        'application_status': email_data.get('application_status', 'unknown'),
                        'parsing_confidence': email_data.get('parsing_confidence', 0.0),
                        'is_processed': True
                    }
                )
                if created:
                    saved_count += 1
            
            return Response({
                'message': f'Successfully synced {len(emails)} emails',
                'saved_new': saved_count,
                'total_processed': len(emails)
            })
            
        except Exception as e:
            logger.error(f"Error syncing emails: {str(e)}")
            return Response(
                {'error': f'Failed to sync emails: {str(e)}'},
                status=500
            )

class TestEmailFetchView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Test email fetching"""
        try:
            # Get the user with stored token
            user = User.objects.filter(email_token__isnull=False).first()
            if not user:
                return Response({
                    'error': 'No user found with Gmail token',
                    'debug': {
                        'users_count': User.objects.count(),
                        'tokens_count': EmailToken.objects.count()
                    }
                }, status=400)
            
            service = GmailService(user)
            emails = service.fetch_job_related_emails(days_back=10)
            
            return Response({
                'success': True,
                'user_email': user.email,
                'email_count': len(emails),
                'emails': emails[:5]  # Return first 5 emails for preview
            })
            
        except Exception as e:
            logger.error(f"Email fetch error: {str(e)}", exc_info=True)
            return Response({
                'error': str(e),
                'debug': {
                    'users_count': User.objects.count(),
                    'tokens_count': EmailToken.objects.count()
                }
            }, status=500)

class ConnectEmailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Initialize email connection flow"""
        try:
            oauth2 = GmailOAuth2()
            auth_url, state = oauth2.get_authorization_url()
            
            # Store state AND user_id in cache
            cache_key = f"oauth_state_{state}"  # Use state as key
            cache_data = {
                'user_id': request.user.id,
                'expires': datetime.now() + timedelta(minutes=5)
            }
            cache.set(cache_key, cache_data, timeout=300)  # 5 minutes expiry
            
            return Response({
                'auth_url': auth_url,
                'state': state,
                'expires_in': 300
            })
            
        except Exception as e:
            logger.error(f"Email connection error: {str(e)}")
            return Response({'error': str(e)}, status=500)

class ScrapeEmailsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Fetch and parse emails"""
        try:
            days_back = request.data.get('days_back', 30)
            page_token = request.data.get('page_token')
            
            service = GmailService(request.user)
            result = service.fetch_job_related_emails(days_back=days_back, page_token=page_token)
            
            # Sanitize email data before caching
            sanitized_emails = []
            for email in result['emails']:
                sanitized_email = {
                    'message_id': email.get('message_id'),
                    'thread_id': email.get('thread_id'),
                    'subject': email.get('subject'),
                    'from': email.get('from'),
                    'received_date': email.get('received_date'),
                    'body': email.get('body', '')[:1000],  # Limit body length
                    'job_title': email.get('job_title'),
                    'company_name': email.get('company_name'),
                    'application_status': email.get('application_status', 'unknown'),
                    'parsing_confidence': email.get('parsing_confidence', 0.0),
                    'labels': email.get('labels', [])
                }
                sanitized_emails.append(sanitized_email)
            
            # Store sanitized emails in cache
            cache_key = f"parsed_emails_{request.user.id}"
            cache.set(cache_key, sanitized_emails, timeout=3600)  # 1 hour expiry
            
            return Response({
                'message': f'Successfully parsed {len(sanitized_emails)} emails',
                'emails': sanitized_emails,
                'next_page_token': result.get('next_page_token'),
                'cache_key': cache_key
            })
            
        except Exception as e:
            logger.error(f"Email scraping error: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ConfirmApplicationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Save confirmed parsed emails to database and create corresponding applications"""
        try:
            # Get email IDs from request
            email_ids = request.data.get('email_ids', [])
            
            if not email_ids:
                return Response({
                    'error': 'No email IDs provided',
                    'received_data': request.data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get cached emails
            cache_key = f"parsed_emails_{request.user.id}"
            cached_emails = cache.get(cache_key)
            
            if not cached_emails:
                return Response({
                    'error': 'No parsed emails found in cache',
                    'cache_key': cache_key
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Filter emails by selected IDs
            selected_emails = [
                email for email in cached_emails 
                if email.get('message_id') in email_ids
            ]
            
            if not selected_emails:
                return Response({
                    'error': 'None of the provided email IDs were found in cache',
                    'provided_ids': email_ids
                }, status=status.HTTP_400_BAD_REQUEST)
            
            saved_count = 0
            applications_created = 0
            
            for email_data in selected_emails:
                try:
                    # Create or update JobEmail
                    job_email = JobEmail.objects.update_or_create(
                        message_id=email_data['message_id'],
                        defaults={
                            'user': request.user,
                            'thread_id': email_data.get('thread_id', ''),
                            'subject': email_data.get('subject', ''),
                            'from_email': email_data.get('from', ''),
                            'received_date': email_data.get('received_date') or timezone.now(),
                            'body': email_data.get('body', ''),
                            'job_title': email_data.get('job_title'),
                            'company_name': email_data.get('company_name'),
                            'application_status': email_data.get('application_status', 'unknown'),
                            'parsing_confidence': email_data.get('parsing_confidence', 0.0),
                            'is_processed': True
                        }
                    )[0]
                    saved_count += 1
                    
                    # Create Application
                    application_date = email_data.get('received_date')
                    if isinstance(application_date, str):
                        try:
                            application_date = datetime.strptime(
                                application_date.split('T')[0], 
                                '%Y-%m-%d'
                            ).date()
                        except (ValueError, TypeError):
                            application_date = timezone.now().date()
                    
                    status_mapping = {
                        'applied': 'Pending',
                        'interview': 'Interview',
                        'rejected': 'Rejected',
                        'offer': 'Offer',
                        'unknown': 'Pending'
                    }
                    
                    Application.objects.create(
                        user=request.user,
                        company_name=email_data.get('company_name', 'Unknown Company'),
                        position=email_data.get('job_title', 'Unknown Position'),
                        job_title=email_data.get('job_title', 'Unknown Position'),
                        status=status_mapping.get(
                            email_data.get('application_status', 'unknown').lower(),
                            'Pending'
                        ),
                        date_applied=application_date,
                        job_description=email_data.get('body', ''),
                        notes=f"Created from email: {email_data.get('subject', '')}"
                    )
                    applications_created += 1
                    
                except Exception as e:
                    logger.error(f"Error processing email {email_data.get('message_id')}: {str(e)}")
                    continue
            
            # Clear cache after processing
            cache.delete(cache_key)
            
            return Response({
                'message': f'Successfully processed {saved_count} emails',
                'saved_emails': saved_count,
                'created_applications': applications_created
            })
            
        except Exception as e:
            logger.error(f"Error in ConfirmApplicationsView: {str(e)}")
            return Response({
                'error': str(e),
                'detail': 'Error processing email confirmation'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConnectionStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Check if user has connected their email"""
        try:
            # Check if user has an email token
            has_token = EmailToken.objects.filter(user=request.user).exists()
            
            return Response({
                'is_connected': has_token,
                'status': 'connected' if has_token else 'disconnected',
                'user_email': request.user.email
            })
            
        except Exception as e:
            logger.error(f"Error checking email connection status: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def get_emails(request):
    page_token = request.GET.get('page_token')
    days_back = int(request.GET.get('days_back', 30))
    
    email_service = GmailService(request.user)
    result = email_service.fetch_job_related_emails(days_back=days_back, page_token=page_token)
    
    return Response({
        'emails': result['emails'],
        'next_page_token': result['next_page_token']
    })