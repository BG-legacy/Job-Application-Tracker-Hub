from django.db import models
from django.conf import settings

class EmailToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_token'
    )
    token_data = models.TextField()  # Stores the full OAuth token data as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_tokens'

class JobEmail(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_emails'
    )
    message_id = models.CharField(max_length=100, unique=True)
    thread_id = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)
    received_date = models.DateTimeField()
    body = models.TextField()
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields for parsed job data
    job_title = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    application_status = models.CharField(
        max_length=50,
        choices=[
            ('applied', 'Applied'),
            ('interview', 'Interview'),
            ('rejected', 'Rejected'),
            ('offer', 'Offer'),
            ('unknown', 'Unknown'),
        ],
        default='unknown'
    )
    parsing_confidence = models.FloatField(default=0.0)

    # New fields for enhanced data
    salary_range = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('full-time', 'Full Time'),
            ('part-time', 'Part Time'),
            ('contract', 'Contract'),
            ('remote', 'Remote'),
            ('unknown', 'Unknown')
        ],
        default='unknown'
    )
    key_requirements = models.JSONField(default=list, blank=True)
    email_domain = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'job_emails'
        ordering = ['-received_date']
        indexes = [
            models.Index(fields=['job_title', 'company_name']),
            models.Index(fields=['application_status']),
            models.Index(fields=['received_date'])
        ]
