from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
from datetime import datetime, timedelta
from django.utils import timezone

class ApplicationListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ApplicationDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer
    
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        applications = Application.objects.filter(user=user)
        
        # Get date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        stats = {
            "total_applications": applications.count(),
            "by_status": {
                "pending": applications.filter(status='Pending').count(),
                "interviews": applications.filter(status='Interview').count(),
                "offers": applications.filter(status='Offer').count(),
                "rejected": applications.filter(status='Rejected').count()
            },
            "time_based": {
                "last_7_days": applications.filter(applied_date__gte=week_ago).count(),
                "last_30_days": applications.filter(applied_date__gte=month_ago).count(),
            },
            "recent_applications": applications.order_by('-applied_date')[:5].values(
                'company_name', 'job_title', 'status', 'applied_date'
            )
        }
        return Response(stats) 