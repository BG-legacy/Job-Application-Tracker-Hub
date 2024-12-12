from rest_framework import serializers
from .models import AIInsight

class AIInsightSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model to serialize
        model = AIInsight
        # Include all relevant fields
        fields = ['id', 'application', 'trend_analysis', 'recommendations', 'created_at']
        # Prevent created_at from being modified
        read_only_fields = ['created_at']