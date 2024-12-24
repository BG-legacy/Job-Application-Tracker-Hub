from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class AIInsightEmailService:
    @staticmethod
    def send_insight_email(user, insights):
        """Send email with AI insights to user"""
        subject = 'Your Job Application Insights'
        
        # Create email context
        context = {
            'username': user.username,
            'metrics': insights['metrics'],
            'recommendations': insights.get('recommendations', '')  # Add recommendations to context
        }
        
        # Render HTML email template
        html_message = render_to_string('ai_insights/email/insights.html', context)
        
        # Create plain text version
        plain_message = f"""
Hi {user.username},

Your Job Application Insights:

{insights.get('recommendations', '')}

Best regards,
Job Application Tracker
"""
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,  # Add plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        ) 