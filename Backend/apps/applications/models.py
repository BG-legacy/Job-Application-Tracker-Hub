from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
        ('Withdrawn', 'Withdrawn'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=200)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_applied = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_applied']
        db_table = 'applications_application'

    def __str__(self):
        return f"{self.company_name} - {self.position}" 

    def save(self, *args, **kwargs):
        # Ensure date_applied is a date object in UTC
        if isinstance(self.date_applied, str):
            try:
                # Parse the date in UTC
                self.date_applied = timezone.datetime.strptime(
                    self.date_applied, 
                    '%Y-%m-%d'
                ).date()
            except ValueError:
                self.date_applied = timezone.now().date()
        super().save(*args, **kwargs)