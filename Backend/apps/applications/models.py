from django.db import models
from django.contrib.auth import get_user_model

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
    date_applied = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_applied']
        db_table = 'applications_application'

    def __str__(self):
        return f"{self.company_name} - {self.position}" 