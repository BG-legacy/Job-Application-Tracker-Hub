from django.urls import path
from .views import (
    AIInsightView,
    ApplicationInsightView,
    DashboardSummaryView,
    AIRecommendationsView
)

urlpatterns = [
    # Get general AI insights
    path('', AIInsightView.as_view(), name='ai-insights'),
    
    # Get insights for a specific application
    path('application/<int:application_id>/', 
         ApplicationInsightView.as_view(), 
         name='application-insights'),
    
    # Get dashboard summary with AI-enhanced metrics
    path('dashboard/summary/',
         DashboardSummaryView.as_view(), 
         name='dashboard-summary'),
    
    # Get AI-powered recommendations
    path('recommendations/', 
         AIRecommendationsView.as_view(), 
         name='ai-recommendations'),
]