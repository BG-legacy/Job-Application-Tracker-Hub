from django.db import models
from apps.users.models import User
from apps.applications.models import Application

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    reminder_date = models.DateTimeField()
    message = models.TextField() 