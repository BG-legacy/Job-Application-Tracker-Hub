from django.db import models
from apps.applications.models import Application

class AIInsight(models.Model):
    # Link each insight to a specific job application
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    # Store the analysis of application trends as text
    trend_analysis = models.TextField()
    # Store AI-generated recommendations as text
    recommendations = models.TextField()
    # Automatically set timestamp when insight is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order insights with newest first
        ordering = ['-created_at'] 