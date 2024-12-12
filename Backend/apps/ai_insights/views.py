from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.analysis_service import AIAnalysisService
from .models import AIInsight
from .serializers import AIInsightSerializer

class AIInsightView(APIView):
    # Ensure only authenticated users can access
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Create analysis service instance
        analysis_service = AIAnalysisService()
        # Generate insights for the current user
        insights = analysis_service.analyze_application_trends(request.user)
        
        # Return formatted response
        return Response({
            'trend_analysis': insights['trend_analysis'],
            'recommendations': insights['recommendations']
        })

class ApplicationInsightView(APIView):
    # Ensure only authenticated users can access
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        try:
            # Get insights for specific application (only if user owns it)
            insight = AIInsight.objects.get(
                application_id=application_id,
                application__user=request.user
            )
            # Serialize the insight data
            serializer = AIInsightSerializer(insight)
            return Response(serializer.data)
        except AIInsight.DoesNotExist:
            # Return 404 if no insights found
            return Response({'error': 'No insights found'}, status=404)