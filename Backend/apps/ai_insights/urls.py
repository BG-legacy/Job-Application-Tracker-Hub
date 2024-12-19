from django.urls import path
from .views import AIInsightView, ApplicationInsightView, DashboardSummaryView, AIRecommendationsView

urlpatterns = [
    path('insights/', AIInsightView.as_view(), name='ai-insights'),
    path('insights/application/<int:application_id>/', ApplicationInsightView.as_view(), name='application-insights'),
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('recommendations/', AIRecommendationsView.as_view(), name='ai-recommendations'),
] 