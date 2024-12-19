from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    date_applied = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = Application
        fields = ['id', 'company_name', 'position', 'job_title', 'status', 'date_applied', 'job_description', 'notes']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Add validation logging
        print("Validating data:", data)
        return data

    def create(self, validated_data):
        # Add creation logging
        print("Creating application with data:", validated_data)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)