from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'company_name', 'job_title', 'status', 'applied_date', 'updated_at']
        read_only_fields = ['updated_at']