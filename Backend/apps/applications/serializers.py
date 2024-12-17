from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'company_name',
            'position',
            'job_title',
            'job_description',
            'notes',
            'status',
            'date_applied',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['updated_at']

    def create(self, validated_data):
        # Automatically set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)